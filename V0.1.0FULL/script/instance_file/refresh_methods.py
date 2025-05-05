import tkinter as tk
import sys, os

class GAME_LOOP:
	def __init__(self, root, stock_market_manager):
		self.root = root
		self.stock_market_manager = stock_market_manager 
		
	def fluctuation_loop(self):
		self.stock_market_manager.price_fluctuation()
		self.root.after(5000, self.fluctuation_loop)
	def refresh_ui(self, main_hub):
		main_hub.update_labels()
		self.root.after(5000, lambda: self.refresh_ui(main_hub))
