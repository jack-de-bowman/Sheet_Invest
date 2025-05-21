import json
def read(file_path):
	try:
		with open(file_path, 'r') as source:
			data = json.load(source)
		return data
	except FileNotFoundError:
		print(f"file not found{file_path}")
		return {}
	except json.JSONDecodeError as e :
		print(f"Decode erorr: {file_path}")
		return {}

def write(file_path, data):
	with open(file_path, 'w') as destination:
		json.dump(data, destination, indent=4)