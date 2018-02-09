import sys, random, sqlite3

# The following are emulating dice rolls (D5 being the odd man out)

def D4():
	roll = random.randint(1,4)
	return roll

def D5():
	roll = random.randint(1,5)
	return roll

def D6():
	roll = random.randint(1,6)
	return roll

def D8():
	roll = random.randint(1,8)
	return roll

def D10():
	roll = random.randint(1,10)
	return roll
	
def D12():
	roll = random.randint(1,12)
	return roll

def D20():
	roll = random.randint(1,20)
	return roll

def D100():
	roll = random.randint(1,100)
	return roll

# This function creates a DB connection and does some basic error checking.

def Conn():
		try:
			conn = sqlite3.connect('exchange.db')
			return conn
		except Error as e:
			print(e)
		return None

# This function retuns the current resource count from the DB.

def ResourceCount(resource_id):
	resource_Count = 0
	conn = Conn()
	data = conn.execute('SELECT resource_count FROM Resources WHERE resource_id =?', (resource_id,))
	for x in data:
		resource_Count = x[0]
	return resource_Count

# This function finds the current value for a listing Unsure if needed....
def GetValue(listing_id):
	listing_ID = (listing_id)
	conn = Conn()
	data = conn.execute('SELECT listing_price FROM Listings WHERE listing_id =?', listing_ID)
	for x in data:
		value = x[0]
	return value

# The following functions determine resources used, or resources produced per round.

def ToolUse():
	toolUse = -(D4())
	return toolUse

def MaterialUse():
	materialUse = -(D6())
	return materialUse

def FoodUse():
	FoodUse = -(D4())
	return FoodUse

def ReagentUse():
	ReagentUse = -(D8())
	return ReagentUse

def MagicUse():
	MagicUse = 	-(D4())
	return MagicUse

def FoodProduce():
	FoodProduced = D20()
	return FoodProduced

def MaterialProduce():
	MaterialProduce = D6() + D6()
	return MaterialProduce

def ToolProduce():
	ToolProduce = D8() + D8()
	return ToolProduce

def ReagentProduce():
	ReagentProduce = D10() + D10()
	return	ReagentProduce

def MagicProduce():
	MagicProduce = D8()
	return MagicProduce

def ContractProduce():
	ContractProduce = D6()
	return ContractProduce

def ContractFill():
	ContractFill = -(D20())
	return ContractFill

# The following functions are used to update the DB with resources used/created and industry invested in for trade guilds.

def InvestUpdate(listing_id, invest_id):
	conn = Conn()
	cur = conn.cursor()
	invest_id = (invest_id,)
	cur.execute('UPDATE Listings SET listing_investid =? WHERE listing_id =?', invest_id + listing_id)
	conn.commit()
	return

def ResourceUpdate(resource_id, resource_delta):
	resource_count = ResourceCount(resource_id)
	conn = Conn()
	cur = conn.cursor()
	resource_current = resource_count + resource_delta
	resource_current = (resource_current,)
	cur.execute('UPDATE Resources SET resource_count =? WHERE resource_id =?', resource_current + (resource_id,))
	conn.commit()
	resource_count = ResourceCount(resource_id)
	return

def VolumeChange(listing_id):
	volume = (D100(),)
	conn = Conn()
	cur = conn.cursor()
	cur.execute('UPDATE Listings SET listing_volume =? WHERE listing_id =?', volume + listing_id)
	conn.commit()
	return


def Product(listing_id, product_count):
	product_count = (product_count,)
	conn = Conn()
	cur = conn.cursor()
	cur.execute('UPDATE Listings SET listing_production =? WHERE listing_id =?', product_count + listing_id)
	conn.commit()
	return

def ValueUpdate(listing_id, newValue):
	newValue = (newValue,)
	conn = Conn()
	cur = conn.cursor()
	cur.execute('UPDATE Listings SET listing_price =? WHERE listing_id =?', newValue + listing_id)
	conn.commit()
	return

def ChangeUpdate(listing_id, valueDelta):
	valueDelta = (valueDelta,)
	conn = Conn()
	cur = conn.cursor()
	cur.execute('UPDATE Listings SET listing_change =? WHERE listing_id =?', valueDelta + listing_id)
	conn.commit()


def dayStart():
	conn = Conn()
	data = conn.execute('UPDATE Resources SET resource_count = 0')
	conn.commit()
	conn.close()
	return




