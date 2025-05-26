import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.ttk import Combobox
from typing import Any, Dict, Optional, cast

import requests

from .implementations.list_var import ListVar

# from .new_sample_list import newBatch
from .structure import Blank, DirectusCredentials, MassSpectrometry, Methods
from .utils import gui_utils


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
        self.batch_key = tk.StringVar()

        # File paths
        self.method_files: ListVar = ListVar([])
        self.standby_file = tk.StringVar(
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
        self.instrument_id = tk.StringVar(value="inst_000002")

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
        gui_utils.create_label_input_pair(
            parent=self,
            left_label_text="Directus username:",
            right_label_text="Directus password:",
            left_var=self.directus_username,
            right_var=self.directus_password,
            show_right="*",
        )

        # Operator initials and mass spectrometer ID
        self.inst_list = ["Test1", "Test2", "Test3"]
        gui_utils.create_label_input_pair(
            parent=self,
            left_label_text="Operator's initials:",
            right_label_text="Mass spectrometer ID:",
            left_var=self.operator_initials,
            right_var=self.instrument_id,
            right_type="combobox",
            right_values=self.inst_list,  # TODO change to the real inst list
        )

        # Rack dimensions
        gui_utils.create_label_input_pair(
            parent=self,
            left_label_text="Rack columns:",
            right_label_text="Rack rows:",
            left_var=self.rack_columns,
            right_var=self.rack_rows,
        )

        # Blank information
        gui_utils.create_label_input_pair(
            parent=self,
            left_label_text="Blank name:",
            right_label_text="Blank position:",
            left_var=self.blank_name,
            right_var=self.blank_position,
        )
        gui_utils.create_label_input_pair(
            parent=self,
            left_label_text="Blank before samples:",
            right_label_text="Blank after samples:",
            left_var=self.blank_pre,
            right_var=self.blank_post,
        )

        # Injection volume and batch
        _, self.batch_combobox = gui_utils.create_label_input_pair(
            parent=self,
            left_label_text="Injection Volume (µL):",
            right_label_text="Batch:",
            left_var=self.injection_volume,
            right_var=self.batch_key,
            right_type="combobox",
            right_values=[],  # Empty for now
        )

        # Load batches from directus into the combobox
        gui_utils.get_batches(
            batch_combobox=cast(Combobox, self.batch_combobox),
            batch_key=self.batch_key,
            on_batch_selected=self.on_batch_selected,
            set_mapping=lambda mapping: setattr(self, "batch_mapping", mapping),
        )

        # Create a frame for each section
        gui_utils.build_method_section(self)
        gui_utils.build_standby_selector(self)
        gui_utils.build_data_selector(self)
        gui_utils.build_output_selector(self)
        gui_utils.build_submit_button(self, self.validate_data)

    def on_batch_selected(self, event: Optional[tk.Event] = None) -> None:
        """
        Called when a batch is selected in the batch Combobox.
        Updates the selected batch ID or handles creation of a new batch.
        """
        selected_label = self.batch_combobox.get()
        selected_id = self.batch_mapping.get(selected_label)

        print(f"Selected batch: {selected_label} -> {selected_id}")

        if selected_label == "Select a batch":
            self.label.config(text="Please select a batch.")
            self.batch_key.set("")
        elif selected_id == "__NEW__":
            self.label.config(text="You selected a new batch")  # TODO : handle creation of a new batch
        else:
            self.label.config(text="")
            self.batch_key.set(str(selected_id))

    def validate_data(self) -> None:
        try:
            blank = Blank(
                blank_name=self.blank_name.get(),
                blank_position=self.blank_position.get(),
                blank_pre=int(self.blank_pre.get()),
                blank_post=int(self.blank_post.get()),
            )
            print("Blank:", blank)
            mass_spectrometry = MassSpectrometry(
                rack_columns=int(self.rack_columns.get()),
                rack_rows=int(self.rack_rows.get()),
                instrument_id=self.instrument_id.get(),
                operator_initials=self.operator_initials.get(),
                injection_volume=int(self.injection_volume.get()),
                batch_key=int(self.batch_key.get()),
                data_path=self.data_path.get(),
                output_path=self.output_path.get(),
                standby_file=self.standby_file.get(),
            )
            print("Mass Spectrometry:", mass_spectrometry)
            methods = Methods(
                method_files=self.method_files.get(),
                method_keys=[1, 2, 3],
            )
            print("Methods:", methods)
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
        # # Get the instrument key based on the ms_id
        # instrument_key = self.get_instrument_key(user_data["ms_id"])
        # self.session_data.instrument_key = instrument_key

        # # Store the instrument key in the environment if valid
        # if instrument_key != -1:
        #     os.environ["INSTRUMENT_KEY"] = str(self.session_data.instrument_key)

        #     # Define the Directus base URL
        #     base_url = "https://emi-collection.unifr.ch/directus"
        #     login_url = base_url + "/auth/login"

        #     # Create a session object for making requests
        #     session = requests.Session()

        #     # Recover connection identifiers from dataclass
        #     username = default_vars.directus_username
        #     password = default_vars.directus_password

        #     # Send a POST request to login
        #     response = session.post(login_url, json={"email": username, "password": password})

        #     if response.status_code == 200:
        #         self.handle_successful_login(response.json())
        #     else:
        #         self.label.config(text="Connection to Directus failed, verify your credentials", foreground="red")
        # else:
        #     self.label.config(text="Invalid instrument key, please verify your MS_ID", foreground="red")

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

    # def get_instrument_key(self, ms_id: str) -> int:
    #     print(24)
    #     """
    #     Retrieves the primary key of the instrument based on the MS_ID.

    #     Args:
    #         ms_id (str): The mass spectrometer ID.

    #     Returns:
    #         int: The instrument key, or -1 if not found.
    #     """
    #     ms_id = default_vars.instrument_id
    #     return utils.get_primary_key(
    #         "https://emi-collection.unifr.ch/directus/items/Instruments", ms_id, "instrument_id"
    #     )

    def handle_successful_login(self, data: dict) -> None:
        print(25)
        """
        Handles the actions after a successful login to Directus.

        Args:
            data (dict): The response data containing the access token.

        Returns:
            None
        """

    #     self.session_data.access_token = data["data"]["access_token"]
    #     os.environ["ACCESS_TOKEN"] = self.session_data.access_token

    #     selected_batch_label = self.batch_combobox.get()
    #     batch = self.batch_mapping.get(selected_batch_label, -1)
    #     print("Selected batch:", selected_batch_label)
    #     print("Mapped batch ID:", batch)

    #     if batch == "__NEW__":
    #         batch = self.add_batch(self.session_data.access_token)

    #     if batch in (-1, 0):
    #         self.label.config(text="Invalid batch, please check the batch key.", foreground="red")
    #         return

    #     self.session_data.batch_key = batch
    #     default_vars.batch_key = batch
    #     os.environ["BATCH_KEY"] = str(self.session_data.batch_key)

    #     method_keys = []
    #     all_success = True

    #     # Attempt to add each method file
    #     for method_file in default_vars.method_files:
    #         key = self.add_method(self.session_data.access_token, method_file)
    #         if key == -1:
    #             all_success = False
    #         method_keys.append(key)

    #     # If all methods were successfully added, store the method keys
    #     if all_success:
    #         self.session_data.method_keys = method_keys
    #         os.environ["INJECTION_METHOD_KEYS"] = ",".join(map(str, self.session_data.method_keys))
    #         self.manage_choice(self.root)
    #     else:
    #         self.label.config(text="One or more methods could not be added.", foreground="red")

    # def add_method(self, access_token: str, method_file: str) -> int:
    #     print(26)
    #     """
    #     Adds an injection method to Directus and returns its ID if successful.

    #     If the method already exists, fetches its ID instead of failing.

    #     Args:
    #         access_token (str): The JWT access token for authentication.
    #         method_file (str): The name of the method to add.

    #     Returns:
    #         int: The Directus ID of the method, or -1 if it failed completely.
    #     """

    #     session = requests.Session()
    #     session.headers.update({"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"})

    #     base_url = "https://emi-collection.unifr.ch/directus"
    #     method_name = Path(method_file).stem
    #     payload = {"method_name": method_name}

    #     try:
    #         # Try posting the new method
    #         response = session.post(f"{base_url}/items/Injection_Methods/", json=payload)
    #         response.raise_for_status()
    #         return int(response.json()["data"]["id"])

    #     except requests.HTTPError as e:
    #         # If error 400 (conflict): method probably already present
    #         if e.response is not None and e.response.status_code == 400:
    #             print(f"Method '{method_name}' already exists, trying to fetch existing ID...")

    #             # Try to retrieve it using a GET request with a filter
    #             get_response = session.get(
    #                 f"{base_url}/items/Injection_Methods", params={"filter[method_name][_eq]": method_name}
    #             )
    #             if get_response.ok:
    #                 data = get_response.json().get("data")
    #                 if data:
    #                     return int(data[0]["id"])
    #                 else:
    #                     print(f"Method '{method_name}' not found even though it was expected.")
    #         else:
    #             print(f"Failed to add method '{method_file}': {e}")
    #             if e.response is not None:
    #                 print("Response content:", e.response.text)

    #     return -1

    # def add_batch(self, access_token: str) -> str:
    #     print(27)
    #     """
    #     Creates a new batch entry in Directus and returns its ID.

    #     Args:
    #         access_token (str): The JWT access token for authentication.

    #     Returns:
    #         str: The Directus UUID of the created batch, or "" if it failed.
    #     """
    #     session = requests.Session()
    #     session.headers.update({"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"})

    #     # Get next batch number
    #     url = "https://emi-collection.unifr.ch/directus/items/Batches"
    #     column = "batch_id"
    #     params = {"sort[]": f"-{column}", "limit": 1}
    #     response = session.get(url, params=params)
    #     json_data = response.json()
    #     last_value: str = json_data["data"][0][column] if json_data["data"] else "null"
    #     last_number = int(last_value.split("_")[1]) if last_value != "null" else 0
    #     first_number = last_number + 1
    #     self.new_batch = f"batch_{first_number:06d}"

    #     # Fetch batches of type 6
    #     params = {"sort[]": f"{column}", "filter[batch_type][_eq]": 6}
    #     response = session.get(url, params=params)
    #     data = response.json()["data"]

    #     # Create a mapping dictionary and list of options for the dropdown
    #     batch_mapping = {f"New ({self.new_batch})": 0}  # "new" maps to ID 0
    #     batch_names = ["Select a batch"]  # Add a placeholder for no default selection
    #     batch_names.append(f"New ({self.new_batch})")  # Add "new batch" option

    #     for item in data:
    #         batch_id = item[column]  # column = "batch_id"
    #         directus_id = item["id"]
    #         batch_mapping[batch_id] = directus_id
    #         batch_names.append(batch_id)

    #     self.batch_mapping = batch_mapping

    #     payload = {
    #         "batch_id": self.new_batch,
    #         "batch_type": 6,
    #         "short_description": "ms batch",
    #         "description": "ms batch",
    #     }

    #     try:
    #         response = session.post(url=url, json=payload)
    #         response.raise_for_status()
    #         return int(response.json()["data"]["id"])
    #     except requests.RequestException as e:
    #         print(f"Failed to create batch: {e}")
    #         return ""

    # def manage_choice(self, root: tk.Tk) -> None:
    #     print(28)

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
