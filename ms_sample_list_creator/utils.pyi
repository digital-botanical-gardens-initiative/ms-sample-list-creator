# import tkinter as tk
# from tkinter import ttk
# from tkinter.ttk import Treeview
# from typing import Any, Callable, Optional

# def create_label_entry_pair(
#     parent: ttk.Widget,
#     left_label_text: str,
#     right_label_text: str,
#     left_var: tk.Variable,
#     right_var: tk.Variable,
#     left_default: Optional[object] = ...,
#     right_default: Optional[object] = ...,
#     show_left: str = "",
#     show_right: str = "",
# ) -> tuple[ttk.Entry, ttk.Entry]: ...
# def create_label_widget_pair(
#     parent: ttk.Widget,
#     row: int,
#     left_label_text: str,
#     right_label_text: str,
#     left_widget: ttk.Widget,
#     right_widget: ttk.Widget,
# ) -> tuple[ttk.Widget, ttk.Widget]: ...
# def get_primary_key(endpoint: str, identifier: str, field_name: str) -> int: ...
# def directus_login(username: str, password: str) -> str: ...
# def create_label_button_row(
#     parent: ttk.Widget, label_text: str, button_text: str, command: Callable[[], None], color: str = ...
# ) -> ttk.Button: ...
# def get_directus_token(email: str, password: str) -> str: ...
# def post_sample_to_directus(token: str, sample_data: dict[str, Any]) -> dict[str, Any]: ...
# def export_treeview_to_csv(treeview: Treeview, file_path: str) -> None: ...
# def get_existing_batches() -> list[str]: ...

# # def post_sample_with_retry(
# #     session: DirectusSessionData, sample: dict[str, object], login_func: Callable[[], DirectusSessionData]
# # ) -> dict[str, object]: ...
