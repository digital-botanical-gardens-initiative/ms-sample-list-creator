import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Dict, List, Optional

from ms_sample_list_creator.implementations.result import Result

# from .new_sample_list import newBatch
from ms_sample_list_creator.structure import (
    Batch,
    Blank,
    Instrument,
    MassSpectrometry,
)
from ms_sample_list_creator.utils.directus_utils import (
    get_batches,
    get_instruments,
    test_batch,
)
from ms_sample_list_creator.utils.gui_utils import (
    build_data_selector,
    build_method_section,
    build_output_selector,
    build_standby_selector,
    build_submit_button,
    create_label_input_pair,
)

from .implementations.list_var import ListVar


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
        self.batch_id = tk.IntVar(value=-1)

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

        # Batch and instrument mapping for the combobox
        self.batch_mapping: Dict[str, int] = {}
        self.instrument_mapping: Dict[str, int] = {}

        self.build_gui()

    def build_gui(self) -> None:
        """
        Builds the main GUI elements: fields for user inputs and buttons.
        """

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
            right_var=self.instrument_name,
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
            right_var=self.batch_name,
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
        self.instrument_combobox.bind("<<ComboboxSelected>>", self.on_instrument_selected)

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
        self.batch_combobox.set("test")

        # Set select listener
        self.batch_combobox.bind("<<ComboboxSelected>>", self.on_batch_selected)

        # Create a frame for each section
        build_method_section(self)
        build_standby_selector(self)
        build_data_selector(self)
        build_output_selector(self)
        build_submit_button(self, self.validate_data)

    def on_instrument_selected(self, _: Optional[tk.Event] = None) -> None:
        """
        Called when an instrument is selected in the instrument Combobox.
        Updates the selected instrument ID.
        """
        # Get user selected entry
        selected_label = self.instrument_combobox.get()
        selected_id = self.instrument_mapping.get(selected_label, -1)

        print(f"Selected instrument: {selected_label}, ID: {selected_id}")

        self.instrument_combobox.set(selected_label)

        self.instrument_name.set(selected_label)
        self.instrument_id.set(selected_id)

    def on_batch_selected(self, _: Optional[tk.Event] = None) -> None:
        """
        Called when a batch is selected in the batch Combobox.
        Updates the selected batch ID or handles creation of a new batch.
        """
        # Get user selected entry
        selected_label = self.batch_combobox.get()
        selected_id = self.batch_mapping.get(selected_label, -1)

        print(f"Selected batch: {selected_label}, ID: {selected_id}")

        self.batch_name.set(selected_label)
        self.batch_id.set(selected_id)

    def validate_data(self) -> None:
        try:
            # -------------Credentials------------------#

            # # Get directus credentials
            # directus_credentials = DirectusCredentials(
            #     username=self.directus_username.get(),
            #     password=self.directus_password.get(),
            # )

            # # check that credentials are valid
            # cred_result: Result = test_credentials(directus_credentials)

            # if not cred_result.is_ok:
            #     messagebox.showerror("Directus connection", cred_result.error)
            #     return

            # access_token = cred_result.value

            # -------------MS------------------#

            mass_spectrometry = MassSpectrometry(
                operator_initials=self.operator_initials.get(),
                injection_volume=int(self.injection_volume.get()),
            )
            print("Mass Spectrometry:", mass_spectrometry)

            # -------------Instrument------------------#

            instrument = Instrument(name=self.instrument_name.get(), identifier=self.instrument_id.get())

            if instrument.identifier < 1:
                messagebox.showerror("No instrument", "Please select an instrument")
                return

            # -------------Batch------------------#

            # Check that batch is valid
            batch = Batch(name=self.batch_name.get(), identifier=self.batch_id.get())

            batch_result: Result = test_batch(batch, access_token)

            if not batch_result.is_ok:
                messagebox.showerror("Batch validation", batch_result.error)
                return

            # Update batch if it was updated
            batch = batch_result.value

            # -------------Blank------------------#

            blank = Blank(
                blank_name=self.blank_name.get(),
                blank_position=self.blank_position.get(),
                blank_pre=int(self.blank_pre.get()),
                blank_post=int(self.blank_post.get()),
            )
            print("Blank:", blank)

            # meth_result: Result = get_methods(methods_list=self.method_list_path.get(), token=access_token)

            # if not meth_result.is_ok:
            #     messagebox.showerror("Method validation", meth_result.error)
            #     return

            # methods: Method = meth_result.value

            # path = Path(
            #     methods=methods,
            #     standby=self.standby_path.get(),
            #     data=self.data_path.get(),
            #     output=self.output_path.get(),
            # )
            # print("Path:", path)
            # rack = Rack(
            #     column=self.rack_columns.get(),
            #     row=self.rack_rows.get(),
            # )
            # print("Rack:", rack)

        except ValueError as e:
            messagebox.showerror("Invalid input", f"Invalid input: {e}")
            return None

    # def handle_successful_login(self, data: dict) -> None:
    #     print("handle_successful_login called")
    #     """
    #     Handles the actions after a successful login to Directus.

    #     Args:
    #         data (dict): The response data containing the access token.

    #     Returns:
    #         None
    #     """

    #     selected_batch_label = self.batch_combobox.get()

    #     batch_id = self.add_batch(self.access_token) if selected_batch_label == "__NEW__" else selected_batch_label

    #     print(batch_id)

    #     if batch_id in (-1, 0):
    #         self.label.config(text="Invalid batch, please check the batch key.", foreground="red")
    #         return

    #     # Attempt to add each method file
    #     method_keys: List[int] = []
    #     all_success = True
    #     for method_file in self.method_list_path.get():
    #         key = self.add_method(self.access_token, method_file)
    #         if key == -1:
    #             all_success = False
    #         method_keys.append(key)

    #     if all_success:
    #         self.method_keys = method_keys
    #         self.manage_choice(self.root)
    #     else:
    #         self.label.config(text="No method could be added (or all already existed).", foreground="red")

    # def manage_choice(self, root: tk.Tk) -> None:
    #     print(28)

    # """
    # Launches the next window depending on the user's selected action: "new" or "csv".
    # """
    # print("manage_choice called")
    # self.label.config(text="Connect to Directus and adjust the parameters", foreground="black")

    # user_data = self.get_user_data()

    # # Check that all data is valid
    # if not self.are_all_values_present(user_data):
    #     self.label.config(text="Données manquantes ou invalides. Vérifiez tous les champs.", foreground="red")
    #     return

    # if self.clicked_button == "new":
    #     new_batch_window = tk.Toplevel(root)
    #     new_batch_window.title("Create new batch")
    #     new_batch_instance = newBatch(new_batch_window, session_data=self.session_data)
    #     new_batch_instance.pack(fill="both", expand=True)

    # else:
    #     self.label.config(text="Unknown error, please try again with other parameters", foreground="red")
