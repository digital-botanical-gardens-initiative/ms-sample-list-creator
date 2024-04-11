import tkinter as tk
import os

class AskBoxPrefixWindow(tk.Frame):
    def __init__(self, root: tk.Toplevel):
        """
        Initializes an instance of the class.

        Args:
            root(tk.Toplevel): The parent widget or window where this frame will be placed.
            csv_path(str): CSV path and name.

        Returns:
            None
        """
        tk.Frame.__init__(self, root)

        self.prefix = tk.StringVar()

        # Adjust the window size
        root.geometry("300x150")

        # Label + textbox to enter prefix
        label_prefix = tk.Label(self, text="Box's prefix:")
        label_prefix.pack()

        entry_prefix = tk.Entry(self, textvariable=self.prefix)
        entry_prefix.pack()

        # Submit button
        button_submit = tk.Button(self, text="Submit", command=self.store_prefix)
        button_submit.pack()

    def store_prefix(self) -> None:
        """
        Puts the asked prefix to the environment.

        Args:
            None

        Returns:
            None
        """
        os.environ["PREFIX"] = self.prefix.get()

        # Close the AskBoxPrefixWindow
        self.master.destroy()