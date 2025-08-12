#!/usr/bin/env python3
import sqlite3
import re
import sys
import os.path

if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
    print("wrong parameters - supply the path to your Firefox profile's 'places.sqlite' file")
    exit(1)
conn = sqlite3.Connection(f"file:{sys.argv[1]}?immutable=1")
places = conn.execute("SELECT url, visit_count FROM 'moz_places' order by visit_count desc, url asc").fetchall()
visit_count_for_host = dict()
for place in places:
    if place[0][0:4] != 'http':
        continue
    host = re.sub(r"^https?://([^/]+)/??.*?$", r"\1", place[0])
    if host[0:4] == 'www.':
        host = host[4:]
    visit_count_for_host[host] = visit_count_for_host.get(host, 0) + place[1]
sorted_visit_count_for_host = sorted(visit_count_for_host.items(), key=lambda x: -x[1])
for entry in sorted_visit_count_for_host:
    print(f"{entry[0]};{entry[1]}")
