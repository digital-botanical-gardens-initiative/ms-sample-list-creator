import csv
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog

import pandas as pd
import requests


class csvBatch(tk.Frame):
    def __init__(self, csv_batch_window: tk.Toplevel, root: tk.Tk):
        """
        Initializes an instance of the class.

        Args:
            csv_batch_window(tk.Toplevel): The parent widget where this frame will be placed.
            root(tk.Tk): The root window to perform actions on it.

        Returns:
            None
        """
        self.csv_batch_window = csv_batch_window
        self.root = root

        # Make CsvWindow wait for AskBoxPrefixWindow result
        self.root.withdraw()

        self.csv_batch_window.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.operator = str(os.environ.get("OPERATOR"))
        self.output_folder = os.environ.get("OUTPUT_FOLDER")
        self.ms_id = str(os.environ.get("MS_ID"))
        self.col_rack_size = int(str(os.environ.get("COL_RACK_NUMBER")))
        self.row_rack_size = int(str(os.environ.get("ROW_RACK_NUMBER")))
        self.pre_blk = int(str(os.environ.get("PRE_BLK")))
        self.post_blk = int(str(os.environ.get("POST_BLK")))
        self.blk_name = str(os.environ.get("BLK_NAME"))
        self.blk_pos = str(os.environ.get("BLK_POS"))
        self.inj_volume = int(str(os.environ.get("INJ_VOLUME")))
        self.access_token = str(os.environ.get("ACCESS_TOKEN"))
        self.method_file = str(os.environ.get("METHOD_FILE"))
        self.data_path = str(os.environ.get("DATA_FOLDER"))
        self.standby_file = str(os.environ.get("STANDBY_FILE"))
        self.file = str(os.environ.get("FILE"))
        self.current_position = 1
        self.current_row = 1
        self.timestamp = "202404101527"#datetime.now().strftime("%Y%m%d%H%M")
        self.csv_path = f"{self.output_folder}/{datetime.now().strftime('%Y%m%d')}_{self.operator}_dbgi_{self.file}.csv"

        self.warning_label = tk.Label(
            self.csv_batch_window,
            text="Warning, this mode is exclusively made to submit sample lists that have already been made using this tool.",
        )
        self.warning_label.pack()

        label = tk.Label(self.csv_batch_window, text="Search for your CSV:", pady=10)
        label.pack()

        import_button = tk.Button(
            self.csv_batch_window, text="Import your CSV", width=17, command=self.import_csv, pady=10
        )
        import_button.pack()

        button_submit = tk.Button(self.csv_batch_window, text="Submit", width=17, command=self.submit_result, pady=10)
        button_submit.pack()

        button_back = tk.Button(self.csv_batch_window, text="Go back to home", width=17, command=self.on_exit, pady=10)
        button_back.pack()

    def on_exit(self) -> None:
        """
        Defines behaviour when user quits this window (by x button or specified button).

        Args:
            None

        Returns:
            None
        """
        self.csv_batch_window.destroy()
        self.root.deiconify()

    def import_csv(self) -> None:
        """
        Asks the path to input CSV.

        Args:
            None

        Returns:
            None
        """
        os.environ["FILE_PATH"] = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    def submit_result(self) -> None:
        """
        performs modifications on the CSV, submit them to directus and writes the output csv.

        Args:
            None

        Returns:
            None
        """
        # Retrieves file path and method name given by the user
        file_path = os.environ.get("FILE_PATH")
        self.file = str(os.environ.get("FILE"))

        # Converts the CSV to a dataframe
        df = pd.read_csv(str(file_path), skiprows=1)

        # Delete standby row
        df = df.drop(df.index[-1])

        # Remove blanks
        patterns = ["pre", "post"]
        combined_patterns = "|".join(patterns)
        filtered_df = df[~df["File Name"].str.contains(combined_patterns, regex=True)]

        # Update data path, instrument method and injection volume
        path = self.data_path.replace("/", "\\")
        instrument_method = self.method_file.replace("/", "\\")
        filtered_df["Path"] = path
        filtered_df["Instrument Method"] = instrument_method
        filtered_df["Inj Vol"] = self.inj_volume

        # Change timestamp and operator initials
        filtered_df["File Name"] = df["File Name"].apply(
            lambda x: "_".join([self.timestamp, self.operator] + x.split("_")[2:])
        )

        # Prepare data for directus
        directus_df = filtered_df
        directus_df = directus_df.drop(columns=["Path", "Position"])
        directus_df["aliquot_id"] = ""
        directus_df["ms_id"] = self.ms_id
        directus_df = directus_df.rename(columns={"File Name": "mass_spec_id"})
        directus_df = directus_df.rename(columns={"Inj Vol": "injection_volume"})
        directus_df = directus_df.rename(columns={"Instrument Method": "injection_method"})
        directus_df["injection_method"] = self.file
        for index, row in directus_df.iterrows():  # Iterate over rows using iterrows()
            parts = row["mass_spec_id"].split("_")  # Split the "File Name" column by underscores
            aliquot_id = "_".join(parts[2:])  # Extract the desired parts of the split string
            directus_df.at[index, "aliquot_id"] = aliquot_id

        # Send data to directus
        records = directus_df.to_json(orient="records")
        base_url = "http://directus.dbgi.org"
        collection_url = base_url + "/items/Mass_Spectrometry_Analysis"
        session = requests.Session()
        headers = {"Content-Type": "application/json"}
        session.headers.update({"Authorization": f"Bearer {self.access_token}"})
        response = session.post(url=collection_url, headers=headers, data=records)

        # Check if correctly added to directus
        if response.status_code == 200:
            self.warning_label.config(text="Success!! Writing CSV...", foreground="green")
            # Write data to the CSV file
            with open(self.csv_path, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                # Write headers
                csv_writer.writerow(["Bracket Type=4", "", "", "", ""])
                csv_writer.writerow(["File Name", "Path", "Instrument Method", "Position", "Inj Vol"])

                # Write pre blanks
                if self.pre_blk > 0:
                    for i in range(1, self.pre_blk + 1):
                        padded_number = str(i).zfill(2)
                        filename = (
                            self.timestamp + "_" + self.operator + "_dbgi_" + self.blk_name + "_blk_pre" + padded_number
                        )
                        path = self.data_path.replace("/", "\\")
                        instrument_method = self.method_file.replace("/", "\\")
                        position = self.blk_pos
                        inj_volume = self.inj_volume
                        csv_writer.writerow([filename, path, instrument_method, position, inj_volume])
                else:
                    print("no pre blanks")

                # Write data
                csv_writer.writerows(filtered_df.values)

                # Write post blanks
                if self.post_blk > 0:
                    for i in range(1, self.post_blk + 1):
                        padded_number = str(i).zfill(2)
                        filename = (
                            self.timestamp
                            + "_"
                            + self.operator
                            + "_dbgi_"
                            + self.blk_name
                            + "_blk_post"
                            + padded_number
                        )
                        path = self.data_path.replace("/", "\\")
                        instrument_method = self.method_file.replace("/", "\\")
                        position = self.blk_pos
                        inj_volume = self.inj_volume
                        csv_writer.writerow([filename, path, instrument_method, position, inj_volume])
                else:
                    print("no post blanks")

                # Write standby line
                parts = self.standby_file.split("/")
                file = parts[-1]
                filename = self.timestamp + "_" + self.operator + "_" + file
                path = self.data_path.replace("/", "\\")
                standby = self.standby_file.replace("/", "\\")
                position = self.blk_pos
                inj_volume = self.inj_volume
                csv_writer.writerow([filename, path, standby, position, inj_volume])

            # Close the Tkinter window
            self.csv_batch_window.destroy()
            self.root.destroy()
        else:
            self.warning_label.config(text="Directus error, please check your CSV.", foreground="red")
