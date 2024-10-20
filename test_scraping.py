import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

# Ignore SSL certificate errors
# Remove this section, and remove context=ctx if I get errors with https sites
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html = urllib.request.urlopen('https://www.sportsbet.com.au/betting/politics/australian-federal-politics/48th-parliament-of-australia-8571604')
a_soup_object = BeautifulSoup(html, 'html.parser')
# And now we can ask the soup object some questions, after it has parsed all the messy data


alp = a_soup_object.find_all('span', {'data-automation-id': 'price-text'})[0].string
lnp = a_soup_object.find_all('span', {'data-automation-id': 'price-text'})[1].string

alp_f = float(alp)
lnp_f = float(lnp)

