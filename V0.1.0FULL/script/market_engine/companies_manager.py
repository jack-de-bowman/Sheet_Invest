
import sys, os
import json
import random	
sys.path.append(os.path.join(os.path.dirname(__file__),'..','instance_file'))
from sheet_io import read, write

class Random_Companies : #Generation class for creating and or managing new companies.
	min_rand_companies = 100
	def __init__(self, profile_dir):
		self.profile_dir = profile_dir 
		self.absolute_dir = os.path.dirname(os.path.abspath(__file__))
	
		
		#-PATH-#
		self.companies_path = os.path.join(self.profile_dir,'market_data','player_market.json')
		self.production_file = os.path.join(self.absolute_dir,'..','var_fetching','production.json')
		#-READ-#
		self.random_name_json= os.path.join(self.absolute_dir, '..','var_fetching','random_companies.json')
		self.fetched_random_name = read(self.random_name_json)
		self.player_companies = read(self.companies_path)
		self.fetched_production = read(self.production_file)
	def get_keys_and_values(self, dict_name, parent_key =""): #helper method to extract keys
		keys= []
		values = []

		
		for key, value in dict_name.items():
			full_key = f"{parent_key}.{key}"if parent_key else key
			
			if isinstance(value, dict):
				nested_data = self.get_keys_and_values(value, full_key)
				keys.extend(nested_data[0]) 
				values.extend(nested_data[1])
			elif isinstance(value, list):
				keys.append(full_key)
				values.append((full_key, value))
			else:
				keys.append(full_key)
				values.append((full_key, [value]))
		
		return keys, values
		
	def extract_production_data(self):
		keys, values = self.get_keys_and_values(self.fetched_production["services"])
		print(keys)
	def create_market_data(self):
		self.extract_production_data()
		
		amount_companies = len(self.player_companies)
		company_name = self.generate_name()
		if amount_companies < Random_Companies.min_rand_companies:
				for _ in range(Random_Companies.min_rand_companies - amount_companies):
					company_name = self.generate_name()
					while company_name in self.player_companies:
						company_name = self.generate_name()
                

					stock_data = self.stocks_generator()	
					random_production_choice = random.choice([product_dict, service_dict])
					market_companies = {}
				
					self.player_companies[company_name] ={
					"stock_data":stock_data,
					"production_data":random_production_choice}
			
				with open(self.companies_path, 'w') as file:
					json.dump(self.player_companies, file, indent =4)
		
				
				  
		
	def generate_name(self):
	
		first_compound = random.choice(self.fetched_random_name.get("first_compound", ["Generic"]))
		first_adjective = random.choice(self.fetched_random_name.get("first_adjective", ["Other_Generic"]))
		return f"{first_compound} {first_adjective}"
	def generate_price(self):
		cheap_price = round(random.uniform(0.05, 10),2)
		standard_price = round(random.uniform(10, 100),2)
		expensive_price = round(random.uniform(100, 1000),2)
		
		return random.choice([cheap_price,standard_price, expensive_price])
	
	
	def stocks_generator(self):
		stock_data= {"shares_available": 10000,"shares_price": self.generate_price()}
		return stock_data

	
