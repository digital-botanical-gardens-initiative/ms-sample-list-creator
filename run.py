# Run "pyinstaller --onefile run.py --hidden-import=PIL._tkinter_finder --hidden-import=PIL.ImageTk"
# Generated binaries are made for the native system where the pyinstaller command is run.

# You can generate windows executable from linux using wine, by previously installing wine, python 3.8.20, pyinstaller and
# other non-built-in packages (here requests and pandas) inside wine. Then run: wine PyInstaller --onefile run.py --hidden-import=PIL._tkinter_finder --hidden-import=PIL.ImageTk

from ms_sample_list_creator.main import main

if __name__ == "__main__":
    main()
