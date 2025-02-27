# Prompt-Creator

Prompt-Creator is a GUI application that allows you to visualize, customize, and generate text-based representations of your project folder structure. It not only displays the directory tree with toggleable checkboxes but also lets you modify an exclusion configuration on the fly, generate output either to the clipboard or to a file, and even supports an automated release process via GitHub Actions.

## Overview

Prompt-Creator helps you:
- **Select and visualize a project folder:** Automatically load the last used folder or choose a new one.
- **Customize directory and file inclusion:** Use checkboxes and an editable JSON exclusion file to fine-tune which files and folders appear in your output.
- **Generate comprehensive output:** Create a text file (or clipboard content) that not only shows the folder hierarchy but also includes file contents for text-based files.
- **Automate releases:** With GitHub Actions and PyInstaller, build a standalone executable for your application.
- **Support development and testing:** Comes with a PowerShell project structure script and unit tests to help maintain code quality.

## Features

- **Graphical User Interface:** A Tkinter-based window for folder selection, exclusion editing, and previewing the generated structure.
- **Exclusion Management:** Dynamic handling of files and directories based on rules defined in `Exclude.json`.
- **Flexible Output Modes:** Choose between clipboard-only output or saving the prompt to a file.
- **Automated Build and Release:** A GitHub Actions workflow (in `.github/workflows/release.yml`) builds the project using PyInstaller and packages it into a release archive.
- **Testing Framework:** Unit tests in the `tests` folder ensure that the core functionalities work as expected.
- **Project Setup Script:** A PowerShell script (`CreateProjectStructure.ps1`) creates the necessary directory and file structure for new projects.

## Installation

### Prerequisites
- Python 3.x installed on your system.
- Tkinter (usually included with Python).
- [PyInstaller](https://www.pyinstaller.org/) for building executables.

### Setup Steps
1. Clone the repository:
   git clone https://github.com/yourusername/prompt-creator.git
   cd prompt-creator
2. Install dependencies:
   pip install -r requirements.txt
3. (Optional) To set up the project structure in a new location, run the PowerShell script:
   .\CreateProjectStructure.ps1

## Usage Scenarios

### 1. Basic Usage
- **Scenario:** You want to quickly generate a text representation of your project folder.
- **Steps:**
  1. Run the application by executing `python src/main.py`.
  2. Select your project folder using the provided folder selection window.
  3. Review the tree view and toggle checkboxes as needed.
  4. Click the **Generate** button to copy the output to the clipboard (or save it to a file, depending on your output mode).

### 2. Customizing Exclusions
- **Scenario:** You have specific files or directories that you want to omit from the output.
- **Steps:**
  1. In the main window, click the **Edit Exclude** button.
  2. Modify the JSON in the editor window (e.g., add new directory names to `excludedDirectories`).
  3. Save your changes and see the tree refresh with the updated exclusions.

### 3. Advanced Output Generation
- **Scenario:** You need both a clipboard copy and a physical output file for documentation or further processing.
- **Steps:**
  1. In the main window, select the **Clipboard and File** radio button.
  2. (Optional) Change the output file path by clicking **Browse**.
  3. Click **Generate** to update the clipboard and write the output to the specified file.

### 4. Automated Release Process
- **Scenario:** You want to build and distribute your application.
- **Steps:**
  1. Create a release on GitHub.
  2. The GitHub Actions workflow (`.github/workflows/release.yml`) triggers automatically.
  3. The workflow checks out the code, sets up Python, installs PyInstaller, builds an executable, packages necessary resources, and uploads the release asset.

### 5. Development and Testing
- **Scenario:** You are developing new features or debugging issues.
- **Steps:**
  1. Run the unit tests located in the `tests` folder:
     python -m unittest discover -s tests
  2. Use the provided PowerShell script (`CreateProjectStructure.ps1`) to set up a consistent development environment.
  3. Modify the source in `src/` and test your changes using the included test files.

## Project Structure
<pre>
prompt-creator
├── .github
│   └── workflows
│       └── release.yml
├── docs
│   └── README.md
├── resources
│   ├── Config.json
│   └── Exclude.json
├── src
│   ├── __init__.py
│   ├── main.py
│   └── test_tk.py
├── tests
│   ├── __init__.py
│   └── test_main.py
├── .gitignore
├── CreateProjectStructure.ps1
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
</pre>

## Contributing

Contributions are welcome! Please follow these steps:
- Fork the repository.
- Create a feature branch.
- Commit your changes with clear messages.
- Open a pull request describing your changes.

## License

This project is licensed under the terms specified in the LICENSE file.

## Additional Information

For more detailed documentation about the application’s architecture and release process, see the Documentation (./docs/README.md).