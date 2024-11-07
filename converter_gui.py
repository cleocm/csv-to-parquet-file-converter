# import tkinter module 
import tkinter as tk
from tkinter import * 
from tkinter import filedialog 
from tkinter import messagebox
from pathlib import Path    
from PIL import Image, ImageTk 
import subprocess
import sys

# Create Object
root = tk.Tk() 
root.geometry("551x390")
root.title("CSV to Parquet Converter")  

script_directory = Path(__file__).parent
ASSETS_PATH = script_directory / "assets" / "frame0"
target_script = script_directory / "csv_to_parquet.py"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def upload_csv():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="Select a CSV File"
    )
    if file_path:
        # Temporarily enable the entry widget to update the text
        file_path_entry.config(state="normal")
        file_path_entry.delete(0, END)  # Clear any existing text
        file_path_entry.insert(0, file_path)  # Insert the file path into the entry widget
        file_path_entry.config(state="disabled")  # Disable the entry widget again

def convert_to_parquet():
    # Get the file path from the entry widget
    file_path = file_path_entry.get()
    
    # Ensure the file path is not empty
    if file_path and file_path != "No file selected":
        # Call an external script (e.g., 'csv_to_parquet.py') with the file path as an argument
        result = subprocess.run([sys.executable, str(target_script), file_path], capture_output=True, text=True)

        if result.returncode == 0:
            # Display the pop-up with the result (parquet file path)
            messagebox.showinfo("Conversion Complete", f"File successfully converted to: {result.stdout}")
        else:
            # Display error message if the conversion fails
            messagebox.showerror("Error", "An error occurred while converting the file.")
    else:
        print("No CSV file selected.")


image = PhotoImage(file=relative_to_assets("image_2.png"))
image_label = tk.Label(root, image=image)

# Load image with Pillow
pil_image = Image.open(relative_to_assets("button_1.png"))
button_image_1 = ImageTk.PhotoImage(pil_image)

pil_image = Image.open(relative_to_assets("button_2.png"))
button_image_2 = ImageTk.PhotoImage(pil_image)

upload_btn = Button(root, text = 'Upload CSV File', 
                command = upload_csv,
                image=button_image_1,
                borderwidth=0,
                highlightthickness=0,) 

convert_btn = Button(root, text = 'Convert to Parquet', 
                command = convert_to_parquet,
                image=button_image_2,
                borderwidth=0,
                highlightthickness=0,)

text_label = Label(root, text="Uploaded File:", fg="#596281",
    font=("ABeeZee", 15 * -1))

file_path_entry = Entry(root, width=50, font=("ABeeZee", 12))
file_path_entry.insert(0, "No file selected")  # Placeholder text
file_path_entry.config(state="disabled")  # Make the entry read-only


# Set the position of button on the top of window 
image_label.pack(pady=(30,10))
upload_btn.pack(pady=10)    
text_label.pack(pady=(20,10))
file_path_entry.pack(pady=(5,10))
convert_btn.pack(pady=(20,30))


root.mainloop() 