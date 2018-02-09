# This is where I plan to execute the while loop that is currently in class.py
import sys, random, sqlite3
from pprint import pprint
from functions import *
from obj import *

# First we want to know how many iterations we need to loop
rounds = sys.argv[1]


# test looping on all listings run 100 times to try to get a better idea of probabilty
y = int(rounds)
while y > 0:
	y -= 1
	dayStart()
	for x in range(1,26):
		Listing(x).dayTrade()
		if Listing(x).IndustryID == 6:
			continue
		elif Listing(x).IndustryID == 7:
			Listing(x).TradeChange()
			continue
		else:
			Listing(x).ValueChange()
	continue