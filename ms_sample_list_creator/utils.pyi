from tkinter import ttk
import tkinter as tk
from tkinter.ttk import Treeview
from typing import Tuple, Optional, Callable, List, Dict
from typing import Any
from .structure import TkVariables, DirectusSessionData


def choose_path_and_update_button(
    dialog_type: str,
    env_var: str,
    button: ttk.Button,
    filetype: Optional[List[Tuple[str, str]]]
) -> None: ...

def create_label_entry_pair(
    parent: ttk.Widget,
    left_label_text: str,
    right_label_text: str,
    left_var: tk.Variable,
    right_var: tk.Variable,
    left_default: Optional[object] = ...,
    right_default: Optional[object] = ...,
    show_left: str = "",
    show_right: str = ""
) -> Tuple[ttk.Entry, ttk.Entry]: ...

def get_primary_key(
    endpoint: str,
    identifier: str,
    field_name: str
) -> int: ...

def directus_login(
    username: str,
    password: str
) -> str: ...

def create_label_button_row(
    parent: ttk.Widget,
    label_text: str,
    button_text: str,
    command: Callable[[], None],
    color: str = ...
) -> ttk.Button: ...

def load_env_config() -> Tuple[TkVariables, DirectusSessionData]: ...

def get_directus_token(
    email: str, 
    password: str
) -> str: ...

def post_sample_to_directus(
    token: str, sample_data: Dict[str, Any]
) -> Dict[str, Any]: ...

def export_treeview_to_csv(
    treeview: Treeview, 
    file_path: str
) -> None: ...
