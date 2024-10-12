#!/usr/bin/env python3


import urllib.request, urllib.parse, urllib.error

fhand = urllib.request.urlopen('https://www.sportsbet.com.au/betting/politics/australian-federal-politics/48th-parliament-of-australia-8571604')
for line in fhand:
    print(line.decode().strip())


