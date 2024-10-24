# See ChatGPT conversation here: https://chatgpt.com/c/6719d254-1a08-800c-970d-e6aadf0604ba
# It looks like TAB obscures their data from Beautiful Soup because it is JavaScript rendered content
# Note: TAB does have a API for personal, non-commercial use
# Consider (a) switching away from TAB as one of the 4 (b) applying for a non-commercial API (c) Following ChatGPTs advice 
# and using another less simple library beyond Beautiful Soup, and ChatGPT gives a couple of examples.




import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

def tab(party):
    if party == 'alp' or 'ALP':
        index = 0
    else:
        index = 1

    # Ignore SSL certificate errors
    # Remove this section, and remove context=ctx if I get errors with https sites
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urllib.request.urlopen('https://www.tab.com.au/sports/betting/Politics/competitions/Australian%20Federal%20Politics/matches/Federal%20Election%20Winner')
    a_soup_object = BeautifulSoup(html, 'html.parser')
    # And now we can ask the soup object some questions, after it has parsed all the messy data

    main_table = a_soup_object.css.select("body")
    # odds = main_table.find('span')
    print(main_table)
    
    #odds_f = float(odds)

    #return odds_f

test_alp = tab('alp')
#print(test_alp)