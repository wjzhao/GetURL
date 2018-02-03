# This program is optimized for python3.6

import argparse
import http.client
import sys
import re

processed = []

def search_links(url, depth, keyword):
    url_is_processed = (url in processed)
    if (not url_is_processed):
        processed.append(url)

        urlparts = url.split('/')
        if (len(urlparts) > 1):
            host = urlparts[0]
            path = url.replace(host, '', 1)

        print("Creawling URL path:%s%s " %(host, path))
        conn = http.client.HTTPConnection(host)
        req = conn.request("GET", path)
        result = conn.getresponse()

        