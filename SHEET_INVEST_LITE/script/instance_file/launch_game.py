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
	random_company_generator = Random_Companies(profile_dir)
	random_company_generator.create_market_data()
	



	