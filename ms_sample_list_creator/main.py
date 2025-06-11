import requests
import ttkbootstrap as tb

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

    if tag > 2.1:
        # Create an instance of new vesion available class
        root = tb.Window(themename="sandstone")
        root.title("New version available")

        # Create an instance of the HomeWindow class
        new = NewVersionAvailable(root)

        # Display the HomeWindow
        new.pack()

        # Start the tkinter event loop
        root.mainloop()
    else:
        # Create an instance of the main window
        root = tb.Window(themename="sandstone")
        root.title("Home")
        root.minsize(550, 650)

        # Create an instance of the HomeWindow class
        home = HomeWindow(root)

        # Display the HomeWindow
        home.pack()

        # Start the tkinter event loop
        root.mainloop()
