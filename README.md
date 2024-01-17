# OSX Big File Cleanup

This Python script is designed to search for files larger than a specified size within a given directory and then offers the user the option to safely delete or permanently shred these files.


## Features

- **File Search**: Locate files exceeding a specified size threshold.
- **Interactive Display**: Presents each file's details in a readable ASCII box format.
- **Permanent Shredding**: Securely overwrite and delete files from the safe location.


## Requirements

- Python 3.x
- Operating system: Compatible with major operating systems (Windows, macOS, Linux)


## Usage

1. **Running the Script**: 
   - Navigate to the script's directory in the terminal or command prompt.
   - Run the script using: `python3 main.py`

2. **Input Parameters**:
   - When prompted, enter the directory path to search and the minimum file size in megabytes.

3. **File Handling Options**:
   - For each file listed, choose to either 'delete' or 'keep'.


## Safety and Security

- File shredding involves overwriting file data, making recovery extremely difficult.
- Always verify the importance and necessity of file deletion before proceeding.



