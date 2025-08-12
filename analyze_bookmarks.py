#!/usr/bin/env python3
import json
import re
import sys
import os.path
import lz4.block  # => https://pypi.org/project/lz4/


def mozlz4_to_text(filepath):
    """
    Given the path to a "mozlz4", "jsonlz4", "baklz4" etc. file, return the uncompressed text.
    from https://gist.github.com/snorey/3eaa683d43b0e08057a82cf776fd7d83
    """
    bytestream = open(filepath, "rb")
    bytestream.read(8)  # skip past the b"mozLz40\0" header
    valid_bytes = bytestream.read()
    text = lz4.block.decompress(valid_bytes)
    return text


def analyze(node: dict):
    if "uri" in node:
        if node["uri"][0:4] == 'http':
            host = re.sub(r"^https?://([^/]+)/??.*?$", r"\1", node["uri"])
            if host[0:4] == 'www.':
                host = host[4:]
            bookmark_count_for_host[host] = bookmark_count_for_host.get(host, 0) + 1
    if "children" in node:
        for child in node["children"]:
            analyze(child)


if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
    print("wrong parameters - supply the path to a file inside your Firefox profile's 'bookmarkbackups' directory")
    exit(1)
bookmarks = json.loads(mozlz4_to_text(sys.argv[1]))
bookmark_count_for_host = dict()
analyze(bookmarks)
sorted_bookmark_count_for_host = sorted(bookmark_count_for_host.items(), key=lambda x: (-x[1], x[0]))
for entry in sorted_bookmark_count_for_host:
    print(f"{entry[0]};{entry[1]}")
