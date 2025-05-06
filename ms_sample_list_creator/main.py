# Run "pyinstaller --onefile main.py"
# Generated binaries are made for the native system where the pyinstaller command is run.

# You can generate windows executable from linux using wine, by previously installing wine, python 3.8.19, pyinstaller and
# other non-built-in packages (here requests and pandas) inside wine. Then run: wine pyinstaller --onefile main.py

import csv
import os
import tkinter as tk
import webbrowser
from datetime import datetime
from tkinter import filedialog, ttk
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import requests


class HomeWindow(tk.Frame):
    def __init__(self, parent: tk.Tk, *args: Any, **kwargs: Any):
        """
        Initializes an instance of the class.

        Args:
            parent(tk.Tk): The parent widget or window where this frame will be placed.
            csv_path(str): CSV path and name.

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
        self.batch_key = tk.IntVar(None)
        self.method_files: List[str] = []
        self.file: str = ""

        # Send a request to github to know if this version is the las one
        release_url = (
            "https://api.github.com/repos/digital-botanical-gardens-initiative/ms-sample-list-creator/releases/latest"
        )
        session = requests.Session()
        response = session.get(release_url)
        data = response.json()["tag_name"]
        tag = float(str.replace(data, "v.", ""))

        if tag <= 2.0:
            self.label = tk.Label(self, text="Connect to directus and adjust the parameters")
            self.label.pack()

            # Create text entry fields
            frame_labels_up = tk.Frame(self)
            frame_labels_up.pack(fill="x", pady=(7, 0))

            label_username = tk.Label(frame_labels_up, text="Directus username:")
            label_username.pack(side="left", padx=15, anchor="center")
            label_password = tk.Label(frame_labels_up, text="Directus password:")
            label_password.pack(side="right", padx=(0, 20), anchor="center")

            frame_entries_up = tk.Frame(self)
            frame_entries_up.pack(fill="x", pady=2)

            entry_username = tk.Entry(frame_entries_up, textvariable=self.username)
            entry_username.pack(side="left", anchor="center")
            entry_password = tk.Entry(frame_entries_up, textvariable=self.password, show="*")
            entry_password.pack(side="right", anchor="center")

            # set the cursor to the prefix entry
            entry_username.focus_set()

            frame_labels_om = tk.Frame(self)
            frame_labels_om.pack(fill="x", pady=(7, 0))

            label_operator = tk.Label(frame_labels_om, text="Operator's initials:")
            label_operator.pack(side="left", padx=18, anchor="center")

            label_ms = tk.Label(frame_labels_om, text="Mass spectrometer ID:")
            label_ms.pack(side="right", padx=(0, 7), anchor="center")

            frame_entries_om = tk.Frame(self)
            frame_entries_om.pack(fill="x", pady=(2, 0))

            entry_operator = tk.Entry(frame_entries_om, textvariable=self.operator)
            entry_operator.pack(side="left", anchor="center")

            entry_ms = tk.Entry(frame_entries_om, textvariable=self.ms_id)
            entry_ms.pack(side="right", anchor="center")

            frame_label_rack = tk.Frame(self)
            frame_label_rack.pack(fill="x", pady=(7, 0))

            label_col_rack_number = tk.Label(frame_label_rack, text="Rack size (columns x rows)")
            label_col_rack_number.pack(side="bottom", anchor="center")

            frame_entries_rack = tk.Frame(self)
            frame_entries_rack.pack(fill="x", pady=(2, 0))

            entry_col_rack_number = tk.Entry(frame_entries_rack, textvariable=self.col_rack_number)
            self.col_rack_number.set(9)
            entry_col_rack_number.pack(side="left", anchor="center")

            label_x = tk.Label(frame_entries_rack, text="x")
            label_x.pack(side="left", padx=40, anchor="center")

            entry_row_rack_number = tk.Entry(frame_entries_rack, textvariable=self.row_rack_number)
            self.row_rack_number.set(6)
            entry_row_rack_number.pack(side="right", anchor="center")

            frame_labels_blk = tk.Frame(self)
            frame_labels_blk.pack(fill="x", pady=(7, 0))

            label_pre_blk = tk.Label(frame_labels_blk, text="Blanks before samples:")
            label_pre_blk.pack(side="left", padx=4, anchor="center")

            label_post_blk = tk.Label(frame_labels_blk, text="Blanks after samples:")
            label_post_blk.pack(side="right", padx=(0, 8), anchor="center")

            frame_entries_blk = tk.Frame(self)
            frame_entries_blk.pack(fill="x", pady=(2, 0))

            entry_pre_blk = tk.Entry(frame_entries_blk, textvariable=self.pre_blk)
            self.pre_blk.set(4)
            entry_pre_blk.pack(side="left", anchor="center")

            entry_post_blk = tk.Entry(frame_entries_blk, textvariable=self.post_blk)
            self.post_blk.set(3)
            entry_post_blk.pack(side="right", anchor="center")

            frame_labels_np = tk.Frame(self)
            frame_labels_np.pack(fill="x", pady=(7, 0))

            label_blk_name = tk.Label(frame_labels_np, text="Blank name:")
            label_blk_name.pack(side="left", padx=40, anchor="center")

            label_blk_pos = tk.Label(frame_labels_np, text="Blank position:")
            label_blk_pos.pack(side="right", padx=(0, 30), anchor="center")

            frame_entries_np = tk.Frame(self)
            frame_entries_np.pack(fill="x", pady=(2, 0))

            entry_blk_name = tk.Entry(frame_entries_np, textvariable=self.blk_name)
            entry_blk_name.pack(side="left", anchor="center")

            entry_blk_pos = tk.Entry(frame_entries_np, textvariable=self.blk_pos)
            entry_blk_pos.pack(side="right", anchor="center")

            frame_labels_pv = tk.Frame(self)
            frame_labels_pv.pack(fill="x", pady=(7, 0))

            label_inj_volume = tk.Label(frame_labels_pv, text="Injection volume (µL):")
            label_inj_volume.pack(side="left", anchor="center", padx=5)

            label_batch = tk.Label(frame_labels_pv, text="Batch:")
            label_batch.pack(side="right", padx=(0, 60), anchor="center")

            frame_entries_pv = tk.Frame(self)
            frame_entries_pv.pack(fill="x", pady=(2, 0))

            entry_inj_volume = tk.Entry(frame_entries_pv, textvariable=self.inj_volume)
            self.inj_volume.set(2)
            entry_inj_volume.pack(side="left")

            self.batch_key.set(-1)

            # Extract future code to possibly create
            collection_url = "https://emi-collection.unifr.ch/directus/items/Batches"
            column = "batch_id"
            params: Dict[str, Union[str, int, float, None]] = {"sort[]": f"-{column}", "limit": 1}
            session = requests.Session()
            response = session.get(collection_url, params=params)
            last_value = response.json()["data"][0][column] if response.json()["data"] else "null"
            last_number = int(last_value.split("_")[1]) if last_value != "null" else 0
            first_number = last_number + 1
            self.new_batch = "batch_" f"{first_number:06d}"

            # Fetch batches of type 6
            params = {"sort[]": f"{column}", "filter[batch_type][_eq]": 6}
            response = session.get(collection_url, params=params)
            data = response.json()["data"]

            # Create a mapping dictionary and list of options for the dropdown
            batch_mapping = {f"New ({self.new_batch})": 0}  # "new" maps to ID 0
            batch_names = ["Select a batch"]  # Add a placeholder for no default selection
            batch_names.append(f"New ({self.new_batch})")  # Add "new batch" option

            for item in data:
                batch_mapping[item[column]] = item["id"]  # Map batch_id to id
                batch_names.append(item[column])  # Add human-readable batch_id to the dropdown

            # Create the OptionMenu and callback
            def on_batch_selected(selection: tk.StringVar) -> None:
                selected_id = batch_mapping.get(str(selection), -1)  # Get the associated ID or None
                self.batch_key.set(selected_id)  # Update self.batch with the ID
                os.environ["BATCH"] = str(selection)

            # Use StringVar for the selected value
            selected_batch = tk.StringVar()
            selected_batch.set(batch_names[0])  # Set default value to "Select a batch"

            # Create the dropdown
            self.dropdown_batch = tk.OptionMenu(
                frame_entries_pv, selected_batch, *batch_names, command=on_batch_selected
            )
            self.dropdown_batch.config(width=15, background="PeachPuff2")
            self.dropdown_batch.pack(side="right", anchor="center")

            frame_label_methods = tk.Frame(self)
            frame_label_methods.pack(fill="x", pady=(7, 0))

            label_method_path = tk.Label(frame_label_methods, text="Method file:")
            label_method_path.pack(side="left", padx=40, anchor="center")

            self.method_select_frame = tk.Frame(self)
            self.method_select_frame.pack(fill="x", pady=(2, 0))

            # Bouton "+"
            add_method_btn = tk.Button(
                self.method_select_frame,
                text="+",
                command=self.add_method_selector,
                width=2,
                background="lemon chiffon",
            )
            add_method_btn.pack(side="left", padx=40)

            label_standby = tk.Label(frame_label_methods, text="Standby method file: ")
            label_standby.pack(side="right", padx=(0, 10), anchor="center")

            frame_entries_methods = tk.Frame(self)
            frame_entries_methods.pack(fill="x", pady=(2, 0))

            self.standby_path_button = tk.Button(
                frame_entries_methods, text="method", background="lemon chiffon", width=17, command=self.standby_file
            )
            self.standby_path_button.pack(side="right", anchor="center", padx=(0, 1))

            frame_label_output = tk.Frame(self)
            frame_label_output.pack(fill="x", pady=(7, 0))

            label_data_path = tk.Label(frame_label_output, text="MS data directory")
            label_data_path.pack(side="left", anchor="center", padx=25)

            label_output_path = tk.Label(frame_label_output, text="Sample list directory: ")
            label_output_path.pack(side="right", padx=(0, 10), anchor="center")

            frame_entry_output = tk.Frame(self)
            frame_entry_output.pack(fill="x", pady=(2, 0))

            self.data_path_button = tk.Button(
                frame_entry_output, text="output", background="light goldenrod", width=17, command=self.data_folder
            )
            self.data_path_button.pack(side="left", padx=1, anchor="center")

            self.output_path_button = tk.Button(
                frame_entry_output, text="output", background="light goldenrod", width=17, command=self.output_folder
            )
            self.output_path_button.pack(side="right", anchor="center", padx=(0, 1))

            frame_submit = tk.Frame(self)
            frame_submit.pack(fill="x", pady=(50, 0))

            button_new_batch = tk.Button(
                frame_submit,
                text="New sample list",
                background="light green",
                width=17,
                height=3,
                command=lambda: self.show_values("new"),
            )
            button_new_batch.pack(side="left")

            button_submit_csv = tk.Button(
                frame_submit,
                text="Sample list from CSV",
                background="light blue",
                width=17,
                height=3,
                command=lambda: self.show_values("csv"),
            )
            button_submit_csv.pack(side="right")
        else:
            # Create GUI elements to ask user to download the latest version
            label_labels = tk.Label(self, text="A new version is available, please download it.")
            label_labels.pack()

            button_new_labels = tk.Button(
                self, text="Download latest version", width=40, command=self.download_last_version
            )
            button_new_labels.pack()

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

    def add_method_selector(self) -> None:
        frame = ttk.Frame(self.method_select_frame)
        frame.pack(fill="x", pady=2)

        method_label = ttk.Label(frame, text="Methods:")
        method_label.pack(side="left")

        method_button = ttk.Button(frame, text="Add method", command=lambda: self.select_method_file(method_button))
        method_button.pack(side="left", padx=5)

    def select_method_file(self, button: ttk.Button) -> None:
        """
        Asks the user to choose the injection method file he wants to use.

        Args:
            None

        Returns:
            None
        """
        file_path = filedialog.askopenfilename(filetypes=[("methods", "*.meth")])
        if file_path:
            method_file = file_path.rsplit(".", 1)[0]  # évite un bug si le nom contient plusieurs "."
            self.method_files.append(method_file)
            file_name = os.path.basename(method_file)
            button.config(text=file_name)

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

    def show_values(self, clicked_button: str) -> None:
        """
        Stores all the parameters to the environment when user confirms his choice.

        Args:
            clicked_button(str): A string ("new" or "csv"), that defines which window will be launched after home page.

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
        os.environ["BATCH_KEY"] = str(self.batch_key.get())
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
        ms_id = str(os.environ.get("MS_ID"))
        col_rack_number = os.environ.get("COL_RACK_NUMBER")
        row_rack_number = os.environ.get("ROW_RACK_NUMBER")
        inj_volume = os.environ.get("INJ_VOLUME")
        method_file = os.environ.get("METHOD_FILE")
        data_folder = os.environ.get("DATA_FOLDER")
        output_folder = os.environ.get("OUTPUT_FOLDER")
        batch = int(str(os.environ.get("BATCH_KEY")))

        instrument_key = get_primary_key(
            "https://emi-collection.unifr.ch/directus/items/Instruments", ms_id, "instrument_id"
        )
        injection_method_key = get_primary_key(
            "https://emi-collection.unifr.ch/directus/items/Injection_Methods", self.file, "method_name"
        )

        os.environ["INSTRUMENT_KEY"] = str(instrument_key)

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
            and batch != -1
            and self.file != ""
            and instrument_key != -1
        ):
            # Define the Directus base URL
            base_url = "https://emi-collection.unifr.ch/directus"

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

                if batch == 0:
                    batch = self.add_batch(access_token)
                    os.environ["BATCH_KEY"] = str(batch)

                if batch > 0:
                    if injection_method_key == -1:
                        self.add_method(access_token)
                    else:
                        # As injection method already exist attribute it
                        os.environ["INJECTION_METHOD_KEY"] = str(injection_method_key)

                        # Hide the main page and open Window 2
                        self.manage_choice()
                else:
                    self.label.config(text="Connexion to directus failed, please try again", foreground="red")

            # If connection to directus failed, informs the user that connection failed.
            else:
                self.label.config(text="Connexion to directus failed, verify your credentials", foreground="red")

        else:
            # If user didn't enter all necessary values, shows this message
            self.label.config(text="Please provide all values / valid values", foreground="red")

    def add_method(self, access_token: str) -> None:
        """
        Adds an injection method to directus
        """

        # Send data to directus
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {access_token}"})

        # Add headers
        headers = {"Content-Type": "application/json"}

        # Define the data to be sent
        data = {"method_name": self.file}

        # Define the Directus URL
        base_url = "https://emi-collection.unifr.ch/directus"
        collection_url = base_url + "/items/Injection_Methods/"

        # Send a POST request to create the new method
        response = session.post(url=collection_url, headers=headers, json=data)

        # if method is successfully added to directus, launches the sample list window
        if response.status_code == 200:
            injection_method_key = response.json()["data"]["id"]
            os.environ["INJECTION_METHOD_KEY"] = str(injection_method_key)

            # Hide the main page and open Window 2
            self.manage_choice()

        else:
            print(f"Error creating method: status code: {response.status_code}, message: {response.text}")

    def add_batch(self, access_token: str) -> int:
        """
        Adds an injection method to directus
        """

        # Send data to directus
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {access_token}"})

        # Add headers
        headers = {"Content-Type": "application/json"}

        collection_url = "https://emi-collection.unifr.ch/directus/items/Batches"

        data = {
            "batch_id": self.new_batch,
            "batch_type": 6,
            "short_description": "ms batch",
            "description": "ms batch",
        }

        response = session.post(url=collection_url, headers=headers, json=data)

        # if method is successfully added to directus, launches the sample list window
        batch_id = response.json()["data"]["id"] if response.status_code == 200 else -1
        return batch_id

    def manage_choice(self) -> None:
        """
        Returns to main script which option did the user choose.

        Args:
            None

        Returns:
            None
        """
        if self.clicked_button == "new":
            self.label.config(text="Connect to directus and adjust the parameters", foreground="black")
            # Create a new Toplevel window for the new batch
            new_batch_window = tk.Toplevel(root)
            new_batch_window.title("Create new batch")
            # Show the window for a new batch
            newBatch(new_batch_window, root)
        elif self.clicked_button == "csv":
            self.label.config(text="Connect to directus and adjust the parameters", foreground="black")
            # Create a new Toplevel window for the new batch
            csv_batch_window = tk.Toplevel(root)
            csv_batch_window.minsize(300, 200)
            csv_batch_window.title("Import csv batch")
            # Show the window for a new batch
            csvBatch(csv_batch_window, root)
        else:
            # If user didn't enter all necessary values, shows this message
            self.label.config(text="Unknow error, please try again with other parameters", foreground="red")

    # Function that redirects user to the last software version
    def download_last_version(self) -> None:
        url = "https://github.com/digital-botanical-gardens-initiative/ms-sample-list-creator/releases/latest"
        webbrowser.open(url)


class newBatch:
    def __init__(self, new_batch_window: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            new_batch_window(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """

        self.new_batch_window = new_batch_window
        self.root = root

        # Make CsvWindow wait for AskBoxPrefixWindow result
        self.root.withdraw()

        self.new_batch_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.operator = str(os.environ.get("OPERATOR"))
        self.ms_id = str(os.environ.get("MS_ID"))
        self.col_rack_size = int(str(os.environ.get("COL_RACK_NUMBER")))
        self.row_rack_size = int(str(os.environ.get("ROW_RACK_NUMBER")))
        self.pre_blk = int(str(os.environ.get("PRE_BLK")))
        self.post_blk = int(str(os.environ.get("POST_BLK")))
        self.blk_name = str(os.environ.get("BLK_NAME"))
        self.blk_pos = str(os.environ.get("BLK_POS"))
        self.inj_volume = int(str(os.environ.get("INJ_VOLUME")))
        self.access_token = str(os.environ.get("ACCESS_TOKEN"))
        self.method_file = str(os.environ.get("METHOD_FILE"))
        self.data_path = str(os.environ.get("DATA_FOLDER"))
        self.standby_file = str(os.environ.get("STANDBY_FILE"))
        self.output_folder = str(os.environ.get("OUTPUT_FOLDER"))
        self.file = str(os.environ.get("FILE"))
        self.batch_key = int(str(os.environ.get("BATCH_KEY")))
        self.batch = str(os.environ.get("BATCH"))
        self.instrument_key = int(str(os.environ.get("INSTRUMENT_KEY")))
        self.injection_method_key = int(str(os.environ.get("INJECTION_METHOD_KEY")))
        self.csv_path = f"{self.output_folder}/{datetime.now().strftime('%Y%m%d')}_{self.operator}_emi_{self.file}.csv"
        self.current_position = 1
        self.current_row = 1
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M")

        # Create Treeview widget
        self.tree = ttk.Treeview(
            self.new_batch_window,
            columns=(
                "aliquot_id",
                "operator",
                "ms_id",
                "File Name",
                "Path",
                "Instrument Method",
                "Position",
                "Inj Vol",
                "Batch",
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
        self.tree.heading("Batch", text="Batch")

        # Bind Enter key to add row
        self.new_batch_window.bind("<Return>", self.add_row)

        # Entry widgets for data input
        self.aliquot_id_entry = ttk.Entry(self.new_batch_window)

        # Error text hidden:
        self.label = ttk.Label(self.new_batch_window, text="")
        self.label.grid(row=2, column=0, columnspan=2, pady=10)

        # Submit button
        submit_button = ttk.Button(
            self.new_batch_window, text="Generate sample list", width=20, command=self.submit_table
        )

        # Back button
        button_back = tk.Button(self.new_batch_window, text="Back to Home", width=20, command=self.on_exit)

        # Grid layout for widgets
        self.tree.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.aliquot_id_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        submit_button.grid(row=3, column=1, columnspan=2, pady=10)
        button_back.grid(row=4, column=1, columnspan=2, pady=10)

        # Start the Tkinter event loop
        self.new_batch_window.mainloop()

    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        self.new_batch_window.destroy()
        self.root.deiconify()

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

        # Placeholder calculations for other columns
        filename = self.timestamp + "_" + str(self.operator) + "_" + aliquot_id
        path = self.data_path.replace("/", "\\")
        instrument_method = self.method_file.replace("/", "\\")
        inj_volume = self.inj_volume

        # Send data to directus
        base_url = "https://emi-collection.unifr.ch/directus"
        collection_url = base_url + "/items/MS_Data"
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {self.access_token}"})

        # Add headers
        headers = {"Content-Type": "application/json"}

        aliquot_key = get_primary_key(
            "https://emi-collection.unifr.ch/directus/items/Containers", aliquot_id, "container_id"
        )

        data = {
            "parent_sample_container": aliquot_key,
            "filename": filename,
            "instrument_used": self.instrument_key,
            "injection_volume": inj_volume,
            "injection_volume_unit": 18,
            "injection_method": self.injection_method_key,
            "batch": self.batch_key,
        }

        response = session.post(url=collection_url, headers=headers, json=data)

        self.label.config(text="")

        if response.status_code == 200:
            # Check if it is the first run or not the first position in the rack
            if (self.current_position > self.col_rack_size and self.current_position > self.col_rack_size) or (
                self.current_position == 1 and self.current_row == 1
            ):
                # Open window to ask prefix
                ask_prefix_window = tk.Toplevel(self.new_batch_window)
                ask_prefix_window.title("Add Prefix")
                self.ask_box = AskBoxPrefixWindow(ask_prefix_window)
                self.ask_box.pack()

                # Make CsvWindow wait for AskBoxPrefixWindow result
                ask_prefix_window.transient(self.new_batch_window)
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
                values=(
                    aliquot_id,
                    self.operator,
                    self.ms_id,
                    filename,
                    path,
                    instrument_method,
                    position,
                    inj_volume,
                    self.batch,
                ),
            )

            # Scroll to the last added row
            self.tree.see(item_id)

            # Clear entry widgets
            self.aliquot_id_entry.delete(0, "end")

        # Catches forbidden access when token is expired and generates a new token
        elif response.status_code == 401:
            self.directus_reconnect()
        else:
            self.label.config(text=f"Directus error, {aliquot_id} doesn't seem to be valid!", foreground="red")

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
        raw_data = [self.tree.item(item, "values")[3:8] for item in all_items]  # Skip the first two elements
        data_to_export = sorted(raw_data, key=blanks_first)

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
                        self.timestamp + "_" + self.operator + "_emi_" + self.blk_name + "_blk_pre" + padded_number
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
                        self.timestamp + "_" + self.operator + "_emi_" + self.blk_name + "_blk_post" + padded_number
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

        self.label.config(text="Sample list correctly generated!", foreground="green")

        # Schedule the window to be destroyed after 2000 milliseconds (2 seconds)
        self.new_batch_window.after(2000, self.destroy_window)

    # Define the function to destroy the window
    def destroy_window(self) -> None:
        self.new_batch_window.destroy()
        self.root.deiconify()

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
        base_url = "https://emi-collection.unifr.ch/directus"

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
    if sample_id.startswith("blk"):
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
        self.prefix.set("G:")
        entry_prefix.pack()

        # set the cursor to the prefix entry
        entry_prefix.focus_set()

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


class csvBatch(tk.Frame):
    def __init__(self, csv_batch_window: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            csv_batch_window(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """
        self.csv_batch_window = csv_batch_window
        self.root = root

        # Make CsvWindow wait for AskBoxPrefixWindow result
        self.root.withdraw()

        self.csv_batch_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.operator = str(os.environ.get("OPERATOR"))
        self.output_folder = os.environ.get("OUTPUT_FOLDER")
        self.ms_id = str(os.environ.get("MS_ID"))
        self.col_rack_size = int(str(os.environ.get("COL_RACK_NUMBER")))
        self.row_rack_size = int(str(os.environ.get("ROW_RACK_NUMBER")))
        self.pre_blk = int(str(os.environ.get("PRE_BLK")))
        self.post_blk = int(str(os.environ.get("POST_BLK")))
        self.blk_name = str(os.environ.get("BLK_NAME"))
        self.blk_pos = str(os.environ.get("BLK_POS"))
        self.inj_volume = int(str(os.environ.get("INJ_VOLUME")))
        self.access_token = str(os.environ.get("ACCESS_TOKEN"))
        self.method_file = str(os.environ.get("METHOD_FILE"))
        self.data_path = str(os.environ.get("DATA_FOLDER"))
        self.standby_file = str(os.environ.get("STANDBY_FILE"))
        self.file = str(os.environ.get("FILE"))
        self.batch_key = int(str(os.environ.get("BATCH_KEY")))
        self.batch = str(os.environ.get("BATCH"))
        self.instrument_key = int(str(os.environ.get("INSTRUMENT_KEY")))
        self.injection_method_key = int(str(os.environ.get("INJECTION_METHOD_KEY")))
        self.current_position = 1
        self.current_row = 1
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M")
        self.csv_path = f"{self.output_folder}/{datetime.now().strftime('%Y%m%d')}_{self.operator}_emi_{self.file}.csv"

        self.warning_label = tk.Label(
            self.csv_batch_window,
            text="Warning, this mode is exclusively made to submit sample lists that have already been made using this tool.",
        )
        self.warning_label.pack()

        label = tk.Label(self.csv_batch_window, text="Search for your CSV:", pady=10)
        label.pack()

        self.import_button = tk.Button(
            self.csv_batch_window, text="Import your CSV", width=17, command=self.import_csv, pady=10
        )
        self.import_button.pack()

        button_submit = tk.Button(self.csv_batch_window, text="Submit", width=17, command=self.submit_result, pady=10)
        button_submit.pack()

        button_back = tk.Button(self.csv_batch_window, text="Go back to home", width=17, command=self.on_exit, pady=10)
        button_back.pack()

    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        self.csv_batch_window.destroy()
        self.root.deiconify()

    def import_csv(self) -> None:
        """
        Asks the path to input CSV.

        Args:
            None

        Returns:
            None
        """
        csv_file = os.environ["FILE_PATH"] = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if csv_file:
            parts = csv_file.split("/")
            file = parts[-1]
            self.import_button.config(text=file)

    def submit_result(self) -> None:
        """
        performs modifications on the CSV, submit them to directus and writes the output csv.

        Args:
            None

        Returns:
            None
        """
        # Retrieves file path and method name given by the user
        file_path = os.environ.get("FILE_PATH")
        self.file = str(os.environ.get("FILE"))

        # Converts the CSV to a dataframe
        df = pd.read_csv(str(file_path), skiprows=1)

        # Keep only the necessary columns in order to not generate a corrupted CSV
        columns_filter = ["File Name", "Path", "Instrument Method", "Position", "Inj Vol"]
        df = df.loc[:, columns_filter]

        # Delete standby row
        df = df.drop(df.index[-1])

        # Remove blanks
        patterns = ["pre", "post"]
        combined_patterns = "|".join(patterns)
        filtered_df = df[~df["File Name"].str.contains(combined_patterns, regex=True)]

        # Update data path, instrument method and injection volume
        path = self.data_path.replace("/", "\\")
        instrument_method = self.method_file.replace("/", "\\")
        filtered_df.loc[:, "Path"] = path
        filtered_df.loc[:, "Instrument Method"] = instrument_method
        filtered_df.loc[:, "Inj Vol"] = self.inj_volume

        # Change timestamp and operator initials
        filtered_df.loc[:, "File Name"] = df.loc[:, "File Name"].apply(
            lambda x: "_".join([self.timestamp, self.operator] + x.split("_")[2:])
        )

        # Prepare data for directus
        directus_df = filtered_df
        directus_df = directus_df.drop(columns=["Path", "Position"])
        directus_df = directus_df.rename(columns={"File Name": "filename"})
        directus_df["parent_sample_container"] = ""
        directus_df = directus_df.rename(columns={"Inj Vol": "injection_volume"})
        directus_df["injection_volume_unit"] = 18
        directus_df = directus_df.rename(columns={"Instrument Method": "injection_method"})
        directus_df["instrument_used"] = self.instrument_key
        directus_df["injection_method"] = self.injection_method_key
        directus_df["batch"] = self.batch_key
        for index, row in directus_df.iterrows():  # Iterate over rows using iterrows()
            parts = row["filename"].split("_")  # Split the "File Name" column by underscores
            aliquot_id = "_".join(parts[2:])  # Extract the desired parts of the split string
            directus_df.at[index, "parent_sample_container"] = get_primary_key(
                "https://emi-collection.unifr.ch/directus/items/Containers", aliquot_id, "container_id"
            )

        # Send data to directus
        records = directus_df.to_json(orient="records")
        base_url = "https://emi-collection.unifr.ch/directus"
        collection_url = base_url + "/items/MS_Data"
        session = requests.Session()
        headers = {"Content-Type": "application/json"}
        session.headers.update({"Authorization": f"Bearer {self.access_token}"})
        response = session.post(url=collection_url, headers=headers, data=records)

        # Check if correctly added to directus
        if response.status_code == 200:
            self.warning_label.config(text="Success!! Writing CSV...", foreground="green")
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
                            self.timestamp + "_" + self.operator + "_emi_" + self.blk_name + "_blk_pre" + padded_number
                        )
                        path = self.data_path.replace("/", "\\")
                        instrument_method = self.method_file.replace("/", "\\")
                        position = self.blk_pos
                        inj_volume = self.inj_volume
                        csv_writer.writerow([filename, path, instrument_method, position, inj_volume])

                # Write data
                csv_writer.writerows(filtered_df.values)

                # Write post blanks
                if self.post_blk > 0:
                    for i in range(1, self.post_blk + 1):
                        padded_number = str(i).zfill(2)
                        filename = (
                            self.timestamp + "_" + self.operator + "_emi_" + self.blk_name + "_blk_post" + padded_number
                        )
                        path = self.data_path.replace("/", "\\")
                        instrument_method = self.method_file.replace("/", "\\")
                        position = self.blk_pos
                        inj_volume = self.inj_volume
                        csv_writer.writerow([filename, path, instrument_method, position, inj_volume])

                # Write standby line
                parts = self.standby_file.split("/")
                file = parts[-1]
                filename = self.timestamp + "_" + self.operator + "_" + file
                path = self.data_path.replace("/", "\\")
                standby = self.standby_file.replace("/", "\\")
                position = self.blk_pos
                inj_volume = self.inj_volume
                csv_writer.writerow([filename, path, standby, position, inj_volume])

            self.warning_label.config(text="Sample list correctly generated!", foreground="green")

            # Schedule the window to be destroyed after 2000 milliseconds (2 seconds)
            self.csv_batch_window.after(2000, self.destroy_window)
        else:
            self.warning_label.config(text="Directus error, please check your CSV.", foreground="red")

    # Define the function to destroy the window
    def destroy_window(self) -> None:
        self.csv_batch_window.destroy()
        self.root.deiconify()


def get_primary_key(collection_url: str, value: str, column: str) -> int:
    params: Dict[str, Union[str, int, float, None]] = {f"filter[{column}][_eq]": value, "limit": 1}
    session = requests.Session()
    response = session.get(collection_url, params=params)
    key = response.json()["data"][0]["id"] if response.json()["data"] else -1
    return key


# Create an instance of the main window
root = tk.Tk()
root.title("Home")
root.minsize(550, 650)

# Create an instance of the HomeWindow class
home = HomeWindow(root)

# Display the HomeWindow
home.pack()

# Start the tkinter event loop
root.mainloop()
