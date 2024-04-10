import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog

import home_page


class csvBatch(tk.Frame):
    def __init__(self, csv_path, parent, *args, **kwargs):
        """
        Initializes an instance of the class.

        Args:
            root(tk.Tk): The parent widget or window where this frame will be placed.
            csv_path(str): CSV path and name.

        Returns:
            None
        """
        print("csv batch")

        tk.Frame.__init__(self, csv_path, parent, *args, **kwargs)

        self.operator = str(os.environ.get("OPERATOR"))
        self.ms_id = str(os.environ.get("MS_ID"))
        self.col_rack_size = int(str(os.environ.get("COL_RACK_NUMBER")))
        self.row_rack_size = int(str(os.environ.get("ROW_RACK_NUMBER")))
        self.pre_blk = int(str(os.environ.get("PRE_BLK")))
        self.post_blk = int(str(os.environ.get("POST_BLK")))
        self.blk_name = str(os.environ.get("BLK_NAME"))
        self.blk_pos = str(os.environ.get("LK_POS"))
        self.inj_volume = int(str(os.environ.get("INJ_VOLUME")))
        self.access_token = str(os.environ.get("ACCESS_TOKEN"))
        self.method_file = str(os.environ.get("METHOD_FILE"))
        self.data_path = str(os.environ.get("DATA_FOLDER"))
        self.standby_file = str(os.environ.get("STANDBY_FILE"))
        self.csv_path = csv_path
        self.current_position = 1
        self.current_row = 1
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M")

        # Create widgets for the main page
        label = tk.Label(self, text="Search for your CSV:")
        label.pack()

        import_button = tk.Button(self, text="Import your CSV", width=17, command=self.import_csv)
        import_button.pack()

        button_submit = tk.Button(self, text="Submit", command=self.show_values)
        button_submit.pack()

        button_back = tk.Button(self, text="Back to Main Page", command=self.back_to_main)
        button_back.pack()

    def import_csv(self):
        os.environ["file_path"] = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    def show_values(self):
        print("correctly written")

    def back_to_main(self):
        # Destroy Window 2 and show the main page
        self.destroy()
        home_page.HomeWindow.pack()
