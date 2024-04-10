import tkinter as tk
import os
from tkinter import ttk
from typing import Any, Optional
import csv
from datetime import datetime

import requests

class newBatch:
    def __init__(self, root: tk.Tk, csv_path: str):
        """
        Initializes an instance of the class.

        Args:
            root(tk.Tk): The parent widget or window where this frame will be placed.
            csv_path(str): CSV path and name.

        Returns:
            None
        """
        print("new batch")

        self.root = root

        # Bind the destroy event to the callback function
        self.root.protocol("WM_DELETE_WINDOW", self.back_to_main)

        self.operator = str(os.environ.get("OPERATOR"))
        self.ms_id = str(os.environ.get("MS_ID"))
        self.col_rack_size = int(str(os.environ.get("COL_RACK_NUMBER")))
        self.row_rack_size = int(str(os.environ.get("ROW_RACK_NUMBER")))
        self.pre_blk = int(str(os.environ.get("PRE_BLK")))
        self.post_blk = int(str(os.environ.get("POST_BLK")))
        self.blk_name = str(os.environ.get("BLK_NAME"))
        self.blk_pos = str(os.environ.get("LK_POS"))
        self.inj_volume = int(str(os.environ.get("INJ_VOLUME")))
        self.access_token = str(os.environ.get("ACCESS_TOKEN"))
        self.method_file = str(os.environ.get("METHOD_FILE"))
        self.data_path = str(os.environ.get("DATA_FOLDER"))
        self.standby_file = str(os.environ.get("STANDBY_FILE"))
        self.csv_path = csv_path
        self.current_position = 1
        self.current_row = 1
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M")

        # Create Treeview widget
        self.tree = ttk.Treeview(
            root,
            columns=(
                "aliquot_id",
                "operator",
                "ms_id",
                "File Name",
                "Path",
                "Instrument Method",
                "Position",
                "Inj Vol",
            ),
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("aliquot_id", text="aliquot_id")
        self.tree.heading("operator", text="operator")
        self.tree.heading("ms_id", text="ms_id")
        self.tree.heading("File Name", text="File Name")
        self.tree.heading("Path", text="Path")
        self.tree.heading("Instrument Method", text="Instrument Method")
        self.tree.heading("Position", text="Position")
        self.tree.heading("Inj Vol", text="Inj Vol")

        # Bind Enter key to add row
        self.root.bind("<Return>", self.add_row)

        # Entry widgets for data input
        self.aliquot_id_entry = ttk.Entry(root)

        # Error text hidden:
        self.label = ttk.Label(root, text="")
        self.label.grid(row=2, column=0, columnspan=2, pady=10)

        # Submit button
        submit_button = ttk.Button(root, text="Generate sample list", width=17, command=self.submit_table)

        button_back = tk.Button(root, text="Back to Home", width=17, command=self.back_to_main)

        # Grid layout for widgets
        self.tree.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.aliquot_id_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        submit_button.grid(row=3, column=1, columnspan=2, pady=10)
        button_back.grid(row=4, column=1, columnspan=2, pady=10)

        # Start the Tkinter event loop
        self.root.mainloop()

    def back_to_main(self):
        import home_page
        # Destroy Window 2 and show the main page
        home_page.HomeWindow.deiconify(self)
        self.root.destroy()
        

    def add_row(self, event: Optional[tk.Event] = None) -> None:
        """
        Adds a sample to the list when enter key is pressed.

        Args:
            event (Optional[tk.Event]): The event triggering the function (optional).

        Returns:
            None
        """

        # Get data from entry widgets
        aliquot_id = self.aliquot_id_entry.get()

        # Check if aliquot_id is not empty
        if not aliquot_id:
            # Display an error message
            self.label.config(text="aliquot id can't be empty!", foreground="red")
            return

        parts = str(self.method_file).split("/")
        file = parts[-1]

        # Placeholder calculations for other columns
        filename = self.timestamp + "_" + str(self.operator) + "_" + aliquot_id
        path = self.data_path.replace("/", "\\")
        instrument_method = self.method_file.replace("/", "\\")
        inj_volume = self.inj_volume

        # Send data to directus
        base_url = "http://directus.dbgi.org"
        collection_url = base_url + "/items/Mass_Spectrometry_Analysis"
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {self.access_token}"})

        # Add headers
        headers = {"Content-Type": "application/json"}

        data = {
            "aliquot_id": aliquot_id,
            "mass_spec_id": filename,
            "ms_id": self.ms_id,
            "injection_volume": inj_volume,
            "injection_method": file,
        }

        response = session.post(url=collection_url, headers=headers, json=data)

        self.label.config(text="")

        if response.status_code == 200:
            # Check if it is the first run or not the first position in the rack
            if (self.current_position > self.col_rack_size and self.current_position > self.col_rack_size) or (
                self.current_position == 1 and self.current_row == 1
            ):
                # Open window to ask prefix
                ask_prefix_window = tk.Toplevel(self.root)
                ask_prefix_window.title("Add Prefix")
                self.ask_box = AskBoxPrefixWindow(ask_prefix_window)
                self.ask_box.pack()

                # Make CsvWindow wait for AskBoxPrefixWindow result
                ask_prefix_window.transient(self.root)
                ask_prefix_window.wait_window(self.ask_box)

            prefix = os.environ.get("PREFIX")
            alphabet_letter = chr(ord("A") + self.current_row - 1)
            position = f"{prefix}{alphabet_letter}{self.current_position}"

            # Update position and box for the next row
            self.current_position += 1
            if self.current_position > self.col_rack_size:
                self.current_position = 1
                self.current_row += 1

            # Check if the rack is full
            if self.current_row > self.row_rack_size:
                self.current_position = 1
                self.current_row = 1

            # display success message
            self.label.config(text="Correctly added!", foreground="green")
            # Insert data into Treeview
            item_id = self.tree.insert(
                "",
                "end",
                values=(aliquot_id, self.operator, self.ms_id, filename, path, instrument_method, position, inj_volume),
            )

            # Scroll to the last added row
            self.tree.see(item_id)

            # Clear entry widgets
            self.aliquot_id_entry.delete(0, "end")

        # Catches forbidden access when token is expired and generates a new token
        elif response.status_code == 401:
            self.directus_reconnect()
        else:
            self.label.config(text="Directus error, check your entry!", foreground="red")

    def submit_table(self) -> None:
        """
        Converts the entered data to a CSV.

        Args:
            None

        Returns:
            None
        """
        # Get all items from the Treeview
        all_items = self.tree.get_children()
        # Check if there are any rows to export
        if not all_items:
            self.label.config(text="No data to export!", foreground="red")
            return

        # Extract data from the Treeview
        raw_data = [self.tree.item(item, "values")[3:] for item in all_items]  # Skip the first two elements
        data_to_export = sorted(raw_data, key=blanks_first)
        print(data_to_export)

        # Write data to the CSV file
        with open(self.csv_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write headers
            csv_writer.writerow(["Bracket Type=4", "", "", "", ""])
            csv_writer.writerow(["File Name", "Path", "Instrument Method", "Position", "Inj Vol"])

            # Write pre blanks
            if self.pre_blk > 0:
                for i in range(1, self.pre_blk + 1):
                    padded_number = str(i).zfill(2)
                    filename = (
                        self.timestamp + "_" + self.operator + "_dbgi_" + self.blk_name + "_blk_pre" + padded_number
                    )
                    path = self.data_path.replace("/", "\\")
                    instrument_method = self.method_file.replace("/", "\\")
                    position = self.blk_pos
                    inj_volume = self.inj_volume
                    csv_writer.writerow([filename, path, instrument_method, position, inj_volume])
            else:
                print("no pre blanks")

            # Write data
            csv_writer.writerows(data_to_export)

            # Write post blanks
            if self.post_blk > 0:
                for i in range(1, self.post_blk + 1):
                    padded_number = str(i).zfill(2)
                    filename = (
                        self.timestamp + "_" + self.operator + "_dbgi_" + self.blk_name + "_blk_post" + padded_number
                    )
                    path = self.data_path.replace("/", "\\")
                    instrument_method = self.method_file.replace("/", "\\")
                    position = self.blk_pos
                    inj_volume = self.inj_volume
                    csv_writer.writerow([filename, path, instrument_method, position, inj_volume])
            else:
                print("no post blanks")

            # Write standby line
            parts = self.standby_file.split("/")
            file = parts[-1]
            filename = self.timestamp + "_" + self.operator + "_" + file
            path = self.data_path.replace("/", "\\")
            standby = self.standby_file.replace("/", "\\")
            position = self.blk_pos
            inj_volume = self.inj_volume
            csv_writer.writerow([filename, path, standby, position, inj_volume])

        # Close the Tkinter window
        self.root.destroy()

    def directus_reconnect(self) -> None:
        """
        Directus tokens have a validity of 15 minutes. If directus returns an unauthorized response,
        it could be due to the token expiration. So this function tries a reconnexion to generate a new access token.

        Args:
            None

        Returns:
            None
        """
        username = os.environ.get("USERNAME")
        password = os.environ.get("PASSWORD")

        # Define the Directus base URL
        base_url = "http://directus.dbgi.org"

        # Define the login endpoint URL
        login_url = base_url + "/auth/login"
        # Create a session object for making requests
        session = requests.Session()
        # Send a POST request to the login endpoint
        response = session.post(login_url, json={"email": username, "password": password})

        if response.status_code == 200:
            data = response.json()["data"]
            self.access_token = data["access_token"]
            self.root.event_generate("<Return>")

        else:
            # Display error statement
            self.label.config(text="Reconnexion to directus failed", foreground="red")

    # Permits to sort the samples and put the blanks at the beginning


def blanks_first(item: Any) -> Any:
    """
    Detects blanks and puts them first in the list.

    Args:
        item (str): The item to be analyzed.

    Returns:
        Tuple[int, str]: A tuple containing a priority value and the sample ID.
    """

    # Extract the sample ID from the file name
    sample_id = item[0].split("_")[3]
    # Check if the sample ID contains 'batch'
    if sample_id.startswith("batch"):
        return (0, sample_id)  # If yes, put it in first place
    else:
        return (1, sample_id)  # Else, put it after


class AskBoxPrefixWindow(tk.Frame):
    def __init__(self, root: tk.Toplevel):
        """
        Initializes an instance of the class.

        Args:
            root(tk.Toplevel): The parent widget or window where this frame will be placed.
            csv_path(str): CSV path and name.

        Returns:
            None
        """
        tk.Frame.__init__(self, root)

        self.prefix = tk.StringVar()

        # Adjust the window size
        root.geometry("300x150")

        # Label + textbox to enter prefix
        label_prefix = tk.Label(self, text="Box's prefix:")
        label_prefix.pack()

        entry_prefix = tk.Entry(self, textvariable=self.prefix)
        entry_prefix.pack()

        # Submit button
        button_submit = tk.Button(self, text="Submit", command=self.store_prefix)
        button_submit.pack()

    def store_prefix(self) -> None:
        """
        Puts the asked prefix to the environment.

        Args:
            None

        Returns:
            None
        """
        os.environ["PREFIX"] = self.prefix.get()

        # Close the AskBoxPrefixWindow
        self.master.destroy()