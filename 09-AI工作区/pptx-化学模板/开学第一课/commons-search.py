# -*- coding: utf-8 -*-
"""Commons 文件搜索助手：python commons-search.py "query" [limit]"""
import json
import sys
import urllib.parse
import urllib.request

q = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 8
url = ('https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6'
       f'&srlimit={limit}&format=json&srsearch=' + urllib.parse.quote(q))
req = urllib.request.Request(url, headers={'User-Agent': 'course-material/1.0 (teacher)'})
d = json.load(urllib.request.urlopen(req, timeout=30))
for r in d['query']['search']:
    print(r['title'][5:])
