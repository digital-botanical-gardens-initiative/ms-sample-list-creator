import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Dict, Optional, List
from pathlib import Path

import requests

from .implementations.list_var import ListVar

# from .new_sample_list import newBatch
from .structure import Blank, DirectusCredentials, MassSpectrometry, Method, Batch, Instrument, Rack
from ms_sample_list_creator.utils.gui_utils import create_label_input_pair, build_method_section, build_data_selector, build_output_selector, build_standby_selector, build_submit_button
from ms_sample_list_creator.utils.directus_utils import get_batches, get_instruments


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

        ttk.Frame.__init__(self, root, *args, **kwargs)

        self.init_vars()

    def init_vars(self) -> None:
        """
        Sets the variables to their default values.
        """
        # Blank information
        self.blank_pre = tk.StringVar(value=str(4))
        self.blank_post = tk.StringVar(value=str(3))
        self.blank_name = tk.StringVar(value="blank")
        self.blank_position = tk.StringVar(value="G:A1")

        # Batch information
        self.batch_name = tk.StringVar()
        self.batch_id = tk.IntVar()

        # File paths
        self.method_list_path: ListVar = ListVar([])
        self.standby_path = tk.StringVar(
            value="/home/heloise/repositories/ms-sample-list-creator/tests_files/stdby.meth"
        )
        self.output_path = tk.StringVar(value="/home/heloise/repositories/ms-sample-list-creator")
        self.data_path = tk.StringVar(value="/home/heloise/repositories/ms-sample-list-creator")

        # Directus credentials
        self.directus_username = tk.StringVar(value="test.user@gmail.com")
        self.directus_password = tk.StringVar(value="test")

        # Operator
        self.operator_initials = tk.StringVar(value="CVOL")

        # Mass spectrometer ID
        self.instrument_name = tk.StringVar()
        self.instrument_id = tk.IntVar()

        # Injection volume
        self.injection_volume = tk.StringVar(value=str(1))
        self.rack_columns = tk.StringVar(value=str(9))
        self.rack_rows = tk.StringVar(value=str(6))

        # Batch mapping for the combobox
        self.batch_mapping: Dict[str, int] = {}

        self.build_gui()

    def build_gui(self) -> None:
        """
        Builds the main GUI elements: fields for user inputs and buttons.
        """

        # Top label to display errors
        self.label = ttk.Label(self.root, text="", foreground="red")
        self.label.pack(anchor="w", pady=5, padx=10)

        # Directus password and username
        create_label_input_pair(
            parent=self,
            left_label_text="Directus username:",
            right_label_text="Directus password:",
            left_var=self.directus_username,
            right_var=self.directus_password,
            show_right="*",
        )

        # Operator initials and instrument ID
        _, self.instrument_combobox = create_label_input_pair(
            parent=self,
            left_label_text="Operator's initials:",
            right_label_text="Mass spectrometer ID:",
            left_var=self.operator_initials,
            right_var=self.instrument_id,
            right_type="combobox",
            right_values=[],
        )

        # Rack dimensions
        create_label_input_pair(
            parent=self,
            left_label_text="Rack columns:",
            right_label_text="Rack rows:",
            left_var=self.rack_columns,
            right_var=self.rack_rows,
        )

        # Blank information
        create_label_input_pair(
            parent=self,
            left_label_text="Blank name:",
            right_label_text="Blank position:",
            left_var=self.blank_name,
            right_var=self.blank_position,
        )
        create_label_input_pair(
            parent=self,
            left_label_text="Blank before samples:",
            right_label_text="Blank after samples:",
            left_var=self.blank_pre,
            right_var=self.blank_post,
        )

        # Injection volume and batch
        _, self.batch_combobox = create_label_input_pair(
            parent=self,
            left_label_text="Injection Volume (µL):",
            right_label_text="Batch:",
            left_var=self.injection_volume,
            right_var=self.batch_id,
            right_type="combobox",
            right_values=[],  # Empty for now
        )

        # Load instruments from directus
        instruments: List[Instrument] = get_instruments()

        # Create instruments list
        instrument_values = []

        # Populate instruments list and instrument mapping
        for instrument in instruments:
            instrument_values.append(instrument.name)
            self.instrument_mapping[instrument.name] = instrument.identifier

        # Set instruments
        self.instrument_combobox["values"] = instrument_values

        # Set select listener
        self.instrument_combobox("<<ComboboxSelected>>", self.on_instrument_selected)

        # Load batches from directus
        batches: List[Batch] = get_batches()

        # Create batches list
        batch_values = []
        
        # Populate batches list and batch mapping
        for batch in batches:
            batch_values.append(batch.name)
            self.batch_mapping[batch.name] = batch.identifier

        # Set batches
        self.batch_combobox["values"] = batch_values

        # Set select listener
        self.batch_combobox.bind("<<ComboboxSelected>>", self.on_batch_selected)

        # Create a frame for each section
        build_method_section(self)
        build_standby_selector(self)
        build_data_selector(self)
        build_output_selector(self)
        build_submit_button(self, self.validate_data)

    def on_batch_selected(self, _: Optional[tk.Event] = None) -> None:
        """
        Called when a batch is selected in the batch Combobox.
        Updates the selected batch ID or handles creation of a new batch.
        """
        # Get user selected entry
        selected_label = self.batch_combobox.get()
        selected_id = self.batch_mapping.get(selected_label, -1)

        self.batch_id.set(selected_id)

    def on_instrument_selected(self, _: Optional[tk.Event] = None) -> None:
        """
        Called when an instrument is selected in the instrument Combobox.
        Updates the selected instrument ID.
        """

    def validate_data(self) -> None:
        try:
            instrument = Instrument(
                name=self.instrument_name.get(),
                identifier=self.instrument_id.get()
            )
            print("Instrument:", instrument)
            batch = Batch(
                name=self.batch_name.get(),
                identifier=self.batch_id.get()
            )
            print("Batch:", batch)
            blank = Blank(
                blank_name=self.blank_name.get(),
                blank_position=self.blank_position.get(),
                blank_pre=int(self.blank_pre.get()),
                blank_post=int(self.blank_post.get()),
            )
            print("Blank:", blank)
            path = Path(
                methods=self.method_list_path.get(),
                standby=self.standby_path.get(),
                data=self.data_path.get(),
                output=self.output_path.get(),
            )
            print("Path:", path)
            rack = Rack(
                column=self.rack_columns.get(),
                row=self.rack_rows.get(),
            )
            print("Rack:", rack)
            mass_spectrometry = MassSpectrometry(
                operator_initials=self.operator_initials.get(),
                injection_volume=int(self.injection_volume.get()),
            )
            print("Mass Spectrometry:", mass_spectrometry)
            directus_credentials = DirectusCredentials(
                username=self.directus_username.get(),
                password=self.directus_password.get(),
            )
            print("Directus Credentials:", directus_credentials)

            self.attempt_connection()

        except ValueError as e:
            messagebox.showerror("Invalid input", f"Invalid input: {e}")
            return None

    def attempt_connection(self) -> None:
        """
        Attempts to connect to Directus using the provided user data.

        If the connection is successful, the access token is stored.

        Args:
            user_data (dict): The dictionary containing the necessary user data.

        Returns:
            None
        """

        base_url = "https://emi-collection.unifr.ch/directus"
        login_url = base_url + "/auth/login"

        session = requests.Session()

        # Get Directus credentials from the dataclass
        username = self.directus_username.get()
        password = self.directus_password.get()

        try:
            response = session.post(login_url, json={"email": username, "password": password})
            response.raise_for_status()

            # If connection is successful
            self.handle_successful_login(response.json())

        except requests.HTTPError as e:
            self.label.config(text="Connection to Directus failed, verify your credentials", foreground="red")
            print(f"HTTPError during Directus login: {e}")

        except requests.RequestException as e:
            self.label.config(text="Network error during connection to Directus", foreground="red")
            print(f"RequestException during Directus login: {e}")

    def handle_successful_login(self, data: dict) -> None:
        print("handle_successful_login called")
        """
        Handles the actions after a successful login to Directus.

        Args:
            data (dict): The response data containing the access token.

        Returns:
            None
        """

        self.access_token = data["data"]["access_token"]
       
        selected_batch_label = self.batch_combobox.get()

        if selected_batch_label == "__NEW__":
            batch_id = self.add_batch(self.access_token)
        else:
            batch_id = selected_batch_label
        
        print(batch_id)

        if batch_id in (-1, 0):
            self.label.config(text="Invalid batch, please check the batch key.", foreground="red")
            return

        self.batch_id = batch_id

        # Attempt to add each method file
        method_keys: List[int] = []
        all_success = True
        for method_file in self.method_list_path.get():
            key = self.add_method(self.access_token, method_file)
            if key == -1:
                all_success = False
            method_keys.append(key)

        if all_success:
            self.method_keys = method_keys
            self.manage_choice(self.root)
        else:
            self.label.config(text="No method could be added (or all already existed).", foreground="red")

    def add_method(self, access_token: str, method_file: str) -> int:
        print("add_method called")
        """
        Adds an injection method to Directus and returns its ID if successful.

        If the method already exists, fetches its ID instead of failing.

        Args:
            access_token (str): The JWT access token for authentication.
            method_file (str): The name of the method to add.

        Returns:
            int: The Directus ID of the method, or -1 if it failed completely.
        """

        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"})

        base_url = "https://emi-collection.unifr.ch/directus"
        method_name = Path(method_file).stem
        payload = {"method_name": method_name}

        try:
            # Try posting the new method
            response = session.post(f"{base_url}/items/Injection_Methods/", json=payload)
            response.raise_for_status()
            return int(response.json()["data"]["id"])

        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 400:
                # Likely already exists — try to fetch it
                print(f"Method '{method_name}' already exists. Fetching ID...")

                get_response = session.get(
                    f"{base_url}/items/Injection_Methods",
                    params={"filter[method_name][_eq]": method_name}
                )

                if get_response.ok:
                    data = get_response.json().get("data")
                    if data:
                        return int(data[0]["id"])
                    else:
                        print(f"Method '{method_name}' not found despite 400 error.")
                else:
                    print(f"Failed to fetch existing method '{method_name}'. Status code: {get_response.status_code}")
                    print("Response content:", get_response.text)
            else:
                print(f"Failed to add method '{method_file}': {e}")
                if e.response is not None:
                    print("Response content:", e.response.text)

        return -1

    def add_batch(self, access_token: str) -> Batch:
        print(27)
        """
        Creates a new batch entry in Directus and returns its ID.

        Args:
            access_token (str): The JWT access token for authentication.

        Returns:
            str: The Directus UUID of the created batch, or "" if it failed.
        """
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"})

        # Get next batch number
        url = "https://emi-collection.unifr.ch/directus/items/Batches"
        params = {"sort[]": "-batch_id", "limit": 1}

        try:
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            json_data = response.json()
            last_value: str = json_data["data"][0]["batch_id"] if json_data["data"] else "null"
            last_number = int(last_value.split("_")[1]) if last_value != "null" else 0
        except (requests.RequestException, IndexError, ValueError) as e:
            print(f"Failed to determine next batch number: {e}")
            return Batch(
                name = "None",
                identifier = -1
            )
        
        new_batch = f"batch_{last_number + 1:06d}"

        # Create payload and post to Directus
        payload = {
            "batch_id": new_batch,
            "batch_type": 6,
            "short_description": "ms batch",
            "description": "ms batch",
        }

        try:
            response = session.post(url=url, json=payload, timeout=10)
            response.raise_for_status()
            return Batch(
                name = new_batch,
                identifier = int(response.json()["data"]["id"])
            )
        except requests.RequestException as e:
            print(f"Failed to create batch: {e}")
            return Batch(
                name = "None",
                identifier = -1
            )

    def manage_choice(self, root: tk.Tk) -> None:
        print(28)

    #     """
    #     Launches the next window depending on the user's selected action: "new" or "csv".
    #     """
    #     print("manage_choice called")
    #     self.label.config(text="Connect to Directus and adjust the parameters", foreground="black")

    #     user_data = self.get_user_data()

    #     # Check that all data is valid
    #     if not self.are_all_values_present(user_data):
    #         self.label.config(text="Données manquantes ou invalides. Vérifiez tous les champs.", foreground="red")
    #         return

    #     if self.clicked_button == "new":
    #         new_batch_window = tk.Toplevel(root)
    #         new_batch_window.title("Create new batch")
    #         new_batch_instance = newBatch(new_batch_window, session_data=self.session_data)
    #         new_batch_instance.pack(fill="both", expand=True)

    #     elif self.clicked_button == "csv":
    #         csv_batch_window = tk.Toplevel(root)
    #         csv_batch_window.minsize(300, 200)
    #         csv_batch_window.title("Import CSV batch")
    #         csv_batch_instance = csvBatch(csv_batch_window, root)
    #         csv_batch_instance.pack(fill="both", expand=True)

    #     else:
    #         self.label.config(text="Unknown error, please try again with other parameters", foreground="red")
