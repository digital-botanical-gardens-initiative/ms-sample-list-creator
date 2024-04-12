import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog


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
        self.blk_pos = str(os.environ.get("LK_POS"))
        self.inj_volume = int(str(os.environ.get("INJ_VOLUME")))
        self.access_token = str(os.environ.get("ACCESS_TOKEN"))
        self.method_file = str(os.environ.get("METHOD_FILE"))
        self.data_path = str(os.environ.get("DATA_FOLDER"))
        self.standby_file = str(os.environ.get("STANDBY_FILE"))
        self.file = str(os.environ.get("FILE"))
        self.current_position = 1
        self.current_row = 1
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M")
        self.csv_path = f"{self.output_folder}/{datetime.now().strftime('%Y%m%d')}_{self.operator}_dbgi_{self.file}.csv"

        warning_label = tk.Label(
            self.csv_batch_window,
            text="Warning, this mode is exclusively made to submit sample lists that have already been made using this tool.",
        )
        warning_label.pack()

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
        print("correctly written")
