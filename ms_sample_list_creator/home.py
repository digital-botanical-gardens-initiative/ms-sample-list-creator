import tkinter as tk
from tkinter import messagebox
from typing import Any, Dict, List, Optional

from ttkbootstrap import ttk

from ms_sample_list_creator.implementations.list_var import ListVar
from ms_sample_list_creator.implementations.result import Result
from ms_sample_list_creator.sample_list import SampleList
from ms_sample_list_creator.structure import (
    Batch,
    Blank,
    DirectusCredentials,
    Instrument,
    MassSpectrometry,
    Method,
    ProjectPath,
    Rack,
)
from ms_sample_list_creator.token_manager import TokenManager, validate_credentials
from ms_sample_list_creator.utils.directus_utils import (
    get_batches,
    get_instruments,
    get_methods,
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
        self.blank_name = tk.StringVar()
        self.blank_position = tk.StringVar()

        # Batch information
        self.batch_name = tk.StringVar()
        self.batch_id = tk.IntVar(value=-1)

        # File paths
        self.method_list_path: ListVar = ListVar([])
        self.standby_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.data_path = tk.StringVar()

        # Directus credentials
        self.directus_username = tk.StringVar()
        self.directus_password = tk.StringVar()

        # Operator
        self.operator_initials = tk.StringVar()

        # Mass spectrometer ID
        self.instrument_name = tk.StringVar()
        self.instrument_id = tk.IntVar()

        # Injection volume
        self.injection_volume = tk.DoubleVar(value=1.0)
        self.rack_columns = tk.IntVar(value=9)
        self.rack_rows = tk.IntVar(value=6)

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
        instrument_result = get_instruments()

        if not instrument_result.is_ok:
            messagebox.showerror("Instruments loading", instrument_result.error)
            return
        instruments = instrument_result.value

        if not isinstance(instruments, list):
            messagebox.showerror("Instruments loading", "No instruments found.")
            return

        # Create instruments list
        instrument_values = []

        # Populate instruments list and instrument mapping
        for instrument in instruments:
            instrument_values.append(instrument.name)
            self.instrument_mapping[instrument.name] = instrument.identifier

        # Set instruments
        self.instrument_combobox["values"] = instrument_values
        if isinstance(self.instrument_combobox, ttk.Combobox):
            self.instrument_combobox.set("Select an instrument")
        else:
            self.instrument_combobox.delete(0, tk.END)
            self.instrument_combobox.insert(0, "Select an instrument")

        # Set select listener
        self.instrument_combobox.bind("<<ComboboxSelected>>", self.on_instrument_selected)

        # Load batches from directus
        batches_result = get_batches()

        if not batches_result.is_ok:
            messagebox.showerror("Batches loading", batches_result.error)
            return

        if not isinstance(batches_result.value, list):
            messagebox.showerror("Batches loading", "No batches found.")
            return

        batches = batches_result.value

        # Create batches list
        batch_values = []

        # Populate batches list and batch mapping
        for batch in batches:
            batch_values.append(batch.name)
            self.batch_mapping[batch.name] = batch.identifier

        # Set batches
        self.batch_combobox["values"] = batch_values
        if isinstance(self.batch_combobox, ttk.Combobox):
            self.batch_combobox.set("Select a batch")
        else:
            self.batch_combobox.delete(0, tk.END)
            self.batch_combobox.insert(0, "Select a batch")

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

        if isinstance(self.instrument_combobox, ttk.Combobox):
            self.instrument_combobox.set(selected_label)
        else:
            self.instrument_combobox.delete(0, tk.END)
            self.instrument_combobox.insert(0, selected_label)

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

        self.batch_name.set(selected_label)
        self.batch_id.set(selected_id)

    def validate_data(self) -> None:
        try:
            # -------------Credentials------------------#

            # Get directus credentials
            credentials = DirectusCredentials(
                username=self.directus_username.get(),
                password=self.directus_password.get(),
            )

            # check that credentials are valid
            result = validate_credentials(credentials)

            if not result.is_ok:
                messagebox.showerror("Login Failed", f"Invalid Directus credentials :\n{result.error}")
                return

            TokenManager(credentials)

            # -------------MS------------------#

            mass_spectrometry = MassSpectrometry(
                operator_initials=self.operator_initials.get(),
                injection_volume=self.injection_volume.get(),
            )

            # -------------Instrument------------------#

            instrument = Instrument(name=self.instrument_name.get(), identifier=self.instrument_id.get())

            if instrument.identifier < 1:
                messagebox.showerror("No instrument", "Please select an instrument")
                return

            # -------------Batch------------------#

            # Check that batch is valid
            batch = Batch(name=self.batch_name.get(), identifier=self.batch_id.get())

            batch_result: Result = test_batch(batch)

            if not batch_result.is_ok:
                messagebox.showerror("Batch validation", batch_result.error)
                return

            if not batch_result.value:
                messagebox.showerror("Batch validation", "Batch not found or invalid.")
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

            # -------------Methods------------------#

            if not self.method_list_path.get():
                messagebox.showerror("Method validation", "Please select at least one method file.")
                return

            meth_result: Result = get_methods(methods_list=self.method_list_path.get())

            if not meth_result.is_ok:
                messagebox.showerror("Method validation", meth_result.error)
                return

            if not isinstance(meth_result.value, list):
                messagebox.showerror("Method validation", "No methods found or invalid format.")
                return

            methods: List[Method] = meth_result.value

            # -------------ProjectPath------------------#

            paths = ProjectPath(
                methods=methods,
                standby=self.standby_path.get().replace(".meth", ""),
                data=self.data_path.get(),
                output=self.output_path.get(),
            )

            # -------------Rack------------------#

            rack = Rack(
                column=self.rack_columns.get(),
                row=self.rack_rows.get(),
            )

            # -------------Launch the sample list creation------------------#
            self.lauch_sample_list_creation(
                credentials=credentials,
                mass_spectrometry=mass_spectrometry,
                instrument=instrument,
                batch=batch,
                blank=blank,
                paths=paths,
                methods=methods,
                rack=rack,
            )

        except ValueError as e:
            messagebox.showerror("Invalid input", f"Invalid input: {e}")
            return None
        except Exception as e:
            messagebox.showerror("Unexpected error", str(e))
            return None

    def lauch_sample_list_creation(
        self,
        credentials: DirectusCredentials,
        mass_spectrometry: MassSpectrometry,
        instrument: Instrument,
        batch: Batch,
        blank: Blank,
        methods: List[Method],
        paths: ProjectPath,
        rack: Rack,
    ) -> None:
        """
        Launches the sample list creation process with the provided parameters.

        Args:
            credentials (DirectusCredentials): The Directus credentials.
            mass_spectrometry (MassSpectrometry): The mass spectrometry parameters.
            instrument (Instrument): The selected instrument.
            batch (Batch): The selected batch.
            blank (Blank): The blank parameters.
            methods (List[Method]): The list of methods to be used.
            paths (ProjectPath): The project paths for standby, data, and output.
            rack (Rack): The rack configuration.

        Returns:
            None
        """

        self.root.withdraw()

        sample_list_window = tk.Toplevel(self)
        sample_list_window.title("Create Sample List")
        sample_list_instance = SampleList(
            sample_list_window,
            root=self.root,
            credentials=credentials,
            mass_spectrometry=mass_spectrometry,
            instrument=instrument,
            batch=batch,
            blank=blank,
            paths=paths,
            methods=methods,
            rack=rack,
        )

        sample_list_instance.pack(fill=tk.BOTH, expand=True)
