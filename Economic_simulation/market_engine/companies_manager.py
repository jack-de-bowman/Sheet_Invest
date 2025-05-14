
import sys, os
import json
import random	
sys.path.append(os.path.join(os.path.dirname(__file__),'..','instance_file'))

class Random_Companies : #Generation class for creating and or managing new companies.
	min_rand_companies = 100
	def __init__(self):
		self.absolute_dir = os.path.dirname(os.path.abspath(__file__))
	
		
	
		self.production_file = os.path.join(self.absolute_dir,'..','var_fetching','production.json')
	
		
		with open(self.production_file, 'r') as file:
			self.fetched_production = json.load(file)
		self.production()
	def production(self):
		keys, values = self.get_keys_and_values(self.fetched_production["services"])
		print(keys)
	
	def get_keys_and_values(self, dict_name): #helper method to extract keys
		keys= []
		values = []
		parent_key = ''
		for key, value in dict_name.items():
			full_key = f"{parent_key}.{key}"if parent_key else key
			if isinstance(value, dict):
				nested_data = self.get_keys_and_values(value)
				keys.extend(nested_data[0]) 
				values.extend(nested_data[1])
			elif isinstance(value, list):
				keys.append(full_key)
				values.append((full_key, value))
			else:
				keys.append(full_key)
				values.append((full_key, [value]))
		
		return keys, values
if __name__ == "__main__":
	Random_Companies()	
	
		
	

	
