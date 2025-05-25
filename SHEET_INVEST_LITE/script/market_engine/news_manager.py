import sys, os
import json
import collections 
sys.path.append(os.path.join(os.path.dirname(__file__),'..','instance_file'))
from sheet_io import read, write

class Stock_Price_News:
	def __init__(self, profile_dir):
		self.profile_dir = profile_dir 
		self.price_index_json = os.path.join(self.profile_dir,'market_data','price_index.json')
			
		raw_price_index = read(self.price_index_json) or {}
		self.price_index = {
		company: collections.deque(prices, maxlen=5) for company, prices in raw_price_index.items()
		}


	def create_price_index(self):
		
		

		self.companies = read(os.path.join(self.profile_dir, 'market_data', 'player_market.json'))  

		for company, data in self.companies.items():
			current_price = data["stock_data"]["shares_price"]
			print(f"New Price for {company}: {current_price}")


			if company not in self.price_index:
				self.price_index[company] = collections.deque([], maxlen=5)
			self.price_index[company].append(current_price)

		price_index_save = {company:list(prices) for company, prices in self.price_index.items()}
		write(self.price_index_json, price_index_save)  
		
	

	def calculate_index(self):
		percent_changes = {}
		
		for company, prices in self.price_index.items():
			if len(prices) < 2:
				percent_changes[company] = 0
				
				continue 
				
			oldest_price = prices[0]
			newest_price = prices[-1]
			
			update_percent = ((newest_price - oldest_price) / oldest_price) * 100 if oldest_price else 0
			percent_changes[company] = update_percent
		print(percent_changes)
		return percent_changes
		
		
			
			
			
			
			
			
			
			
		
		
	