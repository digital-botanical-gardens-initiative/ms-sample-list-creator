from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
from typing import Tuple, List, Callable, Optional, Any, Dict
from .structure import TkVariables, DirectusSessionData
import os
import requests
import csv

def choose_path_and_update_button(
    dialog_type: str,
    env_var: str,
    button: ttk.Button,
    filetype: Optional[List[Tuple[str, str]]] = None
) -> None:
    """
    Chooses a file/folder, sets an environment variable, and updates the button text.

    Args:
        dialog_type: "file" or "folder"
        env_var: environment variable to set
        button: Tkinter button to update
        filetypes: optional filetypes for file dialog

    Returns:
        None
    """
    if dialog_type == "folder":
        path = filedialog.askdirectory()
    elif dialog_type == "file":
        path = filedialog.askopenfilename(filetypes=filetype)
    else:
        raise ValueError("Invalid dialog type")

    if path:
        path_base = os.path.basename(path.split(".")[0])
        os.environ[env_var] = path
        button.config(text=path_base)

def create_label_entry_pair(
    parent: ttk.Widget,
    left_label_text: str,
    right_label_text: str,
    left_var: tk.Variable,
    right_var: tk.Variable,
    left_default=None,
    right_default=None,
    show_left: str = "",
    show_right: str = ""
) -> Tuple[ttk.Entry, ttk.Entry]:
    """Creates a pair of labeled entry fields with a title label above.

    Args:
        parent: The parent widget to contain the frames.
        left_label_text: Label for the left entry.
        right_label_text: Label for the right entry.
        left_var: Tkinter variable for the left entry.
        right_var: Tkinter variable for the right entry.
        left_default: Optional default value for the left entry.
        right_default: Optional default value for the right entry.
        show_left: Character to display instead of actual characters for left entry (e.g., "*" for password).
        show_right: Same as above for right entry.

    Returns:
        A tuple containing the left and right Entry widgets.
    """
    frame_label = ttk.Frame(parent)
    frame_label.pack(fill="x", pady=(7, 0))

    label_left = ttk.Label(frame_label, text=left_label_text)
    label_left.pack(side="left", padx=15, anchor="center")

    label_right = ttk.Label(frame_label, text=right_label_text)
    label_right.pack(side="right", padx=(0, 20), anchor="center")

    frame_entry = ttk.Frame(parent)
    frame_entry.pack(fill="x", pady=2)

    entry_left = ttk.Entry(frame_entry, textvariable=left_var, show=show_left)
    entry_left.pack(side="left", anchor="center")

    entry_right = ttk.Entry(frame_entry, textvariable=right_var, show=show_right)
    entry_right.pack(side="right", anchor="center")

    if left_default is not None:
        left_var.set(left_default)
    if right_default is not None:
        right_var.set(right_default)

    return entry_left, entry_right


def get_primary_key(endpoint: str, identifier: str, field_name: str) -> int:
    """
    Retrieves the primary key of an entry from a Directus collection.

    Args:
        endpoint (str): The API endpoint to query.
        identifier (str): The value of the field to search for.
        field_name (str): The field name to match the identifier against.

    Returns:
        int: The primary key if found, -1 otherwise.
    """
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json().get("data", [])
        for item in data:
            if str(item.get(field_name)) == identifier:
                return item["id"]
    except requests.RequestException as e:
        print(f"Error fetching primary key from {endpoint}: {e}")
    return -1

def directus_login(username: str, password: str) -> str:
    """
    Logs into Directus and retrieves an access token.

    Args:
        username (str): Directus username.
        password (str): Directus password.

    Returns:
        str: Access token if login succeeds, empty string otherwise.
    """
    login_url = "https://emi-collection.unifr.ch/directus/auth/login"
    try:
        response = requests.post(login_url, json={"email": username, "password": password})
        response.raise_for_status()
        return response.json()["data"]["access_token"]
    except requests.RequestException as e:
        print(f"Login failed: {e}")
        return ""

def create_label_button_row(
    parent: ttk.Widget,
    label_text: str,
    button_text: str,
    command: Callable,
    label_width: int = 22,
    button_width: int = 20,
    color: Optional[str] = None
) -> ttk.Button:
    frame = ttk.Frame(parent)
    frame.pack(fill="x", pady=4)

    label = ttk.Label(frame, text=label_text, width=label_width, anchor="w", background="white")
    if color:
        label.configure(foreground=color)
    label.pack(side="left", padx=(10, 5))

    button = ttk.Button(frame, text=button_text, command=command, width=button_width)
    if color:
        button.configure(foreground=color)
    button.pack(side="left", padx=5)

    return button

def load_env_config() -> Tuple[TkVariables, DirectusSessionData]:
    """Charge les variables d'environnement dans des dataclasses."""
    tk_vars = TkVariables()
    directus_data = DirectusSessionData()

    tk_vars.operator_settings.operator.set(os.getenv("OPERATOR", ""))
    tk_vars.operator_settings.ms_id.set(os.getenv("MS_ID", ""))
    tk_vars.col_rack_number.set(int(os.getenv("COL_RACK_NUMBER", "0")))
    tk_vars.row_rack_number.set(int(os.getenv("ROW_RACK_NUMBER", "0")))
    tk_vars.pre_blk.set(int(os.getenv("PRE_BLK", "0")))
    tk_vars.post_blk.set(int(os.getenv("POST_BLK", "0")))
    tk_vars.blk_name.set(os.getenv("BLK_NAME", ""))
    tk_vars.blk_pos.set(os.getenv("BLK_POS", ""))
    tk_vars.inj_volume.set(int(os.getenv("INJ_VOLUME", "0")))
    tk_vars.file = os.getenv("FILE", "")
    tk_vars.method_files = os.getenv("METHOD_FILE", "").split(",") if os.getenv("METHOD_FILE") else []

    directus_data.access_token = os.getenv("ACCESS_TOKEN", "")
    directus_data.instrument_key = int(os.getenv("INSTRUMENT_KEY", "-1"))
    directus_data.batch_key = int(os.getenv("BATCH_KEY", "-1"))
    directus_data.method_keys = [
        int(k) for k in os.getenv("INJECTION_METHOD_KEYS", "").split(",") if k
    ]

    return tk_vars, directus_data

def get_directus_token(email: str, password: str) -> str:
    """Récupère un token d'authentification Directus."""
    response = requests.post(
        "https://emi-collection.unifr.ch/directus/auth/login",
        json={"email": email, "password": password}
    )
    response.raise_for_status()
    return response.json()["data"]["access_token"]


def post_sample_to_directus(token: str, sample_data: Dict[str, Any]) -> Dict[str, Any]:
    """Envoie un échantillon à Directus."""
    url = "https://emi-collection.unifr.ch/directus/items/MS_Data"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=sample_data)
    response.raise_for_status()
    return response.json()


def export_treeview_to_csv(treeview: Treeview, file_path: str) -> None:
    """Exporte le contenu d'un Treeview vers un fichier CSV."""
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        columns = treeview["columns"]
        writer.writerow(columns)
        for row in treeview.get_children():
            writer.writerow(treeview.item(row)["values"])