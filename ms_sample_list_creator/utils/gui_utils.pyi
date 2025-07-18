import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Callable, TypeVar

if TYPE_CHECKING:
    from ms_sample_list_creator.home import HomeWindow

Self = TypeVar("Self", bound="HomeWindow")

def create_label_input_pair(
    parent: ttk.Widget,
    left_label_text: str,
    right_label_text: str,
    left_var: tk.Variable,
    right_var: tk.Variable,
    left_type: str = ...,
    right_type: str = ...,
    left_values: list[str] | None = ...,
    right_values: list[str] | None = ...,
    entry_width: int = ...,
    combobox_width: int = ...,
    left_default: str | None = ...,
    right_default: str | None = ...,
    show_left: str = ...,
    show_right: str = ...,
) -> tuple[ttk.Entry | ttk.Combobox, ttk.Entry | ttk.Combobox]: ...
def build_method_section(self: Self) -> None: ...
def build_standby_selector(self: Self) -> None: ...
def build_output_selector(self: Self) -> None: ...
def build_data_selector(self: Self) -> None: ...
def build_submit_button(self: ttk.Frame, command: Callable[[], None]) -> None: ...
def create_label_button_row(
    parent: ttk.Widget,
    label_text: str,
    button_text: str,
    command: Callable[[], None],
    label_width: int = ...,
    button_width: int = ...,
    color: str | None = ...,
) -> ttk.Button: ...
