# Project Documentation

This documentation provides a comprehensive overview of the Prompt-Creator application, detailing its architecture, configuration, usage scenarios, and release process. It is intended for developers and advanced users who wish to understand the internal workings of the application.

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Configuration Files](#configuration-files)
4. [User Interface Details](#user-interface-details)
5. [Usage Scenarios](#usage-scenarios)
6. [Automated Release Process](#automated-release-process)
7. [Testing and Development](#testing-and-development)
8. [Troubleshooting and FAQs](#troubleshooting-and-faqs)

## Introduction

Prompt-Creator is designed to generate a structured, text-based representation of a project’s folder hierarchy. The application leverages Python’s Tkinter library to provide an interactive GUI that enables users to customize which parts of the project are included in the output.

## Architecture Overview

- **Source Code (src/):**  
  Contains the core application modules:
  - `main.py`: Implements the main GUI and logic for folder selection, tree visualization, exclusion handling, and output generation.
  - `__init__.py`: Initializes the package.
  - `test_tk.py`: A simple window test to verify basic Tkinter functionality.

- **Resources (resources/):**  
  - `Config.json`: Stores configuration data such as the last used project path.
  - `Exclude.json`: Contains lists of directories, files, and path patterns to be excluded from the generated output.

- **Tests (tests/):**  
  Contains unit tests (e.g., `test_main.py`) ensuring the reliability of key functionalities.

- **Project Setup Script:**  
  `CreateProjectStructure.ps1` is a PowerShell script that creates the necessary project directories and files.

- **Release Automation:**  
  The `.github/workflows/release.yml` file defines a GitHub Actions workflow that automates the build and packaging of the application.

## Configuration Files

### Config.json
- **Purpose:** Remembers the last used project folder.
- **Usage:** Automatically loaded when the application starts; updated upon folder selection.

### Exclude.json
- **Purpose:** Defines which directories, files, and patterns should be excluded from the output.
- **Usage:** Editable via the GUI. Changes are immediately reflected in the tree view and output generation.

## User Interface Details

The application features two main windows:

1. **Folder Selection Window:**
   - Prompts the user to choose a project folder.
   - Pre-fills the folder path from Config.json if available.

2. **Main Application Window:**
   - Displays a tree view of the project folder.
   - Checkboxes next to each file/directory indicate inclusion (☑) or exclusion (☐).
   - Buttons allow for editing exclusions, toggling output modes, and generating the output.

Additional UI components include radio buttons for choosing between output modes (clipboard only vs. clipboard and file) and a separate window to display the generated prompt.

## Usage Scenarios

### A. Basic Structure Generation
- **Objective:** Quickly generate a hierarchical text representation of the selected project folder.
- **Flow:**  
  1. Launch the application and select a folder.
  2. Adjust the tree selection if needed.
  3. Click **Generate** to copy the output to the clipboard.

### B. Exclusion Customization
- **Objective:** Fine-tune which parts of the project appear in the output.
- **Flow:**  
  1. Click **Edit Exclude**.
  2. Modify Exclude.json to add or remove items.
  3. Save the changes and observe the updated tree view.

### C. Detailed Output with File Contents
- **Objective:** Include not only the folder structure but also the contents of text-based files.
- **Flow:**  
  1. Choose the **Clipboard and File** output mode.
  2. Generate the output to see both the structure and file contents in the generated prompt.

### D. Automated Release and Distribution
- **Objective:** Build a distributable executable of the application.
- **Flow:**  
  1. Create a new release on GitHub.
  2. The GitHub Actions workflow triggers, builds the executable with PyInstaller, and packages required resources.
  3. A release archive is automatically uploaded.

## Automated Release Process

The release workflow is defined in `.github/workflows/release.yml`:
- **Build:** Uses PyInstaller to create a one-file executable from `src/main.py`.
- **Packaging:** Copies the executable along with configuration files from the resources folder into a release directory.
- **Distribution:** Compresses the release directory into a ZIP file and uploads it as a release asset via GitHub Actions.

## Testing and Development

- **Unit Tests:** Located in the tests directory, these tests help ensure that modifications do not break core functionalities.
- **Development Workflow:**  
  1. Use the PowerShell script to initialize the project structure.
  2. Develop features in src/ and run unit tests using:
     python -m unittest discover -s tests
- **Debugging:** A simple test window (src/test_tk.py) is provided to validate the Tkinter environment.

## Troubleshooting and FAQs

- **Issue: Application Fails to Launch**  
  Check that Python 3.x and Tkinter are correctly installed on your system.

- **Issue: Output Does Not Reflect Exclusion Changes**  
  Ensure that the JSON in Exclude.json is valid. Use the in-app editor to correct any formatting issues.

- **Further Questions:**  
  For additional support, please refer to the GitHub Issues page or contact the maintainers.