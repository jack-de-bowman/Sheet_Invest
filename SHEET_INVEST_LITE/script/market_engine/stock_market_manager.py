import sys
import os
import json
import random
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'instance_file'))
from sheet_io import write, read

logging.basicConfig(
	level= logging.INFO,
	format = '%(asctime)s - %(levelname)s - %(message)s',
	handlers = [
		logging.FileHandler("app.log"),
		logging.StreamHandler()
		]
	)
	

class Stock_Market_Manager:
	def __init__(self, profile_dir, player_data):
		#STRING#
		self.profile_dir = profile_dir 
		#DICTIONARIES#
		self.save_info, self.portfolio, self.companies = player_data
		#PATH#
		self.player_stock_market_json = os.path.join(self.profile_dir, 'market_data', 'player_market.json')
		self.player_portfolio_json = os.path.join(self.profile_dir, 'player_portfolio.json')
		self.player_info_json = os.path.join(self.profile_dir, 'player_info.json')
		#--#
		self.player_info = read(self.player_info_json)
		self.portfolio = read(self.player_portfolio_json)
		self.companies = read(self.player_stock_market_json)
	

	#helper method
	def find_company(self, company_name):
		return self.companies.get(company_name)

	def buy_share(self, share):
		
		company_data = self.find_company(share)
		if company_data is None:
			logging.error(f"No data{share}")
			return
		share_available = company_data["stock_data"]["shares_available"]
		share_price = company_data["stock_data"]["shares_price"]
	
						
		if share_available > 0:
			if share not in self.portfolio["stock_wallet"]:
				self.portfolio["stock_wallet"][share] = {"quantity":0, "profit":0.0} 
				
			
			company_data["stock_data"]["shares_available"] -= 1
			self.portfolio["stock_wallet"][share]["quantity"] += 1
			self.portfolio["stock_wallet"][share]["profit"] += share_price 
			self.player_info["balance"] -= share_price
			print(f"Portfolio After Purchase: {self.portfolio}")
			print(f"Balance After Purchase: {self.player_info['balance']}")

			write(self.player_stock_market_json, self.companies)
			write(self.player_portfolio_json, self.portfolio)
			write(self.player_info_json, self.player_info)
			
	
	def sell_share(self, share):
		
			company_data = self.find_company(share)
		
			
			share_amount = self.portfolio["stock_wallet"][share]["quantity"]
			if share_amount >= 1:
					share_price = company_data["stock_data"]["shares_price"]
					
					self.portfolio["stock_wallet"][share]["quantity"] -= 1
					self.portfolio["stock_wallet"][share]["profit"] -= share_price
					self.player_info["balance"] += share_price
					company_data["stock_data"]["shares_available"] += 1
					write(self.player_stock_market_json, self.companies)
					write(self.player_portfolio_json, self.portfolio)
					write(self.player_info_json, self.player_info)

			else :
				del self.portfolio["stock_wallet"][share]
				write(self.player_portfolio_json, self.portfolio)
			
			
	"""
	def calculate_profit(self):
		try:	
			
			
			total_profit = 0
			remove_share =[]
			for share_name, share_data in self.portfolio["stock_wallet"].items():
				share_amount = share_data.get('quantity',0)
				total_spent = share_data.get('profit',0)
				if share_amount == 0:
					remove_share.append(share_name)
					continue

				current_price = next(
				(company[share_name]["stock_data"]["shares_price"] for company in self.companies if share_name in company), None)
				if current_price is None:
					logging.error(f"Missing stock for {share_name}")
					continue
				profit = (share_amount * current_price) - total_spent
				total_profit += profit
				self.portfolio["stock_wallet"][share_name]["profit"] = round(profit, 2)
		
			for share_name in remove_share:
				self.portfolio["stock_wallet"].pop(share_name)		
					
			write(self.player_portfolio_json,self.portfolio)	
			
		except KeyError as e:
			logging.error(f"Key error while calculating profit for {share_name},:{e}")
			print(e)
		except Exception as e:
			logging.error(f"Unexpected error while calculating profit:{e}")
			print(e)
	"""
	def price_fluctuation(self):
		max_fluctuation = 10
		min_fluctuation = -10
		for company_name, company_data in self.companies.items():
			share_price = company_data["stock_data"]["shares_price"]
			random_fluctuation = round(random.uniform(min_fluctuation, max_fluctuation),2)
			share_price = round(max(0, share_price + random_fluctuation),2)
			company_data["stock_data"]["shares_price"] = share_price
		write(self.player_stock_market_json, self.companies)
		
	
		