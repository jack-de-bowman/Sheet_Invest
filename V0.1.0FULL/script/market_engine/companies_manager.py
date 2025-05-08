
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
		self.production_path = os.path.join(self.profile_dir,'market_data', 'production.json')
		production_file = os.path.join(self.absolute_dir,'..','var_fetching','production.json')
		#-READ-#
		self.player_companies_stock = read(self.companies_path)
		self.production_json = read(production_file)
	def check_data(self):
		amount_companies = len(self.player_companies_stock)
		if amount_companies < Random_Companies.min_rand_companies:
			for _ in range(Random_Companies.min_rand_companies - amount_companies):
				company_name = self.stocks_generator()
				self.production_generator(company_name)
		else:
			print("Companies related files are full")
	
	
	
	def stocks_generator(self):
		try:
			with open(self.companies_path, 'r') as file:
				data = json.load(file)
			self.player_companies_stock = data.get("companies", [])
		except (FileNotFoundError, json.JSONDecodeError):
			self.player_companies_stock = []

		company_name = self.generate_name()
		random_company= {
			"name":company_name,
			"stock_data":{"shares_available": 10000,"shares_price": self.generate_price()}}
		self.player_companies_stock.append(random_company)
		
		with open(self.companies_path, 'w') as file:
			json.dump({"companies":self.player_companies_stock}, file, indent = 4)
		return company_name
	def production_generator(self, company_name):
		product_dict, service_dict = self.generate_production()
		random_production_choice = random.choice([product_dict, service_dict])
		for company in self.player_companies_stock:
			if company["name"] == company_name:
				company["production_data"] = random_production_choice
		with open(self.companies_path, 'w') as file:
			json.dump({"companies": self.player_companies_stock}, file, indent=4)
		with open(self.production_path, 'w') as file:
			json.dump({"production": self.player_companies_stock}, file, indent=4)
		return random_production_choice
	
	def production_json_structure(self): #Build 07-05-2025
		
		sector, product, method_category, method, category, subcategory, theme = None, None, None, None, None, None, None
		for key, values in self.production_json.items():
			if key == "products":
				for sector, items in  values.items():
					if isinstance(items, list):
						product = items
					else:
						
						print(f"Error: Expected a list in 'products', got {type(items)}")


			elif key == "services":
				for service_key, service_values in values.items():
					if isinstance(service_values, dict):
						keys = list(service_values.keys())
						if len(keys) >= 4:
							sector, method_category, method, category = keys[:4]
							subcategory = keys[4] if len(keys) == 5 else None
							theme = service_values.get(subcategory or category, {})
							if not isinstance(theme, dict):
								theme = {}
		monetization_methods = self.production_json.get("monetization", [])
		for method in monetization_methods:
			print(f"Monetization Type: {method}")

		return sector, product, method_category, method, category, subcategory, theme
	def generate_production(self):
		production_data = self.production_json_structure()
		sector, product, method_category, method, category, subcategory, theme = production_data
		if isinstance(product, list):
			product = random.choice(product) if product else "Unknown"
		product_sector = sector if sector else "Unknown"
		service_sector = method_category if method_category else "Unknown"
		
		
		product_dict ={
		product_sector:{product:{"price": self.generate_price(), "storage":random.randint(500,1000)}}}
	
		structure = {category: {subcategory: theme if theme else {}}}
	
		service_dict ={
			service_sector:{method_category:{method:structure}}
			}
		return product_dict, service_dict
		
		  
		
	def generate_name(self):
		random_companies_path = os.path.join(self.absolute_dir, '..','var_fetching','random_companies.json')
		with open(random_companies_path, 'r') as file:
			random_companies_data = json.load(file)
		
		first_compound = random.choice(random_companies_data.get("first_compound", ["Generic"]))
		first_adjective = random.choice(random_companies_data.get("first_adjective", ["Other_Generic"]))
		return f"{first_compound} {first_adjective}"
	def generate_price(self):
		cheap_price = round(random.uniform(0.05, 10),2)
		standard_price = round(random.uniform(10, 100),2)
		expensive_price = round(random.uniform(100, 1000),2)
		
		return random.choice([cheap_price,standard_price, expensive_price])
	
