import tkinter as tk

from devtool_script import Sheet_Extract


class DEV_TOOL:
	def __init__(self, root):
		self.root = root 
		self.main_frame = tk.Frame(root)
		self.main_frame.grid()
		self.sheet_extract = Sheet_Extract
		
	
	def select_a_file(self):
		file_select_button =t k.Button(self.main_frame,
		text ="PLEASE SELECT A FOLDER", command = self.sheet_extract.file_selection())
		)
		file_select_button.grid()
		
	def confirm_selected_file(self, filepath):
		confirmation_toplevel = tk.Toplevel(self.root)
		confirmation_toplevel.grid()
		
		
		confirmation_textVar = {f"DO YOU CONFIRM THAT {filepath}IS THE CORRECT FILE YOU WANT TO OPEN?"}
		warning_textVar = {f"IT IS SUGGESTED TO BE CAREFULL AND CHOSE PERSONAL PROJECT OR TO LIMIT THE SIZE OF FILE YOU WANT TO OPEN TO LESS THEN 1GB"}
		
		confirmation_text = tk.Text(confirmation_toplevel, textVar = confirmation_textVar)
		confirmation_text.grid()
		
		warning_text = tk.Text(confirmation_toplevel, textVar = warning_textVar)
		warning_text.grid()
		
		
		
		yes_button = tk.Button(confirmation_toplevel, text = "YES")
		yes_button.grid()
		
		no_button = tk.Button(confirmation_toplevel, text = "NO")
		no_button.grid()
		
		filter_choice_textVar = {f"By Using the filter option you can manually chose which specific files by type or by selection within{filepath}"}  
		filter_choice_text =tk.Text(confirmation_toplevel, textVar = filter_choice_textVar)
		filter_choice_text.grid()
		
		filter_choice_button = tk.Button(confirmation_toplevel, text = "USE FILTER TOOL")
		filter_choice_button.grid()
		
	
	def specific_files_to_extract(self):
		for folder, files in selected_folder_content.items():
			files_list_widgets: 
			
		
		
		

		

	def auto_frame_constructor(self):
		
		
		
		

if __name__ == "__main__":
	root = tk.Tk()
	
	DEV_TOOL()
	root.mainloop()
	