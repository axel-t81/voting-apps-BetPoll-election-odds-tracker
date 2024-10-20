#!/usr/bin/env python3


import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
# Remove this section, and remove context=ctx if I get errors with https sites
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter --')
html = urllib.request.urlopen(url, context=ctx).read()
a_soup_object = BeautifulSoup(html, 'html.parser')
# And now we can ask the soup object some questions, after it has parsed all the messy data


# Retrieve all the anchor tags
tags = a_soup_object('a')
for tag in tags:
    print(tag.get('href', None))