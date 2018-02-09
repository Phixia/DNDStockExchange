import sys, random, sqlite3
from pprint import pprint
#sys.path.insert(0)
from functions import *


class Listing(object):
	# Listings have the following Properties
	# ListingID (1-20)
	# Listing Name (between 1-4 letters)
	# Long Name
	# Price (Current Stock Value)
	# Volume (Current available # of stock for purchase)
	# PositionChange (% increase or decrease from yesterdays Price)
	# IndustryID (Will have an industry table, where I can provide names of the industries)


	def __init__(self, ListingID):
		self.ListingID = (ListingID,)
		conn = Conn()
		data = conn.execute('SELECT listing_name, longname, listing_price, listing_volume, listing_change, listing_industryid, listing_investid, listing_production FROM Listings WHERE listing_id=?', self.ListingID)
		for row in data:
			self.Listing = row[0]
			self.Name = row[1]
			self.Price = row[2]
			self.Volume = row[3]
			self.PositionChange = row[4]
			self.IndustryID = row[5]
			self.InvestID = row[6]
			self.Production = row[7]
		conn.close()
		return

	def __str__(self):
		output = ( "{}\n"
							"Listing: {}\n"
							"Name: {}\n"
							"Price: {}\n"
							"Volume: {}\n"
							"Change: {}\n")

		return output.format("",
									self.Listing,
									self.Name,
									self.Price,
									self.Volume,
									self.PositionChange,
									self.IndustryID)
	
# This is where we need to define what happens during a single day in the exchange. This function will be called for each listing to simulate a days worth of trade.
# When we get to that logic, Order the listing_id's by descending order and grab the first one (the highest number) then iterate a while loop, incrementing a counter from 1-N (the highest number).
# Each iteration of the loop will run dayTrade(x), and update the resource table with the outcome.

# The first iteration needs to clear out the resource table. Each day we will start with a blank slate? (I may not do this so keeping it contained in a function makes it easy to remove)





	def dayTrade(self):
		if self.IndustryID == 1:
			FoodProduced = FoodProduce()
			toolUse = ToolUse()
			materialUse = MaterialUse()
			final_product = FoodProduced + toolUse + materialUse
			ResourceUpdate(1, FoodProduced)
			ResourceUpdate(3, toolUse)
			ResourceUpdate(2, materialUse)
			Product(self.ListingID, final_product)
			VolumeChange(self.ListingID)
			return
		elif self.IndustryID == 2:
			MaterialProduced = MaterialProduce()
			toolUse = ToolUse()
			foodUse = FoodUse()
			final_product = MaterialProduced + toolUse + foodUse
			ResourceUpdate(1, foodUse)
			ResourceUpdate(3, toolUse)
			ResourceUpdate(2, MaterialProduced)
			Product(self.ListingID, final_product)
			VolumeChange(self.ListingID)

			return
		elif self.IndustryID == 3:
			foodUse = FoodUse()
			materialUse = MaterialUse()
			toolProduced = ToolProduce()
			final_product = toolProduced + foodUse + materialUse
			ResourceUpdate(1, foodUse)
			ResourceUpdate(2, materialUse)
			ResourceUpdate(3, toolProduced)
			Product(self.ListingID, final_product)
			VolumeChange(self.ListingID)
			return
		elif self.IndustryID == 4:
			foodUse = FoodUse()
			toolUse = ToolUse()
			magicUse = MagicUse()
			reagentProduced = ReagentProduce()
			final_product = reagentProduced + magicUse + toolUse + foodUse
			ResourceUpdate(1, foodUse)
			ResourceUpdate(3, toolUse)
			ResourceUpdate(4, reagentProduced)
			ResourceUpdate(5, magicUse)
			Product(self.ListingID, final_product)
			VolumeChange(self.ListingID)
			return
		elif self.IndustryID == 5:
			materialUse = MaterialUse()
			reagentUse = ReagentUse()
			magicProduced = MagicProduce()
			x = D10()
			if x <= 2:
				final_product = magicProduced + reagentUse + materialUse
			if x > 2 and x < 5:
				final_product = magicProduced*2 + reagentUse + materialUse
			if x >= 5 and x < 8:
				final_product = magicProduced*3 + reagentUse + materialUse
			if x >= 8 and x < 10:
				final_product = magicProduced*4 + reagentUse + materialUse
			if x == 10:
				final_product = magicProduced*5 + reagentUse + materialUse
			ResourceUpdate(2, materialUse)
			ResourceUpdate(4, reagentUse)
			ResourceUpdate(5, magicProduced)
			Product(self.ListingID, final_product)
			VolumeChange(self.ListingID)
			return
		elif self.IndustryID == 6:
			contractProduce = ContractProduce()
			contractFill = ContractFill()
			contractUpdate = contractProduce + contractFill
			ResourceUpdate(6, contractUpdate)
			Listing(10).ContractChange()
			VolumeChange(self.ListingID)
			return
		elif self.IndustryID == 7:
			invest = D5()
			InvestUpdate(self.ListingID, invest)
			VolumeChange(self.ListingID)
			return

		else:
			print "error IndustryID not found"
			return

	# this is where the magic has to happen, buckle up this might get dicy.
	def ValueChange(self):
	# First we are gonna check out the total resource count for the industry for this listing
		x = ResourceCount(self.IndustryID)
		if self.Production < 0:
			self.Production = self.Production*3

		if x >= 20:
			value = self.Production/2
		elif x > 10 and x < 20:
			value = self.Production
		elif x > 0 and x <= 10:
			value = self.Production*2
		elif x <= 0 and x >= -5:
			value = self.Production*3
		elif x < -5 and x > -10:
			value = self.Production*4
		elif x <= -10 and x > -20:
			value = self.Production*5
		elif x <= -20 and x > -30:
			value = self.Production*6
		elif x <= -30:
			value = self.Production*7
		else:
			print "Error"

		ChangeUpdate(self.ListingID, value)

		newValue = self.Price + value

		ValueUpdate(self.ListingID, newValue)
		return




	# This function is for the trade guilds which are going to calculate value a bit differently
	def TradeChange(self):
		# Each trade guild picks an industry to invest in each round We are then going to make $$$ based on how that resource does
		x = ResourceCount(self.InvestID)
		# this is going to get interesting. I want to gain more $$$ based on how close we are to 0, but we want to lose $$$ when we are under 0 on a bell curve. Gonna need some more tweaking.
		if x == 0:
			Delta = .50
		if x > 0 and x <= 5:
			Delta = .20
		if x > 5 and x <= 10:
			Delta = .15
		if x > 10 and x <= 15:
			Delta = .10
		if x > 15:
			Delta = .05
		if x < 0 and x >= -5:
			Delta = -.02
		if x < -5 and x >= -10:
			Delta = -.05
		if x < -10 and x >= -15:
			Delta = -.07
		if x < -15:
			Delta = -.10
		Value = self.Price*Delta
		newValue = self.Price+Value
		ValueUpdate(self.ListingID, newValue)

	# This function is for the assassins guild, we need to calculate their profit based on how many contracts they complete. I am actually thinking, how close the outcome is to zero similar to trade guilds.
	def ContractChange(self):
# First we are going to add contracts for each resource in the negative
		food = ResourceCount(1)
		if food < 0:
			contractDelta = D4()
			ResourceUpdate(6, contractDelta)
		material = ResourceCount(2)
		if material < 0:
			contractDelta = D4()
			ResourceUpdate(6, contractDelta)
		tools = ResourceCount(3)
		if tools < 0:
			contractDelta = D4()
			ResourceUpdate(6, contractDelta)
		reagents = ResourceCount(4)
		if reagents < 0:
			contractDelta = D4()
			ResourceUpdate(6, contractDelta)
		magic = ResourceCount(5)
		if magic < 0:
			contractDelta = D4()
			ResourceUpdate(6, contractDelta)
		x = ResourceCount(6)
		if x >= 20:
			value = -x*4
		elif x > 10 and x < 20:
			value = -x*2
		elif x > 3 and x <= 10:
				value = -x
		elif x <= 3 and x >= -3:
				value = abs(x)*3
		elif x < -3 and x > -10:
			value = abs(x)
		elif x <= -10 and x > -20:
			value = abs(x)/2
		elif x <= -20 and x > -30:
			value = -x
		elif x <= -30:
			value = -x*2
		else:
			print "Error"
		ChangeUpdate(self.ListingID, value)
		newValue = self.Price+value
		ValueUpdate(self.ListingID, newValue)
		return





