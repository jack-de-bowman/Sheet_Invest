import sys, os
import json
import random				




class Random_Companies :
	min_rand_companies = 100
	def __init__(self, profile_dir):
		self.profile_dir = profile_dir 
		self.absolute_dir = os.path.dirname(os.path.abspath(__file__))
		self.production_generator()
	def stocks_generator(self):
		companies_path = os.path.join(self.profile_dir, 'market_data','player_market.json')
		if not os.path.exists(companies_path):
			raise FileNotFoundError(f"File not found :{companies_path}")
		else:
			with open(companies_path, 'r') as file:
				try:
					data = json.load(file)
					if not isinstance(data, dict):
						raise TypeError(f"Expected 'companies' to be a list but got {type(data)} instead")
					companies = data.get("companies",[])
					
				except json.JSONDecodeError as e:
					raise ValueError(f"Invalid JSON in {companies_path} :{e}")
		amount_companies = len(companies)
		if amount_companies >= Random_Companies.min_rand_companies:
			return companies
		
		
		for _ in range(Random_Companies.min_rand_companies - amount_companies):
			random_companies = [{self.generate_name():{"shares_available": 10000,"shares_price": self.generate_price()}}]
			companies.extend(random_companies)
			
		with open(companies_path, 'w') as file:
					json.dump({"companies":companies}, file, indent = 4)
		return companies 
	def production_generator(self):
		production_path = os.path.join(self.profile_dir,'market_data', 'production.json')
		
		random_production_choice = random.choice(self.generate_production())
		print(random_production_choice)
		random_production = [{self.generate_name():random_production_choice}]
	def production_json_structure(self): #Build 05-05-2025
		production_file = os.path.join(self.absolute_dir,'..','var_fetching','production.json')
		with open(production_file,'r') as file:
			self.production_json = json.load(file)
		print(self.production_json)
		sector, product, method_category, method, category, subcategory, theme = None, None, None, None, None, None, None
		for key, values in self.production_json.items():
			if isinstance(values, dict):
				sub_keys = list(values.keys())
			else:
				sub_keys = values 
			if key == "services":
					for service_key, service_values in self.production_json.get("services",{}).items():
						if isinstance(service_values, dict):
							sector = list(values.keys())[0]
							method_category = list(values.keys())[1]
							method = list(values.keys())[2]
							category = list(values.keys())[3]
							if len(values) == 5:
								subcategory = list(values.keys())[4]
								theme = values.get(subcategory, {})
							else :
								theme = values.get(category, {})
			elif key == "products":
				for category, items in self.production_json.get("products",{}).items():
						if isinstance(items, list):
							for product in items:
								
								if len(values) >= 2 :
									sector = list(values.keys())[0]
									product = values.get(sector,{})
			monetization_methods = self.production_json.get("monetization", [])
			for method in monetization_methods:
				print(f"Monetization Type: {method}")

		return (sector, product, method_category, method, category, subcategory, theme)
	def generate_production(self):
		production_data = self.production_json_structure()
		sector, product, method_category, method, category, subcategory, theme = production_data

		
		choose_random = random.choice(list(production_data))
		
		product_sector = choose_random[0] 
		service_sector = choose_random[1]
		
		product_dict ={
		product_sector:{product:{"price": 0, "storage":0}}
		}
		if not subcategory:
			structure = {category:[theme]}
		else :
			structure = {category:{subcategory:[theme]}}
		service_dict ={
			service_sector:{
				method_category:{method:{structure}}}
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
	
