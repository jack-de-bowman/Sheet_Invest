import os, sys
import json
import tkinter as tk

sys.path.append(os.path.join(os.path.dirname(__file__),'..','market_engine'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..','..','interface'))

from sheet_io import read, write
from companies_manager import Random_Companies
from market import Market_Management
from stock_market_manager import Stock_Market_Manager
from player_hub import Main_Hub 

class Refresh_Class:
	def __init__(self, stock_market_manager,market_manager, main_hub, root):
		self.root = root
		self.stock_market_manager = stock_market_manager
		self.market_manager = market_manager
		self.main_hub = main_hub
		
		self.refresh_stock_market()
		self.refresh_interface()
	def refresh_market(self):
		self.market_manager.consumption_loop()
		
	def refresh_stock_market(self):
		self.stock_market_manager.price_fluctuation()
		self.stock_market_manager.calculate_profit()
		self.root.after(5000, self.refresh_stock_market)
		
	def refresh_interface(self):
		self.main_hub.update_price_labels()
		self.main_hub.player_portfolio()
		self.root.after(5000, self.refresh_interface)


def main():
	print("main method as launched")
		#ENSURE THAT PROFILE_DIR AS FOR STRING THE USER PROFILENAME AS THE PLAYER CHOOSEN PROFILE.
	try:    
		if len(sys.argv)  < 2 :       
			print("No profile dir")
			return
		profile_dir = sys.argv[1]
		profile_dir = os.path.join(profile_dir)
	
	
	
	
		root = tk.Tk()
		### - READ AND WRITE METHODS ARE FOUND WITHIN INSTANCE_FILE/SHEET.IO.py  .
		### - SELF EXPLICATIVE ## P.S : U DONT TOUCH IT !
		
		#-PATH TO USE FOR READ/WRITE-#
		player_market_json 	= os.path.join(profile_dir,'market_data', 'player_market.json')
		save_info_json 		= os.path.join(profile_dir,'player_info.json')
		player_portfolio_json 	= os.path.join(profile_dir,'player_portfolio.json')
		
		#PORTFOLIO IS A DICTIONNARY
		#COMPANIES IS DICTIONNARIES NESTED IN A LIST.
		portfolio 		= read(player_portfolio_json)
		companies    		= read(player_market_json)
		
		try:
			portfolio = read(player_portfolio_json)
			if not "stock_wallet" in portfolio:
				portfolio = {"stock_wallet":{}}
		except (FileNotFoundError, json.JSONDecodeError) as e:
			print(f"Error loading portfolio: {e}")
			portfolio = {"stock_wallet": {}}  # Default empty structure

		try:
			companies = read(player_market_json)
		except (FileNotFoundError, json.JSONDecodeError) as e:
			print(f"Error loading market data: {e}")
			companies = {}  # Default empty company list

		#-#
	
	
		
		
		
		#-#
		save_info = read(save_info_json)
		#--#
		
		player_data = (save_info, portfolio, companies)
		#--#
		stock_market_manager = Stock_Market_Manager(profile_dir, player_data)
		
		companies_manager = Random_Companies(profile_dir)
		market_manager = Market_Management(profile_dir)
		main_hub = Main_Hub(root, profile_dir, player_data, stock_market_manager)
		refresh_loop = Refresh_Class(stock_market_manager,market_manager, main_hub, root)
		root.mainloop()	
		#--#
	except Exception as e:
		print(f"ERROR 2 : {e}")	



if __name__ == "__main__":
	main()

