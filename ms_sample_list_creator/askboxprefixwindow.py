import tkinter as tk
from tkinter import ttk
from typing import Optional


class AskBoxPrefixWindow(tk.Frame):
    def __init__(self, root: tk.Toplevel):
        """
        Initializes an instance of the class.

        Args:
            root(tk.Toplevel): The parent widget or window where this frame will be placed.

        Returns:
            None
        """
        tk.Frame.__init__(self, root)

        self.prefix = tk.StringVar()
        self.result: Optional[str] = None

        # Adjust the window size
        root.geometry("300x150")

        # Label + textbox to enter prefix
        label_prefix = tk.Label(self, text="Box's prefix:")
        label_prefix.pack()

        entry_prefix = tk.Entry(self, textvariable=self.prefix)
        self.prefix.set("G:")
        entry_prefix.pack()

        # set the cursor to the prefix entry
        entry_prefix.focus_set()

        # Submit button
        button_submit = ttk.Button(self, text="Submit", command=self.store_prefix)
        button_submit.pack()

    def store_prefix(self) -> None:
        """
        Puts the asked prefix to the environment.

        Args:
            None

        Returns:
            None
        """

        self.result = self.prefix.get()

        # Close the AskBoxPrefixWindow
        self.master.destroy()
