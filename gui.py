import tkinter as tk
from tkinter import filedialog
import json
from backend import batch_convert_folder

CONFIG_FILE = "config.json"

def choose_input_folder(entry):
    folder = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder)

def choose_output_folder(entry):
    folder = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder)

def convert_button_click(input_folder, output_folder):
    batch_convert_folder(input_folder, output_folder)
    tk.messagebox.showinfo("Conversion Complete", "FLAC to OPUS conversion is complete.")
    
def load_config():
    try:
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file)

def create_gui():
    config = load_config()
    
    root = tk.Tk()
    root.title("FLAC to OPUS Converter")

    input_folder_label = tk.Label(root, text="Input Folder:")
    input_folder_label.grid(row=0, column=0, padx=10, pady=5)

    input_folder_entry = tk.Entry(root, width=40)
    input_folder_entry.grid(row=0, column=1, padx=5, pady=5)

    input_folder_button = tk.Button(root, text="Choose Folder", command=lambda: choose_input_folder(input_folder_entry))
    input_folder_button.grid(row=0, column=2, padx=5, pady=5)

    output_folder_label = tk.Label(root, text="Output Folder:")
    output_folder_label.grid(row=1, column=0, padx=10, pady=5)

    output_folder_entry = tk.Entry(root, width=40)
    output_folder_entry.grid(row=1, column=1, padx=5, pady=5)

    output_folder_button = tk.Button(root, text="Choose Folder", command=lambda: choose_output_folder(output_folder_entry))
    output_folder_button.grid(row=1, column=2, padx=5, pady=5)
    
    if "input_folder" in config:
        input_folder_entry.insert(0, config["input_folder"])
    if "output_folder" in config:
        output_folder_entry.insert(0, config["output_folder"])
        
    def save_folders():
        config["input_folder"] = input_folder_entry.get()
        config["output_folder"] = output_folder_entry.get()
        save_config(config)

    convert_button = tk.Button(root, text="Convert", command=lambda: [convert_button_click(
        input_folder_entry.get(), output_folder_entry.get()
    ), save_folders()])
    convert_button.grid(row=3, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
