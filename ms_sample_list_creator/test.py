# import tkinter as tk
# from tkinter import ttk
# from typing import Any

# from ms_sample_list_creator.sample_list import SampleList
# from ms_sample_list_creator.structure import (
#     Batch,
#     Blank,
#     DirectusCredentials,
#     Instrument,
#     MassSpectrometry,
#     Method,
#     ProjectPath,
#     Rack,
# )


# class TestWindow(ttk.Frame):
#     """
#     Class to display a message when a new version of the application is available.
#     """

#     def __init__(self, root: tk.Tk, *args: Any, **kwargs: Any):
#         """
#         Initializes an instance of the class.

#         Args:
#             parent(tk.Tk): The parent widget or window where this frame will be placed.
#             csv_path(str): CSV path and name.

#         Returns:
#             None
#         """
#         self.root = root

#         ttk.Frame.__init__(self, root, *args, **kwargs)

#         self.access_token = "TODO: Add access token here"
#         self.credentials = DirectusCredentials(username="test", password="test")

#         self.mass_spectrometry = MassSpectrometry(operator_initials="AB", injection_volume=1.0)

#         self.instrument = Instrument(name="inst_000002", identifier=2)

#         self.batch = Batch(
#             name="batch_000058",
#             identifier=109,
#         )

#         self.blank = Blank(blank_name="blk", blank_position="G:A1", blank_pre=3, blank_post=3)
#         method1 = Method(
#             name="test",
#             #path="C:/Users/username/Documents/methods/test.meth",
#             identifier=21,
#         )

#         method2 = Method(
#             name="test2",
#             #path="C:/Users/username/Documents/methods/test2.meth",
#             identifier=20,
#         )

#         self.methods = [method1, method2]

#         self.paths = ProjectPath(
#             methods=self.methods,
#             standby="C:/Users/username/Documents/standby.meth",
#             data="C:/Users/username/Documents/data",
#             output="/home/heloise/repositories/ms-sample-list-creator",
#         )

#         self.rack = Rack(
#             column=2,
#             row=2,
#         )

#         self.lauch_button = ttk.Button(self, text="Create Sample List", command=self.create_sample_list)
#         self.lauch_button.pack(pady=10)

#     def create_sample_list(self) -> None:
#         sample_list_window = tk.Toplevel(self)
#         sample_list_window.title("Create Sample List")
#         sample_list_instance = SampleList(
#             sample_list_window,
#             access_token=self.access_token,
#             credentials=self.credentials,
#             mass_spectrometry=self.mass_spectrometry,
#             instrument=self.instrument,
#             batch=self.batch,
#             blank=self.blank,
#             paths=self.paths,
#             methods=self.methods,
#             rack=self.rack,
#         )
#         sample_list_instance.pack(fill="both", expand=True)


# # Create an instance of the main window
# root = tk.Tk()
# root.title("Test")
# root.minsize(550, 650)

# # Create an instance of the HomeWindow class
# home = TestWindow(root)

# # Display the HomeWindow
# home.pack()

# # Start the tkinter event loop
# root.mainloop()
