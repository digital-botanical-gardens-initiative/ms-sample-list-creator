import os
import tkinter as tk
from tkinter import filedialog, ttk
from typing import List, Optional, Tuple, Union

from ms_sample_list_creator.implementations.list_var import ListVar


def select_element(
    button: ttk.Button,
    is_file: bool,
    variable: Union[ListVar, tk.StringVar],
    file_type: Optional[List[Tuple[str, str]]] = None,
) -> None:
    path = filedialog.askopenfilename(filetypes=file_type) if is_file else filedialog.askdirectory()

    if path:
        path_base = os.path.basename(path)
        button.config(text=path_base)

        if isinstance(variable, tk.StringVar):
            variable.set(path)
        elif isinstance(variable, ListVar):
            variable.add(path)
