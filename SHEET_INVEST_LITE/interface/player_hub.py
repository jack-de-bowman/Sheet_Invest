import tkinter as tk
import sys, os
import string 
import logging 
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..','script','instance_file'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..','script', 'market_engine'))
from stock_market_manager import Stock_Market_Manager 
from sheet_io import read, write

class ScrollableFrame(tk.Frame):
	def __init__(self, container):
		super().__init__(container)
		
		canvas = tk.Canvas(self)
		self.scrollable_frame = tk.Frame(canvas)
		
		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: canvas.configure(
			scrollregion = canvas.bbox("all")
			)
		)
		
		self.canvas_window = canvas.create_window((0, 0), window= self.scrollable_frame)
		canvas.grid()
		
		
class Main_Hub : 
	def __init__(self, root, profile_dir, player_data, stock_market_manager):
		self.root = root
		self.profile_dir = profile_dir
		print(profile_dir)
		self.stock_market_manager = stock_market_manager
		#-PATH-#
		self.portfolio_json = os.path.join(self.profile_dir,'player_portfolio.json')
		self.market_json = os.path.join(self.profile_dir,'market_data','player_market.json')
		#-Getting read data from main-#
		self.save_info, self.portfolio, self.companies = player_data
		
		#MAIN_FRAME IS THE WINDOW, WITHIN THE WINDOW IS EVERYTHING ELSE
		self.main_frame = tk.Frame(root)
		self.main_frame.grid()
		self.main_frame.grid_columnconfigure(0, weight =1)
		self.main_frame.grid_columnconfigure(1, weight =1)
		#CREATE "CHILD" FRAME OF THE MAIN_FRAME
		self.frames = self.frames_organize()
		self.stock_scroll_frame = ScrollableFrame(self.frames["stock_market_frame"])
		self.portfolio_scroll_frame = ScrollableFrame(self.frames["player_portfolio_frame"])
		self.companies = read(self.market_json)
		self.player_info_frame()
		self.price_labels = {}   ### rename it 
	
		self.create_stock_market()
		self.portfolio_labels = {}
		self.player_portfolio()
		self.update_price_labels()
		
	
	
	def frames_organize(self):
			
		frames_dict = {
		"menu_frame" : {"parent": self.main_frame, "row" : 0, "column":0 },
		"stock_market_frame":{"parent":self.main_frame, "row":2, "column" : 1}, 
		"player_portfolio_frame":{"parent":self.main_frame, "row" : 2, "column" :2, "sticky": 'n'},
		"player_info_frame":{"parent":self.main_frame,"row":1, "column":0},
		"news_frame":{"parent":self.main_frame,"row":3,"column":0},
		}
		
		
		return self.construct_frames(frames_dict)

	def construct_frames(self, frames_dict):
		
		created_frames = {}
		for frame_name, options in frames_dict.items():
			parent =  options.pop("parent")
			grid_options = {k: options.pop(k) for k in ["row", "column", "sticky"] if k in options}
			frame = tk.Frame(parent, **options)
			frame.grid(**grid_options)
			created_frames[frame_name] = frame
		return created_frames 
		
	def news_frame(self, percent_change):
		if not hasattr(self, "news_canvas") or not self.news_canvas:
			self.news_canvas = tk.Canvas(self.frames["news_frame"], width = 200)
			self.news_canvas.grid()
		if hasattr(self, "percent_labels"):
			for label in self.percent_labels:
				label.destroy()
		self.news_canvas.delete("all")
		self.news_canvas.update()
		self.percent_change = percent_change
		self.percent_labels = []
		
		for company, percent in self.percent_change.items():
			percent_change_label = tk.Label(self.news_canvas, text = f"{company}{round(percent,2)}")
			percent_change_label.grid()
			self.percent_labels.append(percent_change_label)
	
	def player_info_frame(self):
		frame = tk.Frame(self.frames["player_info_frame"])
		frame.grid(row = 0, rowspan = 2)
		
		player_balance_label = tk.Label(frame, text = f"{self.save_info['balance']}$")
		player_balance_label.grid(row = 0, column = 0,rowspan = 2)

	###STOCK_MARRKE & PORTFOLIO
		
	def stock_on_mouse_wheel(self, event):
		self.stock_canvas.yview_scroll(-1 * int(event.delta/120),"units")
	def portfolio_on_mouse_wheel(self, event):
		self.portfolio_canvas.yview_scroll(-1 * int(event.delta/120),"units")
	
	def update_price_labels(self):
		if not hasattr(self, "price_labels"):
			return
		self.companies = read(self.market_json)
		for share_name, share_data in self.companies.items():	
			if share_name in self.price_labels:
				current_price = f"{share_data['stock_data']['shares_price']}$"
				self.stock_canvas.itemconfig(self.price_labels[share_name], text = current_price)
		self.root.after(5000, self.update_price_labels)
	
	def create_stock_market(self):
		if not hasattr(self, "stock_canvas") or not self.stock_canvas:
			self.stock_canvas = tk.Canvas(self.frames["stock_market_frame"], width = 220)
			self.stock_canvas.grid(column = 0, sticky = "NSEW")
		
		
		with open(self.market_json, 'r') as file:
			companies = json.load(file)
			
		### CALCULATE THE NUMBERS OF STRING ITEMS AND ADDITION IT TO THE Y_OFFSET
		y_offset = 0
		
		for share_name, share_data in self.companies.items():	
			if share_name in self.price_labels:
					
				current_price = f"{share_data['stock_data']['shares_price']}$"
				self.stock_canvas.itemconfig(self.price_labels[share_name], text = current_price)
			else:
				self.stock_canvas.create_text(2, y_offset + 1, text = f"{share_name}", anchor = 'w')
				price_label = self.stock_canvas.create_text(190, y_offset, text = f"{share_data['stock_data']['shares_price']}$", anchor ='e')
				self.price_labels[share_name] = price_label
					
				buy_button = tk.Button(self.frames["stock_market_frame"],text=f"Buy", command = lambda cn = share_name:self.stock_market_manager.buy_share(cn))
				self.stock_canvas.create_window(205, y_offset + 1, window = buy_button)
				y_offset +=25
		self.stock_canvas.config(scrollregion = self.stock_canvas.bbox("all"))
		self.stock_canvas.bind("<MouseWheel>", self.stock_on_mouse_wheel)
		self.frames["stock_market_frame"].grid_columnconfigure(0, weight = 1)
	def player_portfolio(self):
		if not hasattr(self, "portfolio_canvas") or not self.portfolio_canvas:
			self.portfolio_canvas = tk.Canvas(self.frames["player_portfolio_frame"], width = 300, height= 100)
			self.portfolio_canvas.grid(column = 1, sticky = 'n')
	
		
		if not hasattr(self, "portfolio_labels"):
			self.portfolio_labels = {}
		
		
		with open(self.portfolio_json, 'r') as file:
			portfolio = json.load(file)	
		y_offset = 0
		for share_name, share_data in portfolio["stock_wallet"].items():
			share_profit = share_data["profit"]
			share_owned_amount = share_data["quantity"]
			if share_name in self.portfolio_labels:
				self.portfolio_canvas.itemconfig(
				self.portfolio_labels[share_name]["profit_on_share_label"], text = share_profit)
				self.portfolio_canvas.itemconfig(
				self.portfolio_labels[share_name]["share_owned_amount_label"],text = share_owned_amount)
			
				
			elif share_owned_amount > 0:
				share_name_label = self.portfolio_canvas.create_text(2, y_offset +1, text = share_name, anchor = 'w')	
				share_owned_amount_label = self.portfolio_canvas.create_text(130, y_offset +1, text = share_owned_amount, anchor = 'e')
				profit_on_share_label = self.portfolio_canvas.create_text(170, y_offset+ 1, text = share_profit, anchor ='w')
				sell_share_button = tk.Button(self.frames["player_portfolio_frame"], text = "SELL", 
				command = lambda s = share_name : self.stock_market_manager.sell_share(s))
				
				self.portfolio_canvas.create_window(230, y_offset, window = sell_share_button)
			
				
				self.portfolio_labels[share_name] ={
				"share_name_label":share_name_label, 
				"share_owned_amount_label" : share_owned_amount_label, 
				"profit_on_share_label":profit_on_share_label,
				"sell_share_button":sell_share_button
				}	
			y_offset += 20		
				
		existing_shares = set(portfolio["stock_wallet"].keys())
		for share_name in list(self.portfolio_labels.keys()):
			if share_name not in existing_shares or 'quantity' == 0:
				self.portfolio_canvas.delete(self.portfolio_labels[share_name]['share_name_label'])
				self.portfolio_canvas.delete(self.portfolio_labels[share_name]['share_owned_amount_label'])
				self.portfolio_canvas.delete(self.portfolio_labels[share_name]['profit_on_share_label'])
				self.portfolio_labels[share_name]['sell_share_button'].destroy()		
				del self.portfolio_labels[share_name]
	
		self.frames["player_portfolio_frame"].grid_columnconfigure(1, weight =1)
		self.portfolio_canvas.config(scrollregion = self.portfolio_canvas.bbox("all"))
		self.portfolio_canvas.bind("<MouseWheel>", self.portfolio_on_mouse_wheel)
	
		
		

	
		
if __name__ == "__main__": 
	root = tk.Tk() 
	main_hub = Main_Hub(root, profile_dir, player_data, stock_market_manager) 
	root.title("SHEET INVESTOR HUB") 
	root.mainloop()
