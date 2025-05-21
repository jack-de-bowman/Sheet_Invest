class Population :
	def __init__(self):
		self.population = 1000
	def population_data_management(self):
		gender = random.choice(["m","f"])
		economic_group = random.choice(["sub","min","avg","ab_avg","aff"])
		identifier = random.choice(1,1000)
		
		
		
		random_id = f"{gender}_{economic_group}_{identifier}" #Early Build without economic distribution
		return random_id
		
	def economic_group(self):
		subminimal_consumer = {
		"population":self.population / 5,
		"daily_wallet":{min:0, max:5},
		"monthly_wallet":150
		}
		minimal_consumer = {
		"population": self.population / 10,
		"daily_wallet":{min:5, max:10},
		"monthly_wallet":300
		}
		average_consumer = {
		"population": self.population /2.5,
		"daily_wallet":{min:10, max:20},
		"monthly_wallet":600
		}
		
		above_average_consumer = {
		"population": self.population/5,
		"daily_wallet":{min:20,max:100},
		"monthly_wallet":3000
		}
		
		affluent_consumer = {
		"population": self.population /10,
		"daily_wallet":{min:100,max:200},
		"monthly_wallet":6000
		}
	
	def reset_population_wallet(self):
	def product_priority_management(self):
		
	
		priority = 0
		for company in companies:
			for product, values in company["production_data"].items():
		
		if "food" in company:
			priority = 100
			price_of_satisfaction = "placeholder"
			true_balance = (price_of_satisfaction - ["monthly_wallet"])
			
		if "entertainment" in company:
			priority = 75
			
		
	
		
		
			
	
	def population_spending(self):
		companies = self.companies 
		population = self.population_data
		for seller, seller_info in companies.items():
			seller_sector = "placeholder"
			seller_product ="placeholder"
			seller_product_price = [seller_product]["price"]
			
		for buyer, buyer_info in population.items():
			buyer_need = {"list of need and the quantity they want at that moment"}
			bought_quantity = [][]
			
			if seller_product in buyer_need:
				transaction = {
				"company" : seller,
				"client_need":seller_product,
				"for":buyer}
			
			buyer_true_balance -= seller_product_price
			seller_balance += seller_product_price * bought_quantity
			seller_inventory -= bought_quantity
			# CALL THE METHOD TO INCREASE THE PRICE OF THE STOCKS
				
			
		
		
class Sheet_City:
	def __init__(self):