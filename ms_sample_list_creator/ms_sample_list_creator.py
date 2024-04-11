# To generate binaries for this script, install pyinstaller (pip install pyinstaller) and run "pyinstaller --onefile main.py"
# Generated binaries are made for the native system where the pyinstaller command is run.

# You can generate windows executable from linux using wine, by previously installing wine, python 3.8.19, pyinstaller and
# other non-built-in packages (here requests) inside wine. Then run: wine pyinstaller --onefile main.py

import tkinter as tk
from home_page import HomeWindow
from new_batch import newBatch
from csv_batch import csvBatch

def submit_results(clicked_button:str):
    home_page.show_values(clicked_button)
    handle_user_choice()

# Function to handle the user choice
def handle_user_choice():
    # Call the manage_choice method to get the user choice
    user_choice = home_page.manage_choice()
    # Show the corresponding window based on the user's choice
    show_selected_window(user_choice)

def show_selected_window(choice):
    if choice == "new":
        # Create a new Toplevel window for the new batch
        new_batch_window = tk.Toplevel(root)
        new_batch_window.title("Create new batch")
        # Show the window for a new batch
        newBatch(new_batch_window, root)
    elif choice == "csv":
        # Create a new Toplevel window for the new batch
        csv_batch_window = tk.Toplevel(root)
        csv_batch_window.minsize(300, 200)
        csv_batch_window.title("Import csv batch")
        # Show the window for a new batch
        csvBatch(csv_batch_window, root)
    else:
        # Handle the case of an unknown choice
        print("Unknown error, please try again with other parameters.")

# Create an instance of the main window
root = tk.Tk()
root.title("Home")
root.minsize(600, 600)

# Create an instance of the HomeWindow class
home_page = HomeWindow(root)

# Display the HomeWindow
home_page.pack()

frame_submit = tk.Frame(root)
frame_submit.pack(pady=(50, 0))

button_new_batch = tk.Button(
frame_submit, text="New sample list", width=20, command=lambda: submit_results("new"))
button_new_batch.pack(side="left")

button_submit_csv = tk.Button(
frame_submit, text="Sample list from CSV", width=20, command=lambda: submit_results("csv"))
button_submit_csv.pack(side="right")

# Start the tkinter event loop
root.mainloop()

