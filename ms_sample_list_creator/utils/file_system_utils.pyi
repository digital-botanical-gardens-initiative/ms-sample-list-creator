import tkinter as tk
from tkinter import ttk

from ms_sample_list_creator.implementations.list_var import ListVar

def select_element(
    button: ttk.Button,
    is_file: bool,
    variable: tk.StringVar | ListVar,
    is_method: bool = ...,
    file_type: list[tuple[str, str]] | None = ...,
) -> None: ...
