import sys, os
import tkinter as tk 

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'script','instance_file'))
from launch_game import boot_game
from new_profile import CreateProfile


class Sheet_Launcher:
	def __init__(self, root, profile_dir):
		self.absolute_dir = os.path.dirname(os.path.abspath(__file__))
		self.root = root 
		self.profile_dir = profile_dir
		self.boot_game = boot_game
		self._frame_()
		self.ui_create_profile()
		self.ui_profile_list()
	def _frame_(self):
		self.main_frame = tk.Frame(self.root)
		self.profilelist_frame = tk.Frame(self.main_frame)
		self.createprofile_frame = tk.Frame(self.main_frame)
		
		self.main_frame.grid()
		self.profilelist_frame.grid()
		self.createprofile_frame.grid()
	
	def get_profile(self): # fetch the profile folder name to use in the ui.
		data_dir = os.path.join(self.absolute_dir, '..', 'data')
		return [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))] 
	
	def ui_create_profile(self):
		self.new_profile_entry = tk.Entry(self.createprofile_frame)
		self.new_profile_entry.bind("<Return>", lambda event : self.create_profile()) 
		#get on transform to profilename
		
		self.gamemode_list = tk.Listbox(self.createprofile_frame)
		self.new_profile_entry.grid()
		self.gamemode_list.grid()
		
	def create_profile(self):
		profilename = self.new_profile_entry.get()
		CreateProfile(profilename)
	def ui_profile_list(self):
		#RESETS PROFILE BUTTONS WHEN NEW PROFILE 
		for widget in self.profilelist_frame.winfo_children():
			widget.destroy()
		profiles = self.get_profile()
		#LIST OF BUTTONS TO LAUNCH GAME INSTANCE
		for profile in profiles : 
			profile_button = tk.Button(self.profilelist_frame,
			text = profile,
			command = lambda p = profile : self.launch_game(p))
			profile_button.grid()
		self.root.after(5000, self.ui_profile_list)
	def launch_game(self, profile):
		print(f"{profile} is supposedly launched")
		self.boot_game(profile)
if  __name__=="__main__"  : 	
	root = tk.Tk()
	launcher = Sheet_Launcher(root, sys.argv[1] if len(sys.argv) > 1 else "")
	root.title("SHEET INVEST LAUNCHER")
	root.mainloop()