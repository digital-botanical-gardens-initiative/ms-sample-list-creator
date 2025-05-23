# import csv
# import os
# import tkinter as tk
# from dataclasses import fields
# from datetime import datetime
# from tkinter import filedialog, ttk
# from typing import Any, Optional

# import pandas as pd
# import requests

# from ms_sample_list_creator import utils

# from .structure import DirectusSessionData, TkVariables


# class csvBatch(tk.Frame):
#     def __init__(self, csv_batch_window: tk.Toplevel, root: tk.Tk):
#         """
#         Initializes an instance of the class.

#         Args:
#             csv_batch_window(tk.Toplevel): The parent widget where this frame will be placed.
#             root(tk.Tk): The root window to perform actions on it.

#         Returns:
#             None
#         """
#         super().__init__(csv_batch_window)

#         self.output_folder: Optional[str] = None
#         self.operator: Optional[str] = None
#         self.file: Optional[str] = None

#         self.csv_batch_window = csv_batch_window
#         self.root = root

#         self.tk_vars = TkVariables()
#         self.session_data = DirectusSessionData()

#         # Make CsvWindow wait for AskBoxPrefixWindow result
#         self.root.withdraw()

#         self.csv_batch_window.protocol("WM_DELETE_WINDOW", self.on_exit)

#         # Initialize environment variables
#         self._initialize_env_variables()

#         # CSV file path setup
#         self.timestamp = datetime.now().strftime("%Y%m%d%H%M")
#         self.csv_path = f"{self.output_folder}/{self.timestamp}_{self.operator}_emi_{self.file}.csv"

#         # Create UI components
#         self._create_ui()

#     def _initialize_env_variables(self) -> None:
#         """Initialize environment variables and fill the dataclass fields."""

#         # Initialize TkVariables dataclass
#         self.tk_variables = TkVariables()

#         # Iterate over the fields in the TkVariables dataclass
#         for field in fields(self.tk_variables):
#             field_value = getattr(self.tk_variables, field.name)

#             # Get the environment variable value
#             env_value = os.environ.get(field.name.upper(), None)

#             # If it's a Tkinter StringVar, convert int to str before setting
#             if isinstance(field_value, tk.StringVar):
#                 if env_value is not None:
#                     if isinstance(env_value, int):  # if it's a int, convert to str
#                         field_value.set(str(env_value))
#                     else:
#                         field_value.set(env_value)  # If already a str, set it directly
#             elif isinstance(field_value, tk.IntVar):
#                 if env_value is not None:
#                     field_value.set(int(env_value))  # for IntVar, let it be an int
#             else:
#                 # For regular attributes (e.g. lists, strings), directly assign the value
#                 if env_value is not None:
#                     setattr(self.tk_variables, field.name, env_value)

#         # Special handling for 'method_files', which is a list
#         env_method_files = os.environ.get("METHOD_FILES", "")
#         if env_method_files:
#             self.tk_variables.method_files = [str(k) for k in env_method_files.split(",") if k]

#     def _create_ui(self) -> None:
#         """Create UI components."""

#         """Create UI components."""
#         self.warning_label = tk.Label(
#             self.csv_batch_window,
#             text="Warning, this mode is exclusively made to submit sample lists that have already been made using this tool.",
#         )
#         self.warning_label.pack()

#         label = tk.Label(self.csv_batch_window, text="Search for your CSV:", pady=10)
#         label.pack()

#         self.import_button = ttk.Button(
#             self.csv_batch_window, text="Import your CSV", width=17, command=self.import_csv
#         )
#         self.import_button.pack(pady=10)

#         button_submit = ttk.Button(self.csv_batch_window, text="Submit", width=17, command=self.submit_result)
#         button_submit.pack(pady=10)

#         button_back = ttk.Button(self.csv_batch_window, text="Go back to home", width=17, command=self.on_exit)
#         button_back.pack(pady=10)

#     def on_exit(self) -> None:
#         """Handles window exit."""
#         self.csv_batch_window.destroy()
#         self.root.deiconify()

#     def import_csv(self) -> None:
#         """Prompts user to import a CSV file."""
#         csv_file = os.environ["FILE_PATH"] = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
#         if csv_file:
#             file = csv_file.split("/")[-1]
#             self.import_button.config(text=file)

#     def submit_result(self) -> None:
#         """Processes CSV data and submits it to Directus."""
#         file_path = os.environ.get("FILE_PATH")
#         df = self._load_and_process_csv(file_path)

#         # Update Directus data and write to CSV
#         directus_df = self._prepare_data_for_directus(df)
#         self._send_data_to_directus(directus_df)

#         if self._write_csv(directus_df):
#             self.warning_label.config(text="Sample list correctly generated!", foreground="green")
#             self.csv_batch_window.after(2000, self.destroy_window)
#         else:
#             self.warning_label.config(text="Directus error, please check your CSV.", foreground="red")

#     def _load_and_process_csv(self, file_path: Optional[str]) -> pd.DataFrame:
#         """Load and preprocess CSV."""
#         df = pd.read_csv(str(file_path), skiprows=1)
#         columns_filter = ["File Name", "Path", "Instrument Method", "Position", "Inj Vol"]
#         df = df.loc[:, columns_filter]
#         df = df.drop(df.index[-1])

#         # Filter out blanks
#         patterns = ["pre", "post"]
#         combined_patterns = "|".join(patterns)
#         df = df[~df["File Name"].str.contains(combined_patterns, regex=True)]

#         # Update paths and injection volume
#         df["Path"] = self.tk_vars.data_path.replace("/", "\\")  # Utilisation de la dataclass TkVariables
#         df["Instrument Method"] = self.tk_vars.method_files[0].replace("/", "\\")  # Premier fichier de méthode
#         df["Inj Vol"] = self.tk_vars.inj_volume

#         # Change file name
#         def format_file_name(file_name: str) -> str:
#             file_name_parts = file_name.split("_")
#             return "_".join([self.timestamp, self.tk_vars.operator] + file_name_parts[2:])

#         df["File Name"] = df["File Name"].apply(format_file_name)

#         return df

#     def _prepare_data_for_directus(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Prepare data for Directus API."""
#         directus_df = df.drop(columns=["Path", "Position"]).rename(columns={"File Name": "filename"})
#         directus_df["parent_sample_container"] = ""
#         directus_df["injection_volume_unit"] = 18
#         directus_df["instrument_used"] = self.session_data.instrument_key
#         directus_df["batch"] = self.session_data.batch_key
#         directus_df = self._add_parent_sample_container(directus_df)

#         # Extend rows for multiple injection methods
#         extended_rows = []
#         for _, row in directus_df.iterrows():
#             for method_key in self.session_data.method_keys:  # Utilisation de DirectusSessionData
#                 new_row = row.copy()
#                 new_row["injection_method"] = method_key
#                 extended_rows.append(new_row)

#         return pd.DataFrame(extended_rows)

#     def _add_parent_sample_container(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Add parent sample container to DataFrame."""
#         for index, row in df.iterrows():
#             filename: str = row["filename"]
#             filename_parts = filename.split("_")
#             aliquot_id = "_".join(filename_parts[2:])
#             df.at[index, "parent_sample_container"] = utils.get_primary_key(
#                 "https://emi-collection.unifr.ch/directus/items/Containers", aliquot_id, "container_id"
#             )
#         return df

#     def _send_data_to_directus(self, df: pd.DataFrame) -> None:
#         """Send data to Directus."""
#         records = df.to_json(orient="records")
#         base_url = "https://emi-collection.unifr.ch/directus"
#         collection_url = base_url + "/items/MS_Data"
#         session = requests.Session()
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {self.session_data.access_token}",
#         }  # Utilisation de DirectusSessionData
#         session.post(url=collection_url, headers=headers, data=records)

#     def _write_csv(self, df: pd.DataFrame) -> bool:
#         """Write CSV output with blanks and standby lines."""
#         try:
#             with open(self.csv_path, "w", newline="") as csv_file:
#                 csv_writer = csv.writer(csv_file)
#                 # Write headers
#                 csv_writer.writerow(["Bracket Type=4", "", "", "", ""])
#                 csv_writer.writerow(["File Name", "Path", "Instrument Method", "Position", "Inj Vol"])

#                 # Write pre and post blanks
#                 self._write_blanks(csv_writer, "pre")
#                 csv_writer.writerows(df.values.tolist())  # Write the DataFrame rows
#                 self._write_blanks(csv_writer, "post")

#                 # Write standby line
#                 self._write_standby_line(csv_writer)
#         except Exception as e:
#             print(f"Error writing CSV: {e}")
#             return False
#         else:
#             return True

#     def _write_blanks(self, csv_writer: Any, blk_type: str) -> None:
#         """Write blank rows to CSV (pre or post)."""
#         # On récupère dynamiquement l'attribut blk_type_blk
#         blk_count = getattr(self.tk_vars, f"{blk_type}_blk")

#         # Utilisation de la dataclass TkVariables
#         for i in range(1, blk_count + 1):
#             padded_number = str(i).zfill(2)
#             # Construction du nom du fichier avec les variables TkVariables
#             filename = (
#                 f"{self.timestamp}_{self.tk_vars.operator}_emi_{self.tk_vars.blk_name}_blk_{blk_type}{padded_number}"
#             )

#             # On écrit la ligne dans le fichier CSV
#             csv_writer.writerow(
#                 [
#                     filename,
#                     self.tk_vars.data_path.replace("/", "\\"),
#                     self.tk_vars.method_files[0].replace("/", "\\"),
#                     self.tk_vars.blk_pos,
#                     self.tk_vars.inj_volume,
#                 ]
#             )

#     def _write_standby_line(self, csv_writer: Any) -> None:
#         """Write standby line to CSV."""
#         parts = self.tk_vars.standby_file.split("/")
#         filename = f"{self.timestamp}_{self.tk_vars.operator}_{parts[-1]}"
#         csv_writer.writerow(
#             [
#                 filename,
#                 self.tk_vars.data_path.replace("/", "\\"),
#                 self.tk_vars.standby_file.replace("/", "\\"),
#                 self.tk_vars.blk_pos,
#                 self.tk_vars.inj_volume,
#             ]
#         )

#     def destroy_window(self) -> None:
#         """Destroys the window and shows the root window."""
#         self.csv_batch_window.destroy()
#         self.root.deiconify()
