import tkinter as tk
from tkinter import ttk
import sv_ttk
from tkinter import filedialog
import json
import threading
from backend import batch_convert_folder
from backend import get_progress

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
    
    def conversion_thread():
        batch_convert_folder(input_folder, output_folder, encoder_settings)
        tk.messagebox.showinfo("Conversion Complete", "FLAC to OPUS conversion is complete.")
    # Create a separate thread for the conversion process
    conversion_thread = threading.Thread(target=conversion_thread)
    conversion_thread.start()
    
def load_config():
    try:
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        # Create an empty config file
        with open(CONFIG_FILE, "w") as config_file:
            config = {}
            json.dump(config, config_file)
        return config

def save_config(config):
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file)

def create_gui():
    config = load_config()
    root = tk.Tk()
    root.title("FLAC to OPUS Converter")
    root.iconbitmap("icon.ico")
    sv_ttk.set_theme("dark")
    
    # region: Sectioning

    # IO section
    io_section = ttk.LabelFrame(root, text="Input/Output", padding=10)
    io_section.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Opus encoder settings section
    opus_settings_frame = ttk.LabelFrame(root, text="Opus Encoder Settings", padding=10)
    opus_settings_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Progress section
    progress_section = ttk.LabelFrame(root, text="Converting Progress", padding=10)
    progress_section.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    
    # endregion
    
    # region: GUI elements

    # Input folder selection
    input_folder_label = ttk.Label(io_section, text="Input Folder:")
    input_folder_label.grid(row=0, column=0, padx=10, pady=5)
    input_folder_entry = ttk.Entry(io_section, width=40)
    input_folder_entry.grid(row=0, column=1, padx=5, pady=5)
    input_folder_button = ttk.Button(io_section, text="Choose Folder", command=lambda: choose_input_folder(input_folder_entry))
    input_folder_button.grid(row=0, column=2, padx=5, pady=5)

    # Output folder selection
    output_folder_label = ttk.Label(io_section, text="Output Folder:")
    output_folder_label.grid(row=1, column=0, padx=10, pady=5)
    output_folder_entry = ttk.Entry(io_section, width=40)
    output_folder_entry.grid(row=1, column=1, padx=5, pady=5)
    output_folder_button = ttk.Button(io_section, text="Choose Folder", command=lambda: choose_output_folder(output_folder_entry))
    output_folder_button.grid(row=1, column=2, padx=5, pady=5)

    # Bitrate mode management radio buttons
    bitrate_mode_var = tk.StringVar(value="vbr")  # Default selection is VBR
    vbr_radio = ttk.Radiobutton(opus_settings_frame, text="VBR", variable=bitrate_mode_var, value="vbr")
    vbr_radio.pack(anchor="w")
    cvbr_radio = ttk.Radiobutton(opus_settings_frame, text="Constrained VBR", variable=bitrate_mode_var, value="cvbr")
    cvbr_radio.pack(anchor="w")
    cbr_radio = ttk.Radiobutton(opus_settings_frame, text="CBR", variable=bitrate_mode_var, value="hard-cbr")
    cbr_radio.pack(anchor="w")

    def on_scale_change(event):
        value = int(bitrate_slider.get())
        step = 8  # Set the desired step size
        adjusted_value = round(value / step) * step
        if adjusted_value > 503:
            adjusted_value = 512
        elif adjusted_value < 16:
            adjusted_value = 8
        if adjusted_value != value:
            bitrate_slider.set(adjusted_value)
            bitrate_value_label.config(text=str(int(bitrate_slider.get())) + " kbps")

    # Bitrate slider
    bitrate_label = ttk.Label(opus_settings_frame, text="Bitrate (kbps):")
    bitrate_label.pack(anchor="w", pady=5)
    
    bitrate_slider = ttk.Scale(opus_settings_frame, from_=8, to=512, orient=tk.HORIZONTAL, length=100)
    bitrate_slider.set(128)  # Default bitrate value
    bitrate_slider.configure(command=on_scale_change)
    bitrate_slider.pack(anchor="w")

    # Bitrate value label
    bitrate_value_label = ttk.Label(opus_settings_frame, text="128 kbps")
    bitrate_value_label.pack(anchor="w")

    # Tune low bitrates dropdown menu
    tune_label = ttk.Label(opus_settings_frame, text="Tune low bitrates for:")
    tune_label.pack(anchor="w", pady=5)
    tune_var = tk.StringVar(value="Auto")  # Default selection is Auto
    tune_dropdown = ttk.OptionMenu(opus_settings_frame, tune_var, "Auto", "Music", "Speech")
    tune_dropdown.pack(anchor="w")
    
    # Progress bar
    progress_bar = ttk.Progressbar(progress_section, length=200, mode="determinate")
    progress_bar.grid(row=0, column=0, padx=10, pady=10)
    progress_bar.pack(pady=5)

    # Progress label
    progress_label = ttk.Label(progress_section, text="0%")
    progress_label.pack()
    
    # Time spent label
    time_label = ttk.Label(progress_section, text="Time Spent:")
    time_label.pack(anchor="w", pady=5)

    # Time spent value label
    time_value_label = ttk.Label(progress_section, text="")
    time_value_label.pack(anchor="w", pady=5)
    
    # endregion
    
    def update_progress(progress_bar, progress_label, time_value_label):
        progress, time_spent = get_progress()
        progress_bar["value"] = progress
        progress_label["text"] = f"{progress:.2f}%"
        time_value_label["text"] = f"{time_spent:.2f} seconds"
        if progress <= 100:
            root.after(100, update_progress, progress_bar, progress_label, time_value_label)
        else:
            # Progress reached 100, exit the function
            update_progress(progress_bar, progress_label, time_value_label)
            
    def reset_timer_and_progress(progress_bar, progress_label, time_value_label):
        progress_bar["value"] = 0
        progress_label["text"] = "0%"
        time_value_label["text"] = "0 seconds"
      
    def save_folders():
        config["input_folder"] = input_folder_entry.get()
        config["output_folder"] = output_folder_entry.get()
        save_config(config)
        
    def convert_button_click_wrapper():
        reset_timer_and_progress(progress_bar, progress_label, time_value_label)
        convert_button_click(input_folder_entry.get(), output_folder_entry.get(), bitrate_mode_var, bitrate_slider, tune_var)
        update_progress(progress_bar, progress_label, time_value_label)
        save_folders()
        reset_timer_and_progress(progress_bar, progress_label, time_value_label)

    if "input_folder" in config:
        input_folder_entry.insert(0, config["input_folder"])
    if "output_folder" in config:
        output_folder_entry.insert(0, config["output_folder"])

    convert_button = ttk.Button(root, text="Convert", command=convert_button_click_wrapper)
    convert_button.grid(row=3, column=0, columnspan=3, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
