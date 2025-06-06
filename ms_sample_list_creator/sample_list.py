import csv
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from typing import List, Optional, cast

import ttkbootstrap as tb
from ttkbootstrap import ttk

from ms_sample_list_creator.askboxprefixwindow import AskBoxPrefixWindow
from ms_sample_list_creator.structure import (
    Batch,
    Blank,
    DirectusCredentials,
    Instrument,
    MassSpectrometry,
    Method,
    ProjectPath,
    Rack,
    SampleContainer,
    SampleData,
    SampleListData,
)
from ms_sample_list_creator.utils.directus_utils import get_aliquot, insert_ms_sample


class SampleList(ttk.Frame):
    """
    Class to create a sample list for mass spectrometry analysis.
    This class provides a GUI for users to input sample data, add samples to a list,
    and submit the list to a Directus database.
    """

    def __init__(
        self,
        window: tk.Toplevel,
        root: tk.Tk,
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
        Initializes an instance of the class.

        Args:
            parent(tk.Tk): The parent widget or window where this frame will be placed.

        Returns:
            None
        """
        super().__init__(window)

        # Store the prefix
        self.prefix: Optional[str] = None

        # Store lists of samples and blanks
        self.pre_blank: List[SampleListData] = []
        self.blk_sample: List[SampleListData] = []
        self.samples: List[SampleListData] = []
        self.post_blank: List[SampleListData] = []
        self.standby: List[SampleListData] = []

        # Make variables accessible inside the class
        self.window = window
        self.root = root
        self.credentials = credentials
        self.mass_spectrometry = mass_spectrometry
        self.instrument = instrument
        self.batch = batch
        self.blank = blank
        self.methods = methods
        self.paths = paths
        self.rack = rack

        # Reattribute cross icon
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Add internal counters for the rack position
        self.current_row: int = 1
        self.current_position: int = 1

        self.setup_view()

    def setup_view(self) -> None:
        """
        Sets up the view for the sample list creation window.
        This includes creating the treeview for displaying samples,
        input fields for sample data, and buttons for adding samples
        and submitting the list.
        """

        # Setup treeview for displaying samples
        self.treeview = tb.Treeview(self, bootstyle="secondary", show="headings")
        self.treeview.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree = self.treeview

        # Define columns for the treeview
        columns = (
            "aliquot_id",
            "operator",
            "ms_id",
            "File Name",
            "Path",
            "Instrument Method",
            "Position",
            "Inj Vol",
            "Batch",
        )
        self.tree["columns"] = columns  # Set the columns for the treeview
        self.tree["show"] = "headings"  # Put headings on the top

        # Configure each column
        for col in columns:
            self.tree.heading(col, text=col)

        # Set the column widths
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Create space to add new samples
        input_frame = ttk.Frame(self.window)
        input_frame.pack(padx=10, pady=5, fill="x")

        # Entry for aliquot ID
        self.aliquot_id_entry = ttk.Entry(input_frame)
        self.aliquot_id_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Manual button to add a sample to the list
        add_button = ttk.Button(input_frame, text="Ajouter", command=self.add_row)
        add_button.pack(side="left", padx=5)

        # Mapping to the Return key to add a sample to the list
        self.window.bind("<Return>", self.add_row)

        # Buttons zone
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)

        submit_button = ttk.Button(button_frame, text="Generate sample list", width=20, command=self.submit_table)
        submit_button.pack(side="left", padx=10)

        button_back = ttk.Button(button_frame, text="Back to Home", width=20, command=self.on_exit)
        button_back.pack(side="left", padx=10)

    def add_row(self, _: Optional[tk.Event] = None) -> None:
        parent_sample_result = get_aliquot(self.aliquot_id_entry.get().strip())

        if not parent_sample_result.is_ok:
            messagebox.showerror(
                "Error retrieving aliquot",
                parent_sample_result.error,
            )
            return
        parent_sample = cast(SampleContainer, parent_sample_result.value)

        try:
            sample = SampleData(
                parent_sample_container=parent_sample,
                injection_volume=self.mass_spectrometry.injection_volume,
                injection_methods=self.paths.methods,
                instrument=self.instrument,
                batch=self.batch,
            )

        except ValueError as e:
            messagebox.showerror(
                "Invalid sample data",
                str(e),
            )
            return

        insertion_result = insert_ms_sample(
            timestamp=self.timestamp, operator=self.mass_spectrometry.operator_initials, sample=sample
        )

        if not insertion_result.is_ok:
            messagebox.showerror(
                "Error inserting sample",
                insertion_result.error,
            )
            return

        # Insert the sample into the treeview
        self.insert_into_treeview()

        # Clear the entry field after adding the sample
        self.aliquot_id_entry.delete(0, "end")

    def insert_into_treeview(self) -> None:
        self.maybe_ask_prefix()
        position = self.generate_rack_position()
        aliquot_id = self.aliquot_id_entry.get().strip()

        for method in self.methods:
            filename = (
                self.timestamp + "_" + self.mass_spectrometry.operator_initials + "_" + method.name + "_" + aliquot_id
            )
            item_id = self.tree.insert(
                "",
                "end",
                values=(
                    aliquot_id,
                    self.mass_spectrometry.operator_initials,
                    self.instrument.name,
                    filename,
                    self.paths.data.replace("/", "\\"),
                    method.path.replace("/", "\\"),
                    position,
                    self.mass_spectrometry.injection_volume,
                    self.batch.name,
                ),
            )
            self.tree.see(item_id)

    def maybe_ask_prefix(self) -> None:
        if (self.current_position > self.rack.column) or (self.current_position == 1 and self.current_row == 1):
            ask_prefix_window = tk.Toplevel(self.window)
            ask_prefix_window.title("Add Prefix")

            self.ask_box = AskBoxPrefixWindow(ask_prefix_window)
            self.ask_box.pack(padx=10, pady=10, fill="both", expand=True)

            ask_prefix_window.transient(self.window)
            ask_prefix_window.wait_window(self.ask_box)

            self.prefix = self.ask_box.result

    def generate_rack_position(self) -> str:
        alphabet_letter = chr(ord("A") + self.current_row - 1)
        position = f"{self.prefix}{alphabet_letter}{self.current_position}"

        self.current_position += 1
        if self.current_position > self.rack.column:
            self.current_position = 1
            self.current_row += 1
        if self.current_row > self.rack.row:
            self.current_position = 1
            self.current_row = 1

        return position

    def submit_table(self) -> None:
        if not self.treeview.get_children():
            messagebox.showerror("Error", "No data to export!")
            return

        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.build_samples_from_treeview()
        self.add_pre_blanks()
        self.add_post_blanks()
        self.add_standby_sample()

        self.export_csv()

    def build_samples_from_treeview(self) -> None:
        """Builds the list of samples from the treeview data."""
        self.samples.clear()
        self.blk_sample.clear()

        for item in self.treeview.get_children():
            values = self.treeview.item(item, "values")
            aliquot_id = values[0].strip().lower()
            # Create a SampleData from Treeview column
            sample = SampleListData(
                sample_name=values[3],
                path=values[4],
                method_file=values[5],
                rack_position=values[6],
                injection_volume=float(values[7]),
            )

            if "blk" in aliquot_id:
                self.blk_sample.append(sample)
            else:
                self.samples.append(sample)

    def add_pre_blanks(self) -> None:
        for i in range(self.blank.blank_pre):
            for method in self.methods:
                # Construction of the blank name
                blank_name = f"{self.blank.blank_name}_pre_{i+1}_{method.name}"

                # Create a SampleData with blank infos
                pre_blank_sample = SampleListData(
                    sample_name=blank_name,
                    path=self.paths.data.replace("/", "\\"),
                    method_file=method.path.replace("/", "\\"),
                    rack_position=self.blank.blank_position,
                    injection_volume=self.mass_spectrometry.injection_volume,
                )

                # Insert at the beginning of the list (and keep the order)
                self.pre_blank.append(pre_blank_sample)

    def add_post_blanks(self) -> None:
        for i in range(self.blank.blank_post):
            for method in self.methods:
                blank_name = f"{self.blank.blank_name}_post_{i+1}_{method.name}"

                post_blank_sample = SampleListData(
                    sample_name=blank_name,
                    path=self.paths.data.replace("/", "\\"),
                    method_file=method.path.replace("/", "\\"),
                    rack_position=self.blank.blank_position,
                    injection_volume=self.mass_spectrometry.injection_volume,
                )
                self.post_blank.append(post_blank_sample)

    def add_standby_sample(self) -> None:
        parts = self.paths.standby.split("/")
        file = parts[-1]
        sample_name = f"{self.timestamp}_{self.mass_spectrometry.operator_initials}_{file}"
        standby_sample = SampleListData(
            sample_name=sample_name,
            path=self.paths.data.replace("/", "\\"),
            method_file=self.paths.standby.replace("/", "\\"),
            rack_position=self.blank.blank_position,
            injection_volume=self.mass_spectrometry.injection_volume,
        )
        self.standby.append(standby_sample)

    def export_csv(self) -> None:
        """Exports the sample list to a CSV file in the correct order."""
        try:
            # order the samples and blanks for the csv list
            ordered_samples = self.pre_blank + self.blk_sample + self.samples + self.post_blank + self.standby

            if not ordered_samples:
                messagebox.showwarning("No samples to export.")
                return

            with open(f"{self.paths.output}/{self.timestamp}_sample_list.csv", mode="w", newline="") as file:
                writer = csv.writer(file)

                for row in ordered_samples:
                    writer.writerow(
                        [row.sample_name, row.path, row.method_file, row.rack_position, row.injection_volume]
                    )

            messagebox.showinfo("Success", "Sample list correctly generated!")

            self.on_exit()

        except Exception as e:
            messagebox.showerror("Error", f"Sample list couldn't be generated: {e}")

    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        self.window.destroy()
        if self.root.winfo_exists():
            self.root.deiconify()
