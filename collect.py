#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    with open(path.join("data", view["name"] + ".csv"), "w") as csvf:
        print >> csvf, ",".join(["date"] + FIELDS)
        # API returns maximum 1000 dates at once
        while stdate < eddate:
            st = stdate.isoformat()
            ed = (min(eddate, stdate + timedelta(days=999))).isoformat()
            stdate = stdate + timedelta(days=1000)
            response = query(analytics, view["id"], st, ed)
            for row in response["reports"][0]["data"]["rows"]:
                results = [datize(row["dimensions"][0])] + row["metrics"][0]["values"]
                print >> csvf, ",".join(results)

if __name__ == "__main__":
    if not path.exists("data"):
        makedirs("data")
    analytics = connectAPI()
    for view in VIEWS:
        collect(analytics, view)
