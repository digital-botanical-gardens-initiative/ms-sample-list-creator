# To generate binaries for this script, install pyinstaller (pip install pyinstaller) and run "pyinstaller --onefile main.py"
# Generated binaries are made for the native system where the pyinstaller command is run.

# You can generate windows executable from linux using wine, by previously installing wine, python 3.8.19, pyinstaller and
# other non-built-in packages (here requests) inside wine. Then run: wine pyinstaller --onefile main.py

import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from typing import Any
import new_batch
import csv_batch

import requests


class HomeWindow(tk.Frame):
    def __init__(self, parent: tk.Widget, *args: Any, **kwargs: Any):
        """
        Initializes an instance of the class.

        Args:
            parent (tk.Widget): The parent widget or window where this frame will be placed.
            *args: Additional positional arguments that may be passed to the parent class constructor (optional).
            **kwargs: Additional keyword arguments that may be passed to the parent class constructor (optional).

        Returns:
            None
        """

        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a variable to store the entered text
        self.username = tk.StringVar(None)
        self.password = tk.StringVar(None)
        self.operator = tk.StringVar(None)
        self.ms_id = tk.StringVar(None)
        self.col_rack_number = tk.IntVar(None)
        self.row_rack_number = tk.IntVar(None)
        self.pre_blk = tk.IntVar(None)
        self.post_blk = tk.IntVar(None)
        self.blk_name = tk.StringVar(None)
        self.blk_pos = tk.StringVar(None)
        self.inj_volume = tk.IntVar(None)

        self.label = tk.Label(self, text="Connect to directus and adjust the parameters")
        self.label.pack()

        # Create text entry fields
        frame_labels_up = tk.Frame(self)
        frame_labels_up.pack(fill="x", pady=(5, 0))

        label_username = tk.Label(frame_labels_up, text="Directus username:")
        label_username.pack(side="left", padx=15, anchor="center")
        label_password = tk.Label(frame_labels_up, text="Directus password:")
        label_password.pack(side="right", padx=(0, 20), anchor="center")

        frame_entries_up = tk.Frame(self)
        frame_entries_up.pack(fill="x", pady=5)

        entry_username = tk.Entry(frame_entries_up, textvariable=self.username)
        entry_username.pack(side="left", anchor="center")
        entry_password = tk.Entry(frame_entries_up, textvariable=self.password, show="*")
        entry_password.pack(side="right", anchor="center")

        frame_labels_om = tk.Frame(self)
        frame_labels_om.pack(fill="x", pady=(5, 0))

        label_operator = tk.Label(frame_labels_om, text="Operator's initials:")
        label_operator.pack(side="left", padx=18, anchor="center")

        label_ms = tk.Label(frame_labels_om, text="Mass spectrometer ID:")
        label_ms.pack(side="right", padx=(0, 7), anchor="center")

        frame_entries_om = tk.Frame(self)
        frame_entries_om.pack(fill="x", pady=(5, 0))

        entry_operator = tk.Entry(frame_entries_om, textvariable=self.operator)
        entry_operator.pack(side="left", anchor="center")

        entry_ms = tk.Entry(frame_entries_om, textvariable=self.ms_id)
        entry_ms.pack(side="right", anchor="center")

        frame_label_rack = tk.Frame(self)
        frame_label_rack.pack(fill="x", pady=(5, 0))

        label_col_rack_number = tk.Label(frame_label_rack, text="Rack size (columns x rows)")
        label_col_rack_number.pack(side="bottom", anchor="center")

        frame_entries_rack = tk.Frame(self)
        frame_entries_rack.pack(fill="x", pady=(5, 0))

        entry_col_rack_number = tk.Entry(frame_entries_rack, textvariable=self.col_rack_number)
        self.col_rack_number.set(9)
        entry_col_rack_number.pack(side="left", anchor="center")

        label_x = tk.Label(frame_entries_rack, text="x")
        label_x.pack(side="left", padx=40, anchor="center")

        entry_row_rack_number = tk.Entry(frame_entries_rack, textvariable=self.row_rack_number)
        self.row_rack_number.set(6)
        entry_row_rack_number.pack(side="right", anchor="center")

        frame_labels_blk = tk.Frame(self)
        frame_labels_blk.pack(fill="x", pady=(5, 0))

        label_pre_blk = tk.Label(frame_labels_blk, text="Blanks before samples:")
        label_pre_blk.pack(side="left", padx=4, anchor="center")

        label_post_blk = tk.Label(frame_labels_blk, 
        text="Blanks after samples:")
        label_post_blk.pack(side="right", padx=(0, 8), anchor="center")

        frame_entries_blk = tk.Frame(self)
        frame_entries_blk.pack(fill="x", pady=(5, 0))

        entry_pre_blk = tk.Entry(frame_entries_blk, textvariable=self.pre_blk)
        self.pre_blk.set(4)
        entry_pre_blk.pack(side="left", anchor="center")

        entry_post_blk = tk.Entry(frame_entries_blk, textvariable=self.post_blk)
        self.post_blk.set(3)
        entry_post_blk.pack(side="right", anchor="center")

        frame_labels_np = tk.Frame(self)
        frame_labels_np.pack(fill="x", pady=(5, 0))

        label_blk_name = tk.Label(frame_labels_np, text="Blank name:")
        label_blk_name.pack(side="left", padx=40, anchor="center")

        label_blk_pos = tk.Label(frame_labels_np, text="Blank position:")
        label_blk_pos.pack(side="right", padx=(0, 30), anchor="center")

        frame_entries_np = tk.Frame(self)
        frame_entries_np.pack(fill="x", pady=(5, 0))

        entry_blk_name = tk.Entry(frame_entries_np, textvariable=self.blk_name)
        self.blk_name.set("mapp")
        entry_blk_name.pack(side="left", anchor="center")

        entry_blk_pos = tk.Entry(frame_entries_np, textvariable=self.blk_pos)
        self.blk_pos.set("B:F1")
        entry_blk_pos.pack(side="right", anchor="center")

        frame_labels_pv = tk.Frame(self)
        frame_labels_pv.pack(fill="x", pady=(5, 0))

        label_inj_volume = tk.Label(frame_labels_pv, text="Injection volume (µL):")
        label_inj_volume.pack(side="left", anchor="center", padx=5)

        label_data_path = tk.Label(frame_labels_pv, text="MS data directory")
        label_data_path.pack(side="right", padx=(0, 25), anchor="center")

        frame_entries_pv = tk.Frame(self)
        frame_entries_pv.pack(fill="x", pady=(5, 0))

        entry_inj_volume = tk.Entry(frame_entries_pv, textvariable=self.inj_volume)
        self.inj_volume.set(2)
        entry_inj_volume.pack(side="left")

        self.data_path_button = tk.Button(frame_entries_pv, text="output", width=17, command=self.data_folder)
        self.data_path_button.pack(side="right", padx=1, anchor="center")

        frame_label_methods = tk.Frame(self)
        frame_label_methods.pack(fill="x", pady=(5, 0))

        label_method_path = tk.Label(frame_label_methods, text="Method file:")
        label_method_path.pack(side="left", padx=40, anchor="center")

        label_standby = tk.Label(frame_label_methods, text="Standby method file: ")
        label_standby.pack(side="right", padx=(0, 10), anchor="center")

        frame_entries_methods = tk.Frame(self)
        frame_entries_methods.pack(fill="x", pady=(5, 0))

        self.method_path_button = tk.Button(frame_entries_methods, text="method", width=17, command=self.method_file)
        self.method_path_button.pack(side="left", padx=1, anchor="center")

        self.standby_path_button = tk.Button(frame_entries_methods, text="method", width=17, command=self.standby_file)
        self.standby_path_button.pack(side="right", anchor="center", padx=(0, 1))

        frame_label_output = tk.Frame(self)
        frame_label_output.pack(pady=(5, 0))

        label_output_path = tk.Label(frame_label_output, text="Sample list output directory: ")
        label_output_path.pack(side="right")

        frame_entry_output = tk.Frame(self)
        frame_entry_output.pack(pady=(5, 0))

        self.output_path_button = tk.Button(frame_entry_output, text="output", width=17, command=self.output_folder)
        self.output_path_button.pack(side="right", padx=(0, 1), anchor="center")

        frame_submit = tk.Frame(self)
        frame_submit.pack(pady=(50, 0))

        button_new_batch = tk.Button(frame_submit, text="New sample list", width=20, command=lambda: self.show_values(clicked_button="new"))
        button_new_batch.pack(side="left")

        button_submit_csv = tk.Button(frame_submit, text="Sample list from CSV", width=20, command=lambda: self.show_values(clicked_button="csv"))
        button_submit_csv.pack(side="right")

    def method_file(self) -> None:
        """
        Asks the user to choose the injection method file he wants to use.

        Args:
            None

        Returns:
            None
        """
        method_file = filedialog.askopenfilename(filetypes=[("methods", "*.meth")]).split(".")[0]
        if method_file:
            os.environ["METHOD_FILE"] = method_file
            parts = method_file.split("/")
            self.file = parts[-1]
            self.method_path_button.config(text=self.file)

    def data_folder(self) -> None:
        """
        Asks the user to choose the data folder where MS data will be stored.

        Args:
            None

        Returns:
            None
        """

        data_folder = filedialog.askdirectory()
        if data_folder:
            os.environ["DATA_FOLDER"] = data_folder
            parts = data_folder.split("/")
            folder = parts[-1]
            self.data_path_button.config(text=folder)

    def output_folder(self) -> None:
        """
        Asks the user to choose the output folder where CSV will be written.

        Args:
            None

        Returns:
            None
        """
        output_folder = filedialog.askdirectory()
        if output_folder:
            os.environ["OUTPUT_FOLDER"] = output_folder
            parts = output_folder.split("/")
            folder = parts[-1]
            self.output_path_button.config(text=folder)

    def standby_file(self) -> None:
        """
        Asks the user to choose the Standby method file he wants to use.

        Args:
            None

        Returns:
            None
        """
        standby_file = filedialog.askopenfilename(filetypes=[("methods", "*.meth")]).split(".")[0]
        if standby_file:
            os.environ["STANDBY_FILE"] = standby_file
            parts = standby_file.split("/")
            file = parts[-1]
            self.standby_path_button.config(text=file)

    def show_values(self, clicked_button) -> None:
        """
        Stores all the parameters to the environment when user confirms his choice.

        Args:
            None

        Returns:
            None
        """
        # Retrieve the entered values
        os.environ["USERNAME"] = self.username.get()
        os.environ["PASSWORD"] = self.password.get()
        os.environ["OPERATOR"] = self.operator.get()
        os.environ["MS_ID"] = self.ms_id.get()
        os.environ["COL_RACK_NUMBER"] = str(self.col_rack_number.get())
        os.environ["ROW_RACK_NUMBER"] = str(self.row_rack_number.get())
        os.environ["PRE_BLK"] = str(self.pre_blk.get())
        os.environ["POST_BLK"] = str(self.post_blk.get())
        os.environ["BLK_NAME"] = self.blk_name.get()
        os.environ["BLK_POS"] = self.blk_pos.get()
        os.environ["INJ_VOLUME"] = str(self.inj_volume.get())
        # Launches test connection to directus
        self.clicked_button = clicked_button
        self.testConnection()

    def testConnection(self) -> None:
        """
        Controls that user has passed all the necessary arguments.
        If it is the case, it tries to connect to directus and if connection is successful,
        stores the access token for further requests.

        Args:
            None

        Returns:
            None
        """
        username = os.environ.get("USERNAME")
        password = os.environ.get("PASSWORD")
        operator = os.environ.get("OPERATOR")
        ms_id = os.environ.get("MS_ID")
        col_rack_number = os.environ.get("COL_RACK_NUMBER")
        row_rack_number = os.environ.get("ROW_RACK_NUMBER")
        inj_volume = os.environ.get("INJ_VOLUME")
        method_file = os.environ.get("METHOD_FILE")
        data_folder = os.environ.get("DATA_FOLDER")
        output_folder = os.environ.get("OUTPUT_FOLDER")

        if (
            username
            and password
            and operator
            and ms_id
            and col_rack_number
            and row_rack_number
            and inj_volume
            and method_file
            and data_folder
            and output_folder
        ):
            # Define the Directus base URL
            base_url = "http://directus.dbgi.org"

            # Define the login endpoint URL
            login_url = base_url + "/auth/login"
            # Create a session object for making requests
            session = requests.Session()
            # Send a POST request to the login endpoint
            response = session.post(login_url, json={"email": username, "password": password})
            # Test if connection is successful
            if response.status_code == 200:
                # Stores the access token
                data = response.json()["data"]
                access_token = data["access_token"]
                os.environ["ACCESS_TOKEN"] = str(access_token)

                # Test if the method is already present in directus
                access_token = os.environ.get("ACCESS_TOKEN")
                base_url = "http://directus.dbgi.org"
                collection_url = base_url + f"/items/Injection_Methods/{self.file}"
                session = requests.Session()
                session.headers.update({"Authorization": f"Bearer {access_token}"})
                # collection_url = base_url + '/items/samples'
                response = session.get(collection_url)
                value = response.status_code
                # if already present, launches the sample list window
                if value == 200:
                    # Hide the main page and open Window 2
                    self.manage_choice()
                # else adds the new method to directus
                else:
                    # Send data to directus
                    base_url = "http://directus.dbgi.org"
                    collection_url = base_url + "/items/Injection_Methods"
                    session = requests.Session()
                    session.headers.update({"Authorization": f"Bearer {access_token}"})

                    # Add headers
                    headers = {"Content-Type": "application/json"}

                    data = {"method_name": self.file}

                    response = session.post(url=collection_url, headers=headers, json=data)

                    # if method is successfully added to directus, launchtes the sample list window
                    if response.status_code == 200:
                        # Hide the main page and open Window 2
                        self.manage_choice()

            # If connection to directus failed, informs the user that connection failed.
            else:
                self.label.config(
                    text="Connexion to directus failed, verify your credentials/vpn connection", foreground="red"
                )

        else:
            # If user didn't enter all necessary values, shows this message
            self.label.config(text="Please provide all asked values", foreground="red")

    def manage_choice(self) -> None:
        """
        Redirects the user to the correct next window (new batch or csv batch).

        Args:
            None

        Returns:
            None
        """
        if self.clicked_button == "new":
            self.open_new_batch()
        elif self.clicked_button == "csv":
            self.open_csv_batch()
        else:
            print("unknown error, please try again.")

    def open_new_batch(self) -> None:
        """
        Hides the main window and initializes the new batch sample list window.

        Args:
            None

        Returns:
            None
        """
        # Hide the main page
        window.withdraw()

        operator = os.environ.get("OPERATOR")

        newWindow = tk.Tk()
        newWindow.title("New batch")

        output_folder = os.environ.get("OUTPUT_FOLDER")
        new_batch.newBatch(
            root=newWindow,
            csv_path=f"{output_folder}/{datetime.now().strftime('%Y%m%d')}_{operator}_dbgi_{self.file}.csv",
        )

    def open_csv_batch(self) -> None:
        """
        Hides the main window and initializes the csv sample list window.

        Args:
            None

        Returns:
            None
        """
        # Hide the main page
        self.pack_forget()
        #window.destroy()

        operator = os.environ.get("OPERATOR")
        output_folder = os.environ.get("OUTPUT_FOLDER")

        #window3 = tk.Tk()

        
        #csvBatch(
        #    root=window3,
        #    csv_path=f"{output_folder}/{datetime.now().strftime('%Y%m%d')}_{operator}_dbgi_{self.file}.csv",
        #)

        # Hide the main page and open Window 1
        #self.pack_forget()
        csvWindow = csv_batch.csvBatch(parent=self.master, csv_path=f"{output_folder}/{datetime.now().strftime('%Y%m%d')}_{operator}_dbgi_{self.file}.csv")
        csvWindow.title("CSV import")
        csvWindow.pack()

    def deiconify(self) -> None:
        """
        make the home page visible again. Called by external scripts.

        Args:
            None

        Returns:
            None
        """
        window.deiconify()

# Create the main window
window = tk.Tk()
window.title("Home")
window.minsize(600, 600)

# Create a Frame within the Tk window
window_frame = tk.Frame(window)
# Pack the Frame to occupy the whole window
window_frame.pack()
# Pass window_frame as the parent
main_page = HomeWindow(window_frame)
# Pack the HomeWindow within the Frame
main_page.pack()
window.mainloop()