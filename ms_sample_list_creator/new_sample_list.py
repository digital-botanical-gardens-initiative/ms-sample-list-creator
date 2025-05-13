import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any
from ms_sample_list_creator import utils
from .structure import TkVariables, DirectusSessionData
import webbrowser

class newBatch(ttk.Frame):
    """
    Class to display a message when a new version of the application is available.
    """
    def __init__(self, parent: tk.Toplevel):
        """
        Initializes an instance of the class.

        Args:
            parent(tk.Tk): The parent widget or window where this frame will be placed.
            
        Returns:
            None
        """
        super().__init__(parent)
        self.parent = parent

        self.tk_vars, self.directus_data = utils.load_env_config()
        self.token = self.directus_data.access_token
        
        self.create_widgets()

        # Create GUI elements to ask user to download the latest version
        label = ttk.Label(self, text="A new version is available, please download it.")
        label.pack()

        button_new_version = ttk.Button(
            self, text="Download latest version", width=40, command=self.download_last_version
        )
        button_new_version.pack()

    def create_widgets(self) -> None:
        """Crée les widgets de la fenêtre."""
        self.treeview = ttk.Treeview(self, columns=("Sample", "Rack Position", "Volume"), show="headings")
        for col in ("Sample", "Rack Position", "Volume"):
            self.treeview.heading(col, text=col)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        self.add_sample_button = tk.Button(self, text="Add Sample", command=self.add_sample)
        self.add_sample_button.pack()

        self.export_button = tk.Button(self, text="Exporter CSV", command=self.export_csv)
        self.export_button.pack()

    def add_sample(self) -> None:
        """Ajoute un échantillon fictif à la treeview."""
        self.treeview.insert("", "end", values=("Sample-1", "A1", "10"))

    def export_csv(self) -> None:
        """Exporte les données en CSV."""
        try:
            utils.export_treeview_to_csv(self.treeview, "samples.csv")
            messagebox.showinfo("Succès", "Exportation terminée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation : {e}")

    def push_sample(self, sample_data: dict) -> None:
        """Envoie un échantillon à Directus."""
        try:
            result = utils.post_sample_to_directus(self.token, sample_data)
            messagebox.showinfo("Succès", f"Échantillon envoyé avec succès : {result}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l’envoi : {e}")

    # Function that redirects user to the last software version
    def download_last_version(self) -> None:
        url = "https://github.com/digital-botanical-gardens-initiative/ms-sample-list-creator/releases/latest"
        webbrowser.open(url)

