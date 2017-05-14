#!/usr/bin/env python

import csv, sys, re

re_date = re.compile(r"^(\d+)/(\d+)/(\d+)$")
def reformat_date(d):
    els = re_date.search(row[0]).groups()
    return "%04d-%02d-%02d" % (int("20"+els[2]), int(els[1]), int(els[0]))

with open(sys.argv[1]) as f:
    for row in csv.reader(f):
        if not row or not row[0] or row[0].startswith("#"):
            continue
        if "/" in row[0]:
            row[0] = reformat_date(row[0])
            for idx in range(1, len(row)):
                row[idx] = row[idx].replace(",", "")
        print ",".join(row)
