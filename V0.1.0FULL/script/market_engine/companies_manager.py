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
    def production_json_structure(self): #Build 05-05-2025
        for key, values in self.production_json.items():
            if key == "services":
                if len(key) >= 3:
                    sector = list(values.keys())[0]
                    method_category = list(values.keys())[1]
                    category = list(values.keys())[2]
                    if len(values) == 4:
                        subcategory = list(values.keys())[3] 
                        theme = values.get(subcategory, {})
                    else :
                        theme = values.get(category, {})
            elif key == "products":
                if len(key) >= 2 :
                    sector = list(values.keys())[0]
                    product = values.get(sector,{})
        return (sector, product, method_category, method, category, subcategory, theme)
    def generate_production(self):
   
        choose_random = random.choice(self.production_json_structure())
        
        product_sector = choose_random["products"] 
        service_sector = choose_random["services"]
        product = choose_random.get(product)
        method_category = choose_random.get(method_category)
        method = choose_random.get(method)
        category = choose_random.get(category)
        subcategory = choose_random.get(subcategory)
        theme = choose_random.get(theme)
         
        product_dict ={
        sector:{product:{"price": 0, "storage":0}}
        }
        if not subcategory:
            structure = {category:[theme]}
        else :
            structure = {category:{subcategory:[theme]}}
        service_dict ={
        service_sector:{method_category:{method:{structure}}
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
	
