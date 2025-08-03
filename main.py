import tkinter as tk
from tkinter import ttk

from rubber_spot import rubber_spot
from rubber_stain import rubber_stain
from rubber_tear import rubber_tear

class App(tk.Tk):
    def __init__(self):
      super().__init__()
      self.title("Gloves Defects Detection System")
      self.resizable(False, False)
      self.geometry("250x250")
      self.create_widgets()
      
    def create_widgets(self):
        self.frame = tk.Frame(self)
        self.frame.pack()
        
        # Glove Type Label
        self.glove_type_label = tk.Label(
            self.frame,
            text='Glove Type',
            anchor='w',
            )
        self.glove_type_label.pack(padx = 5, pady = 5)
        
        # Glove Type Options
        glove_type = ["Rubber"]
        self.glove_type_value = tk.StringVar()
        self.glove_type_option = ttk.Combobox(
            self.frame,
            textvariable = self.glove_type_value,
            values = glove_type,
            state= "readonly"
        )
        self.glove_type_option.set("--Select Glove Type--")
        self.glove_type_option.bind("<<ComboboxSelected>>", self.update_defect_options)
        self.glove_type_option.pack(padx = 5, pady = 5)
        
        # Defects Label
        self.defects_label = tk.Label(
            self.frame,
            text='Defect',
            anchor='w'
            )
        self.defects_label.pack(padx = 5, pady = 5)
        
        # Defects Options
        self.defects = {
            "Rubber": ["Spot", "Stain", "Tear"]
        }
        self.defects_value = tk.StringVar()
        self.defects_option = ttk.Combobox(
            self.frame,
            textvariable = self.defects_value,
            values = self.defects,
            state= "readonly"
        )
        self.defects_option.set("--Select Defect--")
        self.defects_option.pack(padx = 5, pady = 5)
        
        # Select Button
        button = tk.Button(self.frame, text ="Select", command = self.get_defect_list)
        button.pack(padx = 5, pady = 5)
     
    # Function to update defect option when glove type option is selected   
    def update_defect_options(self, event):
        selected_glove_type = self.glove_type_option.get()
        self.defects_option['values'] = self.defects[selected_glove_type]
        self.defects_option.set("--Select Defect--")
    
    
    def get_defect_list(self):
        selected_glove_type = self.glove_type_option.get()
        selected_defect = self.defects_option.get()
        print(f"Selected Glove Type: {selected_glove_type}\nSelected Defect: {selected_defect}")
        
        if selected_glove_type == "Rubber":
            if selected_defect == "Spot":
                rubber_spot()
            elif selected_defect == "Stain":
                rubber_stain()
            elif selected_defect == "Tear":
                rubber_tear()
            else:
                return

app = App()
app.mainloop()