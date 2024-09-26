#!/usr/bin/env python3
"""
This module takes Australian Federal Election bookmaker odds.
It then determines the probability of each party winning the next federal election, based on those odds.
Finally, it compares this week's probability of winning to previous periods.
"""
# Program Details
__author__ = "Kojrey"
__version__ = "0.1.1"


# KISS Rquirements
# 1	Collects Odds from 4x major bookmakers
# 2	Averages these to create odds
# 3	Converts odds to probability of winning
# 4	Prints odds of all parties winning this week
# 5	Prints change in percentage vs last week, last month, last year
# 6	Needs to somehow save this over time ...as it is watching the trend that makes this valuable (YOU COULD EXPORT THE RESULTS TO A CSV THAT COULD THEN BE MORE EASILY CONVERTED TO A CHART?)
# 7	Generates graph (YOU COULD EXPORT THE RESULTS TO A CSV THAT COULD THEN BE MORE EASILY CONVERTED TO A CHART?)
# 8	Posts graph to social media
# 9	Repeats every Sunday


# IMPORT STATEMENTS



# Political party Lists, where bookmaker odds will be stored
#### Note, you will have to scrape this data
#### You don't know how to do this at this point
#### So leave this till later, and just use dummy data for now
alp_list = [2, 2, 2, 2]
lnp_list = [4, 4, 4, 4]
oth_list = [50, 75, 75, 100] # 'Any Other Party'. This is how the bookmakers classify this market 

# FUNCTION DEFINITION

# Function to determine the average odds of political parties
def list_average(party):
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
    implied_prob = (1 / avg_odds)
    return implied_prob

#### Incremental testing below
alp_prob = prob_win(alp_avg)
lnp_prob = prob_win(lnp_avg)
oth_prob = prob_win(oth_avg)

# f strings to make %'s https://medium.com/bitgrit-data-science-publication/python-f-strings-tricks-you-should-know-7ce094a25d43
print("The ALP's probabilty of winning is", f'{alp_prob:.2%}')
print("The LNP's probabilty of winning is", f'{lnp_prob:.2%}')
print("Any Other Party's probabilty of winning is", f'{oth_prob:.2%}')
#### Incremental testing above