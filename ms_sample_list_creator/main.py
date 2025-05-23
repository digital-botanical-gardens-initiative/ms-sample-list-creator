# Run "pyinstaller --onefile main.py"
# Generated binaries are made for the native system where the pyinstaller command is run.

# You can generate windows executable from linux using wine, by previously installing wine, python 3.8.20, pyinstaller and
# other non-built-in packages (here requests and pandas) inside wine. Then run: wine PyInstaller --onefile main.py

import tkinter as tk

import requests

from .home import HomeWindow
from .new_version_available import NewVersionAvailable


def main() -> None:
    check_version()


if __name__ == "__main__":
    main()


def check_version() -> None:
    """
    Checks if the current version of the script is up to date.

    Args:
        None

    Returns:
        None
    """

    # Send a request to github to know if this version is the las one
    release_url = (
        "https://api.github.com/repos/digital-botanical-gardens-initiative/ms-sample-list-creator/releases/latest"
    )
    session = requests.Session()
    response = session.get(release_url)
    data = response.json()["tag_name"]
    tag = float(str.replace(data, "v.", ""))

    if tag >= 2.0:
        # Create an instance of new vesion available class
        root = tk.Tk()
        root.title("New version available")
        root.minsize(550, 100)

        # Create an instance of the HomeWindow class
        new = NewVersionAvailable(root)

        # Display the HomeWindow
        new.pack()

        # Start the tkinter event loop
        root.mainloop()
    else:
        # Create an instance of the main window
        root = tk.Tk()
        root.title("Home")
        root.minsize(550, 650)

        # Create an instance of the HomeWindow class
        home = HomeWindow(root)

        # Display the HomeWindow
        home.pack()

        # Start the tkinter event loop
        root.mainloop()
