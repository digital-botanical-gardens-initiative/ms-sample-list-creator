import tkinter as tk
from tkinter import messagebox

from ttkbootstrap import ttk


class AskCsvSorting(tk.Frame):
    def __init__(self, root: tk.Toplevel):
        """
        Initializes an instance of the class.

        Args:
            root(tk.Toplevel): The parent widget or window where this frame will be placed.

        Returns:
            None
        """
        tk.Frame.__init__(self, root)

        self.choice = tk.BooleanVar(value=True)
        self.result: bool = True

        # Adjust the window size
        root.geometry("300x170")

        # Label + textbox to enter prefix
        label_choice = tk.Label(self, text="How do you want to sort the CSV file?")
        label_choice.pack(padx=10, pady=10)

        separated_method_button = ttk.Radiobutton(self, text="Separate methods", variable=self.choice, value=True)
        separated_method_button.pack(anchor=tk.W)

        alterned_method_button = ttk.Radiobutton(self, text="Alternate methods", variable=self.choice, value=False)
        alterned_method_button.pack(anchor=tk.W, pady=(0, 20))

        # Submit button
        button_submit = ttk.Button(self, text="Submit", bootstyle="success", command=self.store_sorting_choice)
        button_submit.pack()

    def store_sorting_choice(self) -> None:
        """
        Puts the asked prefix to the environment.

        Args:
            None

        Returns:
            None
        """

        if self.choice.get() is None:
            messagebox.showerror("Error", "Please select a sorting method.")

        self.result = self.choice.get()

        # Close the window
        self.master.destroy()
