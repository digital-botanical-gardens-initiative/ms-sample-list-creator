import tkinter as tk
import webbrowser
from tkinter import ttk
from typing import Any


class NewVersionAvailable(ttk.Frame):
    """
    Class to display a message when a new version of the application is available.
    """

    def __init__(self, parent: tk.Tk, *args: Any, **kwargs: Any):
        """
        Initializes an instance of the class.

        Args:
            parent(tk.Tk): The parent widget or window where this frame will be placed.
            csv_path(str): CSV path and name.

        Returns:
            None
        """

        ttk.Frame.__init__(self, parent, *args, **kwargs)
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create GUI elements to ask user to download the latest version
        label = tk.Label(self, text="A new version is available, please download it.")
        label.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")

        button_new_version = ttk.Button(
            self, text="Download latest version", width=40, command=self.download_last_version
        )
        button_new_version.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="ew")

    # Function that redirects user to the last software version
    def download_last_version(self) -> None:
        url = "https://github.com/digital-botanical-gardens-initiative/ms-sample-list-creator/releases/latest"
        webbrowser.open(url)
