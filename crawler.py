# This program is optimized for python3.6

import argparse
import http.client
import sys
import re

processed = []

def search_links(url, depth, keyword):
    url_is_processed = (url in processed)
    if (url.startswith("http://") and (not url_is_processed)):
        processed.append(url)
        url = host = url.replace("http://", "", 1)
        path = "/"

        urlparts = url.split('/')
        if (len(urlparts) > 1):
            host = urlparts[0]
            path = url.replace(host, '', 1)

        print("Creawling URL path:%s%s " %(host, path))
        conn = http.client.HTTPConnection(host)
        req = conn.request("GET", path)
        result = conn.getresponse()

        contents = result.read().decode('utf-8')
        pattern = re.compile(r'href="(.*?)"')
        all_links = pattern.findall(contents)

        if (keyword in contents):
            print("Found %s at %s" %(keyword, url))

        print("===> %s: processing %s links" %(str(depth), str(len(all_links))))
        for href in all_links:
            if (href.startswith("/")):
                href = "http://%s%s" %(host, href)

            if (depth > 0):
                search_links(href, depth-1, href)

    else:
        print("Skipping link: %s" %url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Webpage link crawler")
    parser.add_argument('--url', action="store", dest="url", required=True)
    parser.add_argument('--query', action="store", dest="query", required=True)
    parser.add_argument('--depth', action="store", dest="depth", default=3)

    given_args = parser.parse_args()

    try:
        search_links(given_args.url, given_args.depth, given_args.query)
    except KeyboardInterrupt:
        print("Aborting search by user request")