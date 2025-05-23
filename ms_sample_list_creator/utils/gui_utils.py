import tkinter as tk
from tkinter import ttk
from typing import Tuple, List, Dict, Callable, Optional, Union, Any
from tkinter import filedialog
import os

import requests

from ..implementations.list_var import ListVar
from ..structure import Batch
from ..home import HomeWindow


def get_batches() -> List[Batch]:
    """Get the list of batches from Directus.

    Returns:
        A list of batch names.
    """
    url = "https://emi-collection.unifr.ch/directus/items/Batches?filter[batch_type][_eq]=6&fields=batch_id,id"
    headers = {"Content-Type": "application/json"}
    params = {"sort[]": "batch_id"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()["data"]
        batches = []
        for item in data:
            batch = Batch(
                name=item["batch_id"],
                identifier=item["id"]
            )
            batches.append(batch)
        return batches
    except requests.RequestException as e:
        print(f"Error fetching batches: {e}")
        return []


 # def refresh_batch_list(self) -> None:
    #     print(7)
    #     """
    #     Refresh the list of batches from Directus and update the combobox.
    #     Includes a "new batch" option with the correct next batch number.
    #     """

    #     try:
    #         batches = utils.get_existing_batches()
    #         print("Batches récupérés :", batches)
    #     except requests.HTTPError as e:
    #         messagebox.showerror("Erreur", f"Impossible de récupérer les batchs : {e}")
    #         return
    #     except Exception as e:
    #         messagebox.showerror("Erreur", f"Erreur inattendue : {e}")
    #         return

    #     existing_numbers = []
    #     for b in batches:
    #         try:
    #             if b["name"].startswith("batch_"):
    #                 num = int(b["name"].split("_")[1])
    #                 existing_numbers.append(num)
    #         except Exception as e:
    #             print(f"Error during batch extraction : {e}")
    #             continue

    #     next_batch_number = max(existing_numbers, default=0) + 1

    #     new_batch_label = f"batch_{next_batch_number:06d} (new batch)"

    #     # Mapping affichage -> id Directus
    #     self.batch_mapping = {new_batch_label: "__NEW__"}
    #     for b in batches:
    #         self.batch_mapping[b["name"]] = b["id"]

    #     values = ["Select a batch", new_batch_label] + [b["name"] for b in batches]
    #     self.batch_combobox["values"] = values
    #     self.batch_key.set("Select a batch")

    #     # Print pour debug
    #     print("Batch mapping :")
    #     for label, directus_id in self.batch_mapping.items():
    #         print(f"  {label} -> {directus_id}")

    #     self.batch_combobox.bind("<<ComboboxSelected>>", self.on_batch_selected)

def create_label_input_pair(
    parent: ttk.Widget,
    left_label_text: str,
    right_label_text: str,
    left_var: tk.Variable,
    right_var: tk.Variable,
    left_type: str = "entry",
    right_type: str = "entry",
    entry_width: int = 20,
    combobox_width: int = 20,
    show_left: str = "",
    show_right: str = "",
    left_default: Optional[str] = None,
    right_default: Optional[str] = None,
    left_values: Optional[List[str]] = None,
    right_values: Optional[List[str]] = None,
) -> Tuple[Union[ttk.Entry, ttk.Combobox], Union[ttk.Entry, ttk.Combobox]]:
    """
    Create a horizontally aligned pair of input fields (Entry or Combobox) with labels.

    Args:
        parent: The parent widget.
        left_label_text: Label for the left widget.
        right_label_text: Label for the right widget.
        left_var: Variable for the left widget.
        right_var: Variable for the right widget.
        left_type: "entry" or "combobox" for left widget.
        right_type: "entry" or "combobox" for right widget.
        left_values: Values for left combobox, if used.
        right_values: Values for right combobox, if used.
        entry_width: Width for entry fields.
        combobox_width: Width for combobox fields.
        left_default: Default value for left input.
        right_default: Default value for right input.
        show_left: Character to mask left input (for passwords).
        show_right: Character to mask right input.

    Returns:
        Tuple of the left and right input widgets.
    """

    frame_duo = ttk.Frame(parent)
    frame_duo.pack(fill="x", padx=10, pady=(7, 0))

    # --- LEFT ---
    frame_left = ttk.Frame(frame_duo)
    frame_left.pack(side="left", expand=True, fill="x", padx=(0, 25))

    ttk.Label(frame_left, text=left_label_text).pack(anchor="w")

    if left_type == "combobox":
        left_widget: Union[ttk.Entry, ttk.Combobox] = ttk.Combobox(
            frame_left,
            textvariable=left_var,
            values=left_values or [],
            state="readonly",
            width=combobox_width
        )
    else:
        left_widget = ttk.Entry(
            frame_left,
            textvariable=left_var,
            width=entry_width,
            show=show_left
        )
    left_widget.pack(anchor="w", pady=(2, 0))
    if left_default is not None:
        left_var.set(left_default)

    # --- RIGHT ---
    frame_right = ttk.Frame(frame_duo)
    frame_right.pack(side="right", expand=True, fill="x", padx=(25, 0))

    ttk.Label(frame_right, text=right_label_text).pack(anchor="w")

    if right_type == "combobox":
        right_widget: Union[ttk.Entry, ttk.Combobox] = ttk.Combobox(
            frame_right,
            textvariable=right_var,
            values=right_values or [],
            state="readonly",
            width=combobox_width
        )
    else:
        right_widget = ttk.Entry(
            frame_right,
            textvariable=right_var,
            width=entry_width,
            show=show_right
        )
    right_widget.pack(anchor="w", pady=(2, 0))
    if right_default is not None:
        right_var.set(right_default)

    return left_widget, right_widget

def select_element(button: ttk.Button, is_file: bool, variable: Union[tk.StringVar, ListVar], file_type: Optional[List[Tuple[str, str]]] = None) -> None:
        # Check wether we want to select a file or a directory
        if is_file:
            path = filedialog.askopenfilename(filetypes=file_type)
        else:
            path = filedialog.askdirectory()
        
        # Check that we have a valid path
        if path:
            # Extract the base name of the path and set it as the button text
            path_base = os.path.basename(path)
            button.config(text=path_base)
            variable.set(path)

def build_method_section(self: HomeWindow) -> None:
    # If section already exists, do not create it again
    if hasattr(self, 'method_section_frame'):
        return  
    
    # Label for the method section
    method_section_frame = ttk.Frame(self)
    method_section_frame.pack(fill="x", pady=(7, 0))

    label_method_path = ttk.Label(method_section_frame, text="Injection method file:")
    label_method_path.pack(anchor="w", padx=10, pady=(0, 5))

    # Frame containing method buttons
    method_select_frame = ttk.Frame(method_section_frame)
    method_select_frame.pack(fill="x")

    def create_selector(after_frame: Optional[ttk.Frame] = None) -> ttk.Frame:
        frame = ttk.Frame(method_select_frame)
        # Pack under the frame if it exists
        if after_frame is not None:
            frame.pack(fill="x", pady=5, padx=10, after=after_frame)
        else:
            frame.pack(fill="x", pady=5, padx=10)

        method_label = ttk.Label(frame, text="Method:")
        method_label.pack(side="left")

        method_button = ttk.Button(frame, text="Add method")
        method_button.pack(side="left", padx=5)

        def on_select(self: HomeWindow) -> None: 
            select_element(button=method_button,
            is_file=True,
            variable= self.method_files,
            file_type=[("Method files", "*.meth")]
            )

            # Add new button add_method
            create_selector(after_frame=frame)

        method_button.config(command=lambda: on_select(self))

        return frame

    # Start with one button
    create_selector()

def build_standby_selector(self: HomeWindow) -> None:
    standby_path_button = create_label_button_row(
    parent=self,
    label_text="Standby method file:",
    button_text="Select Standby File",
    command=lambda: select_element(
        button=standby_path_button,
        is_file=True,
        variable=self.standby_file,  
        file_type=[("methods", "*.meth")]
    )
)

def build_output_selector(self: HomeWindow) -> None:
    output_path_button = create_label_button_row(
    parent=self,
    label_text="Sample list directory:",
    button_text="Select Output Folder",
    command=lambda: select_element(
        button=output_path_button,
        is_file=False,
        variable=self.output_path
    )
)
    
def build_data_selector(self: HomeWindow) -> None:
    data_path_button = create_label_button_row(
    parent=self,
    label_text="MS data directory:",
    button_text="Select Data Folder",
    command=lambda: select_element(
        button=data_path_button,
        is_file=False,
        variable=self.data_path  
    )
)

def build_submit_button(self: HomeWindow, command: Callable[[], None]) -> None:
    frame_submit = ttk.Frame(self)
    frame_submit.pack(fill="x", pady=(50, 0), padx=10)

    button_frame = ttk.Frame(frame_submit)
    button_frame.pack(fill="x")

    button_new_batch = ttk.Button(
        button_frame,
        text="Validate",
        style="Success.TButton",
        width=17,
        command=command,
    )
    button_new_batch.pack(side="left", padx=(0, 5))

def create_label_button_row(
    parent: ttk.Widget,
    label_text: str,
    button_text: str,
    command: Callable,
    label_width: int = 22,
    button_width: int = 20,
    color: Optional[str] = None,
) -> ttk.Button:
    frame = ttk.Frame(parent)
    frame.pack(fill="x", pady=4)

    label = ttk.Label(frame, text=label_text, width=label_width, anchor="w", background="white")
    if color:
        label.configure(foreground=color)
    label.pack(side="left", padx=(10, 5))

    button = ttk.Button(frame, text=button_text, command=command, width=button_width)
    if color is not None:
        button.configure(**{"foreground": color})
    button.pack(side="left", padx=5)

    return button