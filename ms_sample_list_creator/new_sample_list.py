# import csv
# import tkinter as tk
# from datetime import datetime
# from tkinter import messagebox, ttk
# from typing import List, Optional, Tuple, Union

# import requests

# from ms_sample_list_creator import utils

# from .askboxprefixwindow import AskBoxPrefixWindow
# from .structure import DirectusSessionData, SampleData, TkVariables


# class newBatch(ttk.Frame):
#     """
#     Class to display a message when a new version of the application is available.
#     """

#     def __init__(self, parent: tk.Toplevel, session_data: DirectusSessionData):
#         """
#         Initializes an instance of the class.

#         Args:
#             parent(tk.Tk): The parent widget or window where this frame will be placed.

#         Returns:
#             None
#         """
#         super().__init__(parent)
#         self.root = parent
#         self.new_batch_window = parent

#         self.session_data = session_data
#         self.token = self.session_data.access_token

#         self.new_batch_window.protocol("WM_DELETE_WINDOW", self.on_exit)

#         self.treeview = ttk.Treeview(self)
#         self.treeview.pack(fill="both", expand=True, padx=10, pady=10)
#         self.tree = self.treeview

#         self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#         # Initialisation des variables de configuration
#         self.vars = TkVariables()
#         self.sample_data = SampleData()
#         self.samples: List[SampleData] = []

#         # Ajout des compteurs internes
#         self.current_row: int = 0
#         self.current_position: int = 1

#         # Interface formulaire
#         form_frame = ttk.Frame(self)
#         form_frame.pack(padx=5, pady=5, fill="x")

#         self.sample_entry = ttk.Entry(form_frame)
#         self.sample_entry.pack(side="left", padx=5)

#         self.rack_entry = ttk.Entry(form_frame)
#         self.rack_entry.pack(side="left", padx=5)

#         self.volume_entry = ttk.Entry(form_frame)
#         self.volume_entry.pack(side="left", padx=5)

#         self.create_widgets()

#     def create_widgets(self) -> None:
#         """Crée les widgets de la fenêtre avec une disposition verticale logique."""

#         # === Zone de la liste (Treeview) ===
#         columns = (
#             "aliquot_id",
#             "operator",
#             "ms_id",
#             "File Name",
#             "Path",
#             "Instrument Method",
#             "Position",
#             "Inj Vol",
#             "Batch",
#         )
#         self.tree["columns"] = columns
#         self.tree["show"] = "headings"
#         for col in columns:
#             self.tree.heading(col, text=col)

#         self.tree.pack(padx=10, pady=10, fill="both", expand=True)

#         # === Zone de saisie des échantillons ===
#         input_frame = ttk.Frame(self.new_batch_window)
#         input_frame.pack(padx=10, pady=5, fill="x")

#         self.aliquot_id_entry = ttk.Entry(input_frame)
#         self.aliquot_id_entry.pack(side="left", expand=True, fill="x", padx=5)

#         add_button = ttk.Button(input_frame, text="Ajouter", command=self.add_row)
#         add_button.pack(side="left", padx=5)

#         # Entrée via la touche "Entrée"
#         self.new_batch_window.bind("<Return>", self.add_row)

#         # === Label pour messages d'erreur ou d'état ===
#         self.label = ttk.Label(self.new_batch_window, text="")
#         self.label.pack(pady=5)

#         # === Zone des boutons ===
#         button_frame = ttk.Frame(self.new_batch_window)
#         button_frame.pack(pady=10)

#         submit_button = ttk.Button(button_frame, text="Generate sample list", width=20, command=self.submit_table)
#         submit_button.pack(side="left", padx=10)

#         button_back = ttk.Button(button_frame, text="Back to Home", width=20, command=self.on_exit)
#         button_back.pack(side="left", padx=10)

#     def add_row(self, event: Optional[tk.Event] = None) -> None:
#         aliquot_id = self._get_aliquot_id()
#         if not aliquot_id:
#             return

#         filename, path, instrument_method, inj_volume = self._prepare_sample_data(aliquot_id)
#         aliquot_key = utils.get_primary_key(
#             "https://emi-collection.unifr.ch/directus/items/Containers", aliquot_id, "container_id"
#         )

#         if not self.sample_data.method_key:
#             self.label.config(text="Erreur : aucune méthode sélectionnée.")
#             return

#         for injection_method_key in self.sample_data.method_key:
#             status_code = self._send_data_to_directus(aliquot_key, filename, inj_volume, injection_method_key)

#             self._handle_directus_response(status_code, aliquot_id, filename, path, instrument_method, inj_volume)

#     def _get_aliquot_id(self) -> Optional[str]:
#         aliquot_id = self.aliquot_id_entry.get().strip()
#         if not aliquot_id:
#             self.label.config(text="aliquot id can't be empty!", foreground="red")
#             return None
#         return aliquot_id

#     def _prepare_sample_data(self, aliquot_id: str) -> Tuple[str, str, str, int]:
#         filename = self.timestamp + "_" + str(self.vars.operator) + "_" + aliquot_id
#         path = self.vars.data_path.replace("/", "\\")
#         instrument_methods = [method.replace("/", "\\") for method in self.vars.method_files]
#         inj_volume = self.vars.inj_volume
#         return filename, path, instrument_methods, inj_volume

#     def _send_data_to_directus(
#         self, aliquot_key: str, filename: str, inj_volume: int, injection_method_key: str
#     ) -> int:
#         url = "https://emi-collection.unifr.ch/directus/items/MS_Data"
#         session = requests.Session()
#         session.headers.update({"Authorization": f"Bearer {self.session_data.access_token}"})
#         headers = {"Content-Type": "application/json"}

#         data = {
#             "parent_sample_container": aliquot_key,
#             "filename": filename,
#             "instrument_used": self.session_data.instrument_key,
#             "injection_volume": inj_volume,
#             "injection_volume_unit": 18,
#             "injection_method": injection_method_key,
#             "batch": self.sample_data.batch_key,
#         }

#         # response = session.post(url=url, headers=headers, json=data) #TODO: before production uncomment this line
#         return 200  # response.status_code

#     def _handle_directus_response(
#         self,
#         status_code: int,
#         aliquot_id: str,
#         filename: str,
#         path: str,
#         instrument_method: str,
#         inj_volume: int,
#     ) -> None:
#         if status_code == 200:
#             self._maybe_ask_prefix()

#             position = self._generate_rack_position()

#             self.label.config(text="Correctly added!", foreground="green")
#             self._insert_into_treeview(aliquot_id, filename, path, instrument_method, position, inj_volume)

#             self.aliquot_id_entry.delete(0, "end")

#         elif status_code == 401:
#             self.directus_reconnect()
#         else:
#             self.label.config(text=f"Directus error, {aliquot_id} doesn't seem to be valid!", foreground="red")

#     def directus_reconnect(self) -> None:
#         """
#         Directus tokens have a validity of 15 minutes. If directus returns an unauthorized response,
#         it could be due to the token expiration. So this function tries a reconnexion to generate a new access token.

#         Args:
#             None

#         Returns:
#             None
#         """
#         username = self.session_data.email
#         password = self.session_data.password

#         # Define the Directus base URL
#         base_url = "https://emi-collection.unifr.ch/directus"

#         # Define the login endpoint URL
#         login_url = base_url + "/auth/login"
#         # Create a session object for making requests
#         session = requests.Session()
#         # Send a POST request to the login endpoint
#         response = session.post(login_url, json={"email": username, "password": password})

#         if response.status_code == 200:
#             data = response.json()["data"]
#             self.access_token = data["access_token"]
#             self.root.event_generate("<Return>")

#         else:
#             # Display error statement
#             self.label.config(text="Reconnexion to directus failed", foreground="red")

#     def _maybe_ask_prefix(self) -> None:
#         if (self.current_position > self.vars.col_rack_number) or (
#             self.current_position == 1 and self.current_row == 1
#         ):
#             ask_prefix_window = tk.Toplevel(self.new_batch_window)
#             ask_prefix_window.title("Add Prefix")

#             self.ask_box = AskBoxPrefixWindow(ask_prefix_window)
#             self.ask_box.pack(padx=10, pady=10, fill="both", expand=True)

#             ask_prefix_window.transient(self.new_batch_window)
#             ask_prefix_window.wait_window(self.ask_box)

#     def _generate_rack_position(self) -> str:
#         prefix = self.vars.prefix
#         alphabet_letter = chr(ord("A") + self.current_row - 1)
#         position = f"{prefix}{alphabet_letter}{self.current_position}"

#         self.current_position += 1
#         if self.current_position > self.vars.col_rack_number:
#             self.current_position = 1
#             self.current_row += 1
#         if self.current_row > self.vars.row_rack_number:
#             self.current_position = 1
#             self.current_row = 1

#         return position

#     def _insert_into_treeview(
#         self,
#         aliquot_id: str,
#         filename: str,
#         path: str,
#         instrument_method: str,
#         position: str,
#         inj_volume: int,
#     ) -> None:
#         item_id = self.tree.insert(
#             "",
#             "end",
#             values=(
#                 aliquot_id,
#                 self.vars.operator,
#                 self.vars.ms_id,
#                 filename,
#                 path,
#                 instrument_method,
#                 position,
#                 inj_volume,
#                 self.vars.batch_key,
#             ),
#         )
#         self.tree.see(item_id)

#     def export_csv(self) -> None:
#         """Exporte les données en CSV."""
#         try:
#             utils.export_treeview_to_csv(self.treeview, "samples.csv")
#             messagebox.showinfo("Succès", "Exportation terminée.")
#         except Exception as e:
#             messagebox.showerror("Erreur", f"Erreur lors de l'exportation : {e}")

#     def add_pre_blanks(self) -> None:
#         """
#         Ajoute les blancs pré-échantillons (pre_blks) en début de la liste self.samples
#         avec les infos issues de vars.
#         """
#         for i in range(self.vars.pre_blk):
#             # Construire le nom du blanc selon la nomenclature définie dans TkVariables
#             blank_name = f"{self.vars.blk_name}_pre_{i+1}"

#             # Créer une instance SampleData avec les infos spécifiques au blanc
#             blank_sample = SampleData(
#                 sample_name=blank_name,
#                 rack_position=self.vars.blk_pos,
#                 injection_volume=self.vars.inj_volume,
#             )

#             # Insert at the beginning of the list (and keep the order)
#             self.samples.insert(i, blank_sample)

#     def add_post_blanks(self) -> None:
#         """
#         Ajoute les blancs post-échantillons (post_blks) en fin de la liste self.samples
#         avec les infos issues de vars.
#         """
#         for i in range(self.vars.post_blk):
#             blank_name = f"{self.vars.blk_name}_post_{i+1}"

#             blank_sample = SampleData(
#                 sample_name=blank_name,
#                 rack_position=self.vars.blk_pos,
#                 injection_volume=self.vars.inj_volume,
#             )
#             # Ajouter à la fin
#             self.samples.append(blank_sample)

#     def add_standby_sample(self) -> None:
#         """Ajoute un échantillon standby à la fin de `self.samples`."""
#         parts = self.vars.standby_file.split("/")
#         file = parts[-1]
#         sample_name = f"{self.timestamp}_{self.vars.operator}_{file}"
#         standby_sample = SampleData(
#             sample_name=sample_name,
#             path=self.vars.data_path.replace("/", "\\"),
#             method_file=self.vars.standby_file.replace("/", "\\"),
#             rack_position=self.vars.blk_pos,
#             injection_volume=self.vars.inj_volume,
#         )
#         self.samples.append(standby_sample)

#     def get_next_rack_position(self) -> str:
#         used_positions = {sample.rack_position for sample in self.samples}

#         rows = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#         for row in rows[: self.vars.row_rack_number]:
#             for col in range(1, self.vars.col_rack_number + 1):
#                 pos = f"{row}{col}"
#                 if pos not in used_positions:
#                     return pos
#         raise ValueError("Plus de positions disponibles dans le rack.")

#     def build_samples_from_treeview(self) -> None:
#         """Construit la liste `self.samples` à partir des valeurs du Treeview."""
#         self.samples.clear()
#         for item in self.treeview.get_children():
#             values = self.treeview.item(item, "values")
#             # Crée un SampleData depuis les colonnes du Treeview
#             sample = SampleData(
#                 sample_name=values[3],
#                 path=values[4],
#                 method_file=values[5],
#                 rack_position=values[6],
#                 injection_volume=int(values[7]),
#             )
#             self.samples.append(sample)

#     def export_final_samples_list_to_csv(self) -> None:
#         """Écrit self.samples dans un fichier CSV."""
#         with open(self.vars.data_path, "w", newline="") as csv_file:
#             csv_writer = csv.writer(csv_file)
#             # En-têtes
#             csv_writer.writerow(["Bracket Type=4", "", "", "", ""])
#             csv_writer.writerow(["File Name", "Path", "Instrument Method", "Position", "Inj Vol"])

#             for sample in self.samples:
#                 csv_writer.writerow(
#                     [
#                         sample.sample_name,
#                         sample.path,
#                         sample.method_key,
#                         sample.rack_position,
#                         sample.injection_volume,
#                     ]
#                 )

#     def on_exit(self) -> None:
#         """
#         Defines behaviour when user quits this window (by x button or specified button).

#         Args:
#             None

#         Returns:
#             None
#         """
#         self.new_batch_window.destroy()
#         self.root.deiconify()

#     def blanks_first(item: Union[Tuple[str, ...], List[str]]) -> Tuple[int, str]:
#         """
#         Detects blanks and puts them first in the list.

#         Args:
#             item (str): The item to be analyzed.

#         Returns:
#             Tuple[int, str]: A tuple containing a priority value and the sample ID.
#         """

#         # Extract the sample ID from the file name
#         sample_id = item[0].split("_")[3]
#         # Check if the sample ID contains 'batch'
#         if sample_id.startswith("blk"):
#             return (0, sample_id)  # If yes, put it in first place
#         else:
#             return (1, sample_id)  # Else, put it after

#     def submit_table(self) -> None:
#         """
#         Génère les objets SampleData à partir du Treeview et écrit un CSV avec les blancs et le standby.
#         """
#         if not self.treeview.get_children():
#             self.label.config(text="No data to export!", foreground="red")
#             return

#         self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#         self.build_samples_from_treeview()
#         self.add_pre_blanks()
#         self.add_post_blanks()
#         self.add_standby_sample()
#         self.samples = sorted(self.samples, key=self.blanks_first)

#         self.export_final_samples_list_to_csv()
#         self.label.config(text="Sample list correctly generated!", foreground="green")
