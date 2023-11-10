import tkinter as tk
from tkinter import filedialog
from backend import batch_convert_folder

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

def create_gui():
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

    convert_button = tk.Button(root, text="Convert", command=lambda: convert_button_click(
        input_folder_entry.get(), output_folder_entry.get()
    ))
    convert_button.grid(row=3, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
