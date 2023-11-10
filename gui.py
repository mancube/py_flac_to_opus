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

def convert_button_click(input_folder, output_folder, bitrate_mode_var, bitrate_slider, tune_var):
    # Get Opus encoder settings
    bitrate_mode = bitrate_mode_var.get()
    bitrate = bitrate_slider.get()
    tune = tune_var.get()
    encoder_settings = {
        "bitrate_mode": bitrate_mode,
        "bitrate": bitrate,
        "tune": tune
    }
    
    batch_convert_folder(input_folder, output_folder, encoder_settings)
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

    # Input folder selection
    input_folder_label = tk.Label(root, text="Input Folder:")
    input_folder_label.grid(row=0, column=0, padx=10, pady=5)
    input_folder_entry = tk.Entry(root, width=40)
    input_folder_entry.grid(row=0, column=1, padx=5, pady=5)
    input_folder_button = tk.Button(root, text="Choose Folder", command=lambda: choose_input_folder(input_folder_entry))
    input_folder_button.grid(row=0, column=2, padx=5, pady=5)
    
    # Output folder selection
    output_folder_label = tk.Label(root, text="Output Folder:")
    output_folder_label.grid(row=1, column=0, padx=10, pady=5)
    output_folder_entry = tk.Entry(root, width=40)
    output_folder_entry.grid(row=1, column=1, padx=5, pady=5)
    output_folder_button = tk.Button(root, text="Choose Folder", command=lambda: choose_output_folder(output_folder_entry))
    output_folder_button.grid(row=1, column=2, padx=5, pady=5)
    
    # Opus encoder settings section
    opus_settings_frame = tk.LabelFrame(root, text="Opus Encoder Settings", padx=10, pady=10)
    opus_settings_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
    
    # Bitrate mode management radio buttons
    bitrate_mode_var = tk.StringVar(value="vbr")  # Default selection is VBR
    vbr_radio = tk.Radiobutton(opus_settings_frame, text="VBR", variable=bitrate_mode_var, value="vbr")
    vbr_radio.pack(anchor="w")
    cvbr_radio = tk.Radiobutton(opus_settings_frame, text="Constrained VBR", variable=bitrate_mode_var, value="cvbr")
    cvbr_radio.pack(anchor="w")
    cbr_radio = tk.Radiobutton(opus_settings_frame, text="CBR", variable=bitrate_mode_var, value="hard-cbr")
    cbr_radio.pack(anchor="w")
    
    # Bitrate slider
    bitrate_label = tk.Label(opus_settings_frame, text="Bitrate (kbps):")
    bitrate_label.pack(anchor="w", pady=5)
    bitrate_slider = tk.Scale(opus_settings_frame, from_=8, to=512, orient=tk.HORIZONTAL, resolution=8)
    bitrate_slider.set(128)  # Default bitrate value
    bitrate_slider.pack(anchor="w")
    
    # Tune low bitrates dropdown menu
    tune_label = tk.Label(opus_settings_frame, text="Tune low bitrates for:")
    tune_label.pack(anchor="w", pady=5)
    tune_var = tk.StringVar(value="Auto")  # Default selection is Auto
    tune_dropdown = tk.OptionMenu(opus_settings_frame, tune_var, "Auto", "Music", "Speech")
    tune_dropdown.pack(anchor="w")
    
    if "input_folder" in config:
        input_folder_entry.insert(0, config["input_folder"])
    if "output_folder" in config:
        output_folder_entry.insert(0, config["output_folder"])
    
    def save_folders():
        config["input_folder"] = input_folder_entry.get()
        config["output_folder"] = output_folder_entry.get()
        save_config(config)
    
    convert_button = tk.Button(root, text="Convert", command=lambda: [convert_button_click(
        input_folder_entry.get(), output_folder_entry.get(), bitrate_mode_var, bitrate_slider, tune_var
    ), save_folders()])
    convert_button.grid(row=3, column=0, columnspan=3, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
