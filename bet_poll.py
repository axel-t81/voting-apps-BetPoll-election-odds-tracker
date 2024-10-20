#!/usr/bin/env python3
"""
This module takes Australian Federal Election bookmaker odds.
It then determines the probability of each party winning the next federal election, based on those odds.
Finally, it compares this week's probability of winning to previous periods.
"""
# Program Details
__author__ = "Kojrey"
__version__ = "0.1.2"


# KISS Rquirements
# 1	SEE ** BELOW Collects Odds from 4x major bookmakers
# 2	DONE Averages these to create odds
# 3	DONE Converts odds to probability of winning
# 4	DONE Prints odds of all parties winning this week
# 5	SEE ** BELOW Prints change in percentage vs last week, last month, last year (THIS NEEDS SOME SORT OF LONG TERM MEMORY and May Bleed in)
# 6	SEE ** BELOW Needs to somehow save this over time ...as it is watching the trend that makes this valuable (YOU COULD EXPORT THE RESULTS TO A CSV THAT COULD THEN BE MORE EASILY CONVERTED TO A CHART? ...but surely Python has charting/visualisation!!!)
# 7	Generates graph (YOU COULD EXPORT THE RESULTS TO A CSV THAT COULD THEN BE MORE EASILY CONVERTED TO A CHART? ...but surely Python has charting/visualisation!!!)
# 8	Posts graph to social media
# 9	Repeats every Sunday
#
# ** You need to learn very basics of (1) web scraping and (2) a one table database? Or writing and reading from file?
# ** For number 2, look into json https://stackoverflow.com/questions/4450144/easy-save-load-of-data-in-python or 'pickle' https://www.askpython.com/python/examples/save-data-in-python
# ** And here's another guide, when you like GeekforGeeks https://www.geeksforgeeks.org/saving-text-json-and-csv-to-a-file-in-python/


# IMPORT STATEMENTS
import json
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re


# Political party Lists, where bookmaker odds will be stored
#### Note, you will have to scrape this data
#### You don't know how to do this at this point
#### So leave this till later, and just use dummy data for now
alp_list = [2, 2, 2, 2]
lnp_list = [4, 4, 4, 4]
oth_list = [50, 75, 75, 100] # 'Any Other Party'. This is how the bookmakers classify this market 

# FUNCTION DEFINITION

# Function to get odds from SportsBet
def sportsbet(party):

    if party == 'alp' or 'ALP':
        index = 0
    else:
        index = 1
    
    # Ignore SSL certificate errors
    # Remove this section, and remove context=ctx if I get errors with https sites
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urllib.request.urlopen('https://www.sportsbet.com.au/betting/politics/australian-federal-politics/48th-parliament-of-australia-8571604')
    a_soup_object = BeautifulSoup(html, 'html.parser')
    # And now we can ask the soup object some questions, after it has parsed all the messy data


    odds = a_soup_object.find_all('span', {'data-automation-id': 'price-text'})[index].string
    odds_f = float(odds)
    return odds_f


# Function to determine the average odds of political parties
def list_average(party):
    """Calculate average of bookmaker odds."""
    avg = sum(party) / len(party)
    return avg

#### Incremental testing below
alp_avg = list_average(alp_list)
lnp_avg = list_average(lnp_list)
oth_avg = list_average(oth_list)

print("The ALP average is", alp_avg)
print("The LNP average is", lnp_avg)
print("The Any Other Party average is", oth_avg)
#### Incremental testing above

# Function to determine the probability of each party winning
# This function uses the 'Converting decimal odds to implied probability' formula 
def prob_win(avg_odds):
    """Determine implied probability of bookmaker odds."""
    implied_prob = (1 / avg_odds)
    return implied_prob

#### Incremental testing below
alp_prob = prob_win(alp_avg)
lnp_prob = prob_win(lnp_avg)
oth_prob = prob_win(oth_avg)

print("The ALP's probabilty of winning is", f'{alp_prob:.2%}')
print("The LNP's probabilty of winning is", f'{lnp_prob:.2%}')
print("Any Other Party's probabilty of winning is", f'{oth_prob:.2%}')
#### Incremental testing above



# References:
# 1) https://medium.com/bitgrit-data-science-publication/python-f-strings-tricks-you-should-know-7ce094a25d43
# 2) https://help.smarkets.com/hc/en-gb/articles/214058369-How-to-calculate-implied-probability-in-betting
# 3) https://www.geeksforgeeks.org/find-average-list-python/
