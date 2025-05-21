import sys, os
import random
sys.path.append(os.path.join(os.path.dirname(__file__),'..','instance_file'))
from sheet_io import read, write

class Market_Management:
	def __init__(self, profile_dir):
		
		self.companies_json = os.path.join(profile_dir,'market_data','player_market.json')
		self.companies = read(self.companies_json)
	def roll_dice(self):
		dice ={
		"quality":["critical_miss","miss","success","critical_success"],
		"perceived_quality":["critical_miss","miss","success","critical_success"],
		"quantity" :["small","medium","big"]
		}
	
			
		
		a_quality_roll = random.choice(dice["quality"])
		b_quality_roll = random.choice(dice["perceived_quality"])
		quantity_roll = random.choice(dice["quantity"])
			
		return a_quality_roll, b_quality_roll, quantity_roll 
			
			
		
		
	def consumption_loop(self):
		try :
			for company_name, data in self.companies.items():
				a_quality_roll,b_quality_roll, quantity_roll = self.roll_dice()
						
				if a_quality_roll == "critical_miss":
					a_quality = random.randint(-50,-10)
				elif a_quality_roll =="miss":
					a_quality = random.randint(-10,-5)
				elif a_quality_roll =="success":
					a_quality = random.randint(5,10)
				elif a_quality_roll =="critical_success":
					a_quality = random.randint(10,50)
						
				if b_quality_roll == "critical_miss":
					b_quality = random.randint(-50, -10)
				elif b_quality_roll =="miss":
					b_quality = random.randint(-10, -5)
				elif b_quality_roll =="success":
					b_quality = random.randint(5,10)
				elif b_quality_roll =="critical_success":
					b_quality = random.randint(10,50)
				
				if quantity_roll == "small":
					quantity = random.randint(1,5)
				elif quantity_roll =="medium":
					quantity = random.randint(5,10)
				elif quantity_roll =="big":
					quantity = random.randint(10,50)
			
				data["reputation"]["quality"] += a_quality
				data["reputation"]["perceived_quality"] += b_quality
				
				for product_name, product_data in data["prices"].items():
					product_price = product_data["price"]	
				



				data["balance"] += quantity * product_price	
					
			write(self.companies_json,self.companies)
		except Exception as e:
			print(e)
		
#total_product_value = sum(product_data["price"] for product_data in data["prices"].values())
#data["balance"] += quantity * total_product_value				
		
		