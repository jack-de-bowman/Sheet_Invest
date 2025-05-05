import sys, os
import json
import random


class Random_Companies :
	min_rand_companies = 100
	def __init__(self, profile_dir):
		self.profile_dir = profile_dir 
		self.absolute_dir = os.path.dirname(os.path.abspath(__file__))
	def generator(self):
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
			
		random_companies = [{self.generate_name():{"shares_available": 10000,"shares_price": self.generate_price()}}
		for _ in range(Random_Companies.min_rand_companies - amount_companies)]		
		
		companies.extend(random_companies)
		with open(companies_path, 'w') as file:
			json.dump({"companies":companies}, file, indent = 4)
		return companies 
	def generate_company_production(self):
		default_company_production_dict: 
		{"company_name":
		 {"sector":{
			 "method_category":{
				 "method_type":{
					 "category":{
						 "subcategory":{
							 ,
				 	}
				 }
			 }
		    
		     {"subcategory":[],
		          "theme":[]}}
		 	}
		 }	   
		 }
		  
	
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
	
