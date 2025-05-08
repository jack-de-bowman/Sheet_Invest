import os, sys
import json
import subprocess
import logging
logging.basicConfig(
    filename="game_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


sys.path.append(os.path.join(os.path.dirname(__file__),'..','market_engine'))
from companies_manager import Random_Companies

def boot_game(profile):	
	
	absolute_dir = os.path.dirname(os.path.abspath(__file__))
	profile_dir = os.path.join(absolute_dir, '..','..','data', profile)
	game_path = os.path.join(absolute_dir, 'execute_sheet_invest.py')
	print(profile_dir, game_path)
	try :
		loading_script (profile_dir)
		process = subprocess.run([sys.executable, game_path, profile_dir], 
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE,
			text = True
		)
		print(f"Subprocess output : {process.stdout}")
		print(f"Subprocess Error : {process.stderr}")
	except subprocess.CalledProcessError as e:
		logging.error(f"Game Script Error:{e.stderr}")
		print(f"Game Script Error{e.stderr}")
	except Exception as e:
		print(f"error while booting {e}") 
def loading_script (profile_dir):
	
	random_company_manager = Random_Companies(profile_dir)
	companies_json = os.path.join(profile_dir, 'market_data', 'player_market.json')
	production_json = os.path.join(profile_dir,'market_data','production.json')
	player_portfolio_json = os.path.join(profile_dir, 'player_portfolio.json')	
	
	with open(player_portfolio_json,'r') as file:
		player_portfolio = json.load(file) 
	
	if not "stock_wallet" in player_portfolio:
		player_portfolio = {"stock_wallet":{}}
		with open(player_portfolio_json, 'w') as file:
			json.dump(player_portfolio, file, indent=4)


	try : 
		with open(companies_json, 'r') as file:
			companies_data = json.load(file)
		if not isinstance(companies_data, dict) or "companies" not in companies_data:
			companies_data = {"companies":[]}
	except (FileNotFoundError, json.JSONDecodeError):
		companies_data ={"companies":[]}
	
	companies_number = len(companies_data["companies"])	
	if companies_number < 100 :
		for _ in range(100 - companies_number):
			company_name = random_company_manager.stocks_generator()
			company_production = random_company_manager.production_generator(company_name)
		
		
		
			companies_data["companies"].append({
				"name": company_name,
				"stock_data":{company_name:{"shares_available":1000, "shares_price": random_company_manager.generate_price()}},
				"production_data"  : company_production
				})
		with open(companies_json, 'w') as file:
			json.dump(companies_data, file, indent = 4)
	