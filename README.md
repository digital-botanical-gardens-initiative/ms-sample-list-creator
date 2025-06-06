# ms-sample-list-creator

[![Release](https://img.shields.io/github/v/release/digital-botanical-gardens-initiative/ms-sample-list-creator)](https://img.shields.io/github/v/release/digital-botanical-gardens-initiative/ms-sample-list-creator)
[![Build status](https://img.shields.io/github/actions/workflow/status/digital-botanical-gardens-initiative/ms-sample-list-creator/main.yml?branch=main)](https://github.com/digital-botanical-gardens-initiative/ms-sample-list-creator/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/digital-botanical-gardens-initiative/ms-sample-list-creator)](https://img.shields.io/github/commit-activity/m/digital-botanical-gardens-initiative/ms-sample-list-creator)

A tool to automatically genereate MS sample lists for the EMI project

- **Github repository**: <https://github.com/digital-botanical-gardens-initiative/ms-sample-list-creator/>

### 1. Clone the repository to your local machine:

```bash
git clone https://github.com/digital-botanical-gardens-initiative/ms-sample-list-creator.git
cd ms-sample-list-creator
```

### 2. set up an environment with `poetry`:

Install necessary packages:

```bash
poetry install
```

Then activate the environment:

```bash
poetry shell # For older poetry versions until 1.8.5
poetry env create # For newer poetry versions since 2.0.0
```

If you do not have poetry, you can install it with the command:

```bash
pipx install poetry
```

### 3. Use the software directly in python environment

Run `run.py` script:

```bash
python run.py
```

The software should appear.

### 4. Generate a binary for production use

These binaries are availables in [releases](https://github.com/digital-botanical-gardens-initiative/ms-sample-list-creator/releases)

For your own Operating system:

```bash
poetry run pyinstaller --onefile run.py --hidden-import=PIL._tkinter_finder --hidden-import=PIL.ImageTk
```

To generate windows binary from a Linux system:

```bash
wine PyInstaller --onefile run.py --hidden-import=PIL._tkinter_finder --hidden-import=PIL.ImageTk
```

To do this, you need to install wine, python in the wine environment and poetry or all needed packages manually using pip.

## Contributing

If you would like to contribute to this project or report issues, please follow our contribution guidelines.

## License

see [LICENSE](https://github.com/digital-botanical-gardens-initiative/qfieldcloud-fetcher/blob/main/LICENSE) for details.
