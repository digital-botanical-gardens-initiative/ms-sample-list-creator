import tkinter as tk
from typing import Any, Dict, Union
from tkinter import filedialog, ttk
from .structure import TkVariables, DirectusSessionData
from dataclasses import fields
import os
import requests

from ms_sample_list_creator import utils
from .new_sample_list import newBatch
from .csv_sample_list import csvBatch

class HomeWindow(ttk.Frame):
    """
    Class to display a message when a new version of the application is available.
    """
    def __init__(self, root: tk.Tk, *args: Any, **kwargs: Any): 
        """
        Initializes an instance of the class.

        Args:
            parent(tk.Tk): The parent widget or window where this frame will be placed.
            csv_path(str): CSV path and name.

        Returns:
            None
        """
        self.root = root

        self.vars = TkVariables()
        self.session_data = DirectusSessionData()


        self.label = ttk.Label(self.root, text="", foreground="red")
        self.label.pack(pady=5)

        ttk.Frame.__init__(self, root, *args, **kwargs)

        self.build_gui()

    def build_gui(self) -> None:
        """
        Builds the main GUI elements: fields for user inputs and buttons.
        """
        # Create a frame for each section
        self.build_directus_fields()
        self.build_operator_ms_fields()
        self.build_sample_settings_fields()
        self.build_method_section()
        self.build_standby_selector()
        self.build_data_selector()
        self.build_output_selector()
        self.build_submit_buttons()

    
    def build_directus_fields(self) -> None:
        utils.create_label_entry_pair(
        parent=self,
        left_label_text="Directus username:",
        right_label_text="Directus password:",
        left_var=self.vars.directus.username,  
        right_var=self.vars.directus.password,
        show_right="*"
    )

    def build_operator_ms_fields(self) -> None:
        utils.create_label_entry_pair(
        parent=self,
        left_label_text="Operator's initials:",
        right_label_text="Mass spectrometer ID:",
        left_var=self.vars.operator_settings.operator, 
        right_var=self.vars.operator_settings.ms_id
    )
    
    def build_sample_settings_fields(self) -> None:
        """
        Builds the sample settings section, including rack dimensions and blank info.
        """
        utils.create_label_entry_pair(
            parent=self,
            left_label_text="Rack columns:",
            right_label_text="Rack rows:",
            left_var=self.vars.col_rack_number,
            right_var=self.vars.row_rack_number
        )

        utils.create_label_entry_pair(
            parent=self,
            left_label_text="Blank name:",
            right_label_text="Blank position:",
            left_var=self.vars.blk_name,
            right_var=self.vars.blk_pos
        )


    def add_method_selector(self) -> None:
        frame = ttk.Frame(self.method_select_frame)
        frame.pack(fill="x", pady=2)

        method_label = ttk.Label(frame, text="Methods:")
        method_label.pack(side="left")

        method_button = ttk.Button(frame, text="Add method")
        method_button.pack(side="left", padx=5)
        method_button.config(command=lambda: self.select_method_file(method_button))

    def data_folder(self) -> None:
        utils.choose_path_and_update_button(
            dialog_type="folder",
            env_var="DATA_FOLDER",
            button=self.data_path_button,
            filetype=None
    )
        
    def standby_file(self) -> None:
        utils.choose_path_and_update_button(
            dialog_type="file",
            env_var="STANDBY_FILE",
            button=self.standby_path_button,
            filetype=[("methods", "*.meth")]
    )
        
    def output_folder(self) -> None:
        utils.choose_path_and_update_button(
        dialog_type="folder",
        env_var="OUTPUT_FOLDER",
        button=self.output_path_button,
        filetype=None
    )
        
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
            method_file = file_path.rsplit(".", 1)[0]  # avoids a bug if the name contains multiple '.'
            self.vars.method_files.append(method_file)
            file_name = os.path.basename(method_file)
            button.config(text=file_name)

    def build_method_section(self) -> None:
        frame_label_methods = ttk.Frame(self)
        frame_label_methods.pack(fill="x", pady=(7, 0))

        label_method_path = ttk.Label(frame_label_methods, text="Injection method file:")
        label_method_path.pack(side="left", padx=10)

        self.method_select_frame = ttk.Frame(self)
        self.method_select_frame.pack(fill="x", pady=(2, 0))

        add_method_btn = ttk.Button(
            self.method_select_frame,
            text="+",
            command=self.add_method_selector,
            width=2,
        )
        add_method_btn.pack(side="left", padx=10)

    def build_standby_selector(self) -> None:
        self.standby_path_button = utils.create_label_button_row(
            parent=self,
            label_text="Standby method file:",
            button_text="Select Standby File",
            command=self.standby_file
        )

    def build_output_selector(self) -> None:
        self.output_path_button = utils.create_label_button_row(
            parent=self,
            label_text="Sample list directory:",
            button_text="Select Output Folder",
            command=self.output_folder
        )

    def build_data_selector(self) -> None:
        self.data_path_button = utils.create_label_button_row(
            parent=self,
            label_text="MS data directory:",
            button_text="Select Data Folder",
            command=self.data_folder
        )

    def build_submit_buttons(self) -> None:
        frame_submit = tk.Frame(self)
        frame_submit.pack(fill="x", pady=(50, 0))

        button_new_batch = ttk.Button(
            frame_submit,
            text="New sample list",
            style="Success.TButton",
            width=17,
            command=lambda: self.show_values("new"),
        )
        button_new_batch.pack(side="left")

        button_submit_csv = ttk.Button(
            frame_submit,
            text="Sample list from CSV",
            style="Info.TButton",
            width=17,
            command=lambda: self.show_values("csv"),
        )
        button_submit_csv.pack(side="right")


    def show_values(self, clicked_button: str) -> None:
        """
        Stores all the parameters entered by the user into the environment variables
        and launches the connection test to Directus.

        Args:
            clicked_button (str): A string ("new" or "csv") that defines which window
                                  will be launched after the home page.

        Returns:
            None
        """
        # Retrieve the entered values and store them in environment variables
        self.store_in_environment()

        # Set the clicked button to manage future window launch
        self.clicked_button = clicked_button

        # Proceed to test the connection to Directus
        self.testConnection()

    def store_in_environment(self) -> None:
        """
        Stores all the necessary user input values into environment variables.
        Automatically stores all attributes of the TkVariables dataclass.

        Returns:
            None
        """
        for field in fields(self.vars):
            field_value = getattr(self.vars, field.name)
            
            # Si la valeur est une Tkinter Variable, on extrait sa valeur
            if isinstance(field_value, (tk.StringVar, tk.IntVar)):
                os.environ[field.name.upper()] = str(field_value.get())

    def testConnection(self) -> None:
        """
        Tests if the connection to Directus is successful after checking all necessary arguments.

        If all parameters are valid, it tries to authenticate with Directus and stores the access token.

        Returns:
            None
        """
        # Retrieve values from environment variables
        user_data = self.get_user_data()

        # If all required values are present, attempt the connection
        if self.are_all_values_present(user_data):
            self.attempt_connection(user_data)
        else:
            self.label.config(text="Please provide all values / valid values", foreground="red")
    
    def get_user_data(self) -> dict:
        """
        Retrieves all the necessary user data from environment variables.
        Automatically stores all attributes of the TkVariables dataclass into a dictionary.

        Returns:
            dict: A dictionary containing all the user data.est
        """
        user_data = {}

        for field in fields(self.vars):
            field_value = getattr(self.vars, field.name)
            
            # If the value is a Tkinter Variable, extract its value
            if isinstance(field_value, (tk.StringVar, tk.IntVar)):
                user_data[field.name] = field_value.get()
            else:
                user_data[field.name] = field_value

        # Manually adds environment variables if necessary
        user_data["data_folder"] = os.environ.get("DATA_FOLDER", "")
        user_data["output_folder"] = os.environ.get("OUTPUT_FOLDER", "")
    
        return user_data
    
    def are_all_values_present(self, user_data: dict) -> bool:
        """
        Checks if all the required user values are present and valid.

        Args:
            user_data (dict): The dictionary containing all user input data.

        Returns:
            bool: True if all values are valid, False otherwise.
        """
        return all(value for value in user_data.values()) and user_data["batch"] != -1

    def attempt_connection(self, user_data: dict) -> None:
        """
        Attempts to connect to Directus using the provided user data.

        If the connection is successful, the access token is stored.

        Args:
            user_data (dict): The dictionary containing the necessary user data.

        Returns:
            None
        """
        # Get the instrument key based on the ms_id
        instrument_key = self.get_instrument_key(user_data["ms_id"])
        self.session_data.instrument_key = instrument_key

        # Store the instrument key in the environment if valid
        if instrument_key != -1:
            os.environ["INSTRUMENT_KEY"] = str(self.session_data.instrument_key)

            # Define the Directus base URL
            base_url = "https://emi-collection.unifr.ch/directus"
            login_url = base_url + "/auth/login"

            # Create a session object for making requests
            session = requests.Session()

            # Recover connection identifiers from dataclass
            username = self.vars.directus.username.get()
            password = self.vars.directus.password.get()

            # Send a POST request to login
            response = session.post(login_url, json={"email": username, "password": password})

            if response.status_code == 200:
                self.handle_successful_login(response.json())
            else:
                self.label.config(text="Connection to Directus failed, verify your credentials", foreground="red")
        else:
            self.label.config(text="Invalid instrument key, please verify your MS_ID", foreground="red")
    
    def get_instrument_key(self, ms_id: str) -> int:
        """
        Retrieves the primary key of the instrument based on the MS_ID.

        Args:
            ms_id (str): The mass spectrometer ID.

        Returns:
            int: The instrument key, or -1 if not found.
        """
        ms_id = self.vars.operator_settings.ms_id.get()
        return utils.get_primary_key(
            "https://emi-collection.unifr.ch/directus/items/Instruments",
            ms_id,
            "instrument_id"
        )
    
    def handle_successful_login(self, data: dict) -> None:
        """
        Handles the actions after a successful login to Directus.

        Args:
            data (dict): The response data containing the access token.


        Returns:
            None
        """
        self.session_data.access_token = data["data"]["access_token"]
        os.environ["ACCESS_TOKEN"] = self.session_data.access_token

        
        # If batch is 0, create a new batch
        batch = 0
        if batch == 0:
            batch = self.add_batch(self.session_data.access_token)

        self.session_data.batch_key = batch
        os.environ["BATCH_KEY"] = str(self.session_data.batch_key)  

        if batch > 0:
            method_keys = []
            all_success = True

            # Attempt to add each method file
            for method_file in self.vars.method_files:
                key = self.add_method(self.session_data.access_token, method_file)
                if key == -1:
                    all_success = False
                method_keys.append(key)

            # If all methods were successfully added, store the method keys
            if all_success:
                self.session_data.method_keys = method_keys
                os.environ["INJECTION_METHOD_KEYS"] = ",".join(map(str, self.session_data.method_keys))
                self.manage_choice(self.root)
            else:
                self.label.config(text="One or more methods could not be added.", foreground="red")
        else:
            self.label.config(text="Invalid batch, please check the batch key.", foreground="red")

    def add_method(self, access_token: str, method_file: str) -> int:
        """
        Adds an injection method to Directus and returns its ID if successful.

        Args:
            access_token (str): The JWT access token for authentication.
            method_file (str): The name of the method to add.

        Returns:
            int: The Directus ID of the added method, or -1 if it failed.
        """
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })

        url = "https://emi-collection.unifr.ch/directus/items/Injection_Methods/"
        payload = {"method_name": method_file}

        try:
            response = session.post(url=url, json=payload)
            response.raise_for_status()
            return int(response.json()["data"]["id"])
        except requests.RequestException as e:
            print(f"Failed to add method '{method_file}': {e}")
            return -1         
        
    def add_batch(self, access_token: str) -> int:
        """
        Creates a new batch entry in Directus and returns its ID.

        Args:
            access_token (str): The JWT access token for authentication.

        Returns:
            int: The Directus ID of the created batch, or -1 if it failed.
        """
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })

        # Extract future code to possibly create
        url = "https://emi-collection.unifr.ch/directus/items/Batches"
        column = "batch_id"
        params: Dict[str, Union[str, int, float, None]] = {"sort[]": f"-{column}", "limit": 1}
        session = requests.Session()
        response = session.get(url, params=params)
        last_value = response.json()["data"][0][column] if response.json()["data"] else "null"
        last_number = int(last_value.split("_")[1]) if last_value != "null" else 0
        first_number = last_number + 1
        self.new_batch = "batch_" f"{first_number:06d}" 

        # Fetch batches of type 6
        params = {"sort[]": f"{column}", "filter[batch_type][_eq]": 6}
        response = session.get(url, params=params)
        data = response.json()["data"]

        # Create a mapping dictionary and list of options for the dropdown
        batch_mapping = {f"New ({self.new_batch})": 0}  # "new" maps to ID 0
        batch_names = ["Select a batch"]  # Add a placeholder for no default selection
        batch_names.append(f"New ({self.new_batch})")  # Add "new batch" option

        for item in data:
            batch_mapping[item[column]] = item["id"]  # Map batch_id to id
            batch_names.append(item[column])  # Add human-readable batch_id to the dropdown

        payload = {
            "batch_id": self.new_batch,
            "batch_type": 6,
            "short_description": "ms batch",
            "description": "ms batch",
        }

        try:
            response = session.post(url=url, json=payload)
            response.raise_for_status()
            return int(response.json()["data"]["id"])
        except requests.RequestException as e:
            print(f"Failed to create batch: {e}")
            return -1
        
    def manage_choice(self, root: tk.Tk) -> None:
        """
        Launches the next window depending on the user's selected action: "new" or "csv".
        """
        self.label.config(text="Connect to Directus and adjust the parameters", foreground="black")

        if self.clicked_button == "new":
            new_batch_window = tk.Toplevel(root)
            new_batch_window.title("Create new batch")
            new_batch_instance = newBatch(new_batch_window)  
            new_batch_instance.pack(fill="both", expand=True)

        elif self.clicked_button == "csv":
            csv_batch_window = tk.Toplevel(root)
            csv_batch_window.minsize(300, 200)
            csv_batch_window.title("Import CSV batch")
            csv_batch_instance = csvBatch(csv_batch_window, root)
            csv_batch_instance.pack(fill="both", expand=True)
            
        else:
            self.label.config(text="Unknown error, please try again with other parameters", foreground="red")


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
        button_submit = ttk.Button(self, text="Submit", command=self.store_prefix)
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
