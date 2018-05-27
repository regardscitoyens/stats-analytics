#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from csv import reader
from os import path, makedirs
from datetime import datetime, timedelta
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from settings import VIEWS, FIELDS, KEY_FILE_LOCATION

def connectAPI():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, 'https://www.googleapis.com/auth/analytics.readonly')
    return build('analytics', 'v4', credentials=credentials)

def query(analytics, view, start, end):
    return analytics.reports().batchGet(body={
      'reportRequests': [{
        'viewId': view,
        'dimensions': [{'name': 'ga:date'}],
        'metrics': [{'expression': 'ga:%s' % f} for f in FIELDS],
        'dateRanges': [{'startDate': start, 'endDate': end}]
      }]
    }).execute()

datize = lambda d: "%s-%s-%s" % (d[0:4], d[4:6], d[6:8])

def collect(analytics, view):
    stdate = datetime.strptime(view["start"], "%Y-%m-%d").date()
    eddate = datetime.today().date() + timedelta(days=-1)
    csvfile = path.join("data", view["name"] + ".csv")
    if path.exists(csvfile):
        with open(csvfile, "r") as csvf:
            olddata = list(reader(csvf))[1:]
    data = []
    # API returns maximum 1000 dates at once
    while stdate < eddate:
        st = stdate.isoformat()
        ed = (min(eddate, stdate + timedelta(days=999))).isoformat()
        stdate = stdate + timedelta(days=1000)
        response = query(analytics, view["id"], st, ed)
        try:
            for row in response["reports"][0]["data"]["rows"]:
                results = [datize(row["dimensions"][0])] + row["metrics"][0]["values"]
                data.append(results)
        except Exception as e:
            print >> sys.stderr, "ERROR with", view, "from", st, "to", ed
            print >> sys.stderr, "Data doesn't have rows", response
    idx = 0
    merged = []
    for row in olddata:
        if data[idx][0] > row[0]:
            merged.append(row)
        else:
            merged.append(data[idx])
            idx += 1
    merged += data[idx:]
    with open(csvfile, "w") as csvf:
        print >> csvf, ",".join(["date"] + FIELDS)
        for row in merged:
            print >> csvf, ",".join(row)

if __name__ == "__main__":
    if not path.exists("data"):
        makedirs("data")
    analytics = connectAPI()
    for view in VIEWS:
        collect(analytics, view)
