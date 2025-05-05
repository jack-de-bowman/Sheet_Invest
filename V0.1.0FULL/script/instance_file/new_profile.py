import sys, os 
import json 

class CreateProfile : 
	def __init__(self, profilename):
		self.profilename = profilename
		self.absolute_dir = os.path.dirname(os.path.abspath(__file__))
		self.profile_dir = os.path.join(self.absolute_dir, '..','..', 'data', f"{self.profilename}")
		self.setup_profile()
	
	def fetch_data(self):
			
		#-"player_info are "general":{name, reputation}, "contracts":{}, "stats":{} etc...-#
		default_player_info_fetch = os.path.join(self.absolute_dir,'..', 'var_fetching', 'default_player_info.json')
		with open(default_player_info_fetch, 'r') as file:
			default_player_info = json.load(file)


		default_save_data_fetch = os.path.join(self.absolute_dir,'..', 'var_fetching', 'default_save_data.json')
		with open(default_save_data_fetch, 'r') as file:
			default_save_data = json.load(file)
	
		return default_save_data, default_player_info

	def setup_profile(self):
		
		
		#Create the profile directory
		if not os.path.exists(self.profile_dir):
			os.makedirs(self.profile_dir)
		#Create the market directory (files not directly used by player in game)
		market_dir = os.path.join(self.profile_dir, 'market_data')
		if not os.path.exists(market_dir):
			os.makedirs(market_dir)
				
		def json_create(file_path, data):
			with open(file_path,'w') as destination:
				json.dump(data, destination, indent = 4)
		
		default_save_data, default_player_info = self.fetch_data()
		#Create profile_data folder into profile_directory
		json_create(os.path.join(self.profile_dir, f'{self.profilename}_save_data.json'),default_save_data)
		json_create(os.path.join(self.profile_dir, 'player_info.json'), default_player_info)
		json_create(os.path.join(self.profile_dir, 'player_portfolio.json'),{})
		json_create(os.path.join(market_dir, 'player_market.json'), {})
	
				
if __name__ == "__main__" :
	CreateProfile()
		