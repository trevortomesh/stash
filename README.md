# ![stash-ico](images/stash-ico.png)<u>Stash</u>

**Stash** is a lightweight and powerful Python-based directory sorting tool. It helps you quickly organize and manage files in a directory by sorting them into folders based on file extensions or MIME types. Stash also allows you to interactively define sorting rules for new file types.

---

## Features

- **Automatic Sorting**: Sort files into predefined folders (e.g., `Images`, `Documents`) based on file extensions or MIME types.
- **Interactive Rules**: When a new file type is encountered, you can create a rule interactively.
- **Persistent Configuration**: All sorting rules are saved to `rules.json` for future use.
- **Log of Sorted Files**: Stash shows where files were moved during an update.
- **Lightweight**: Runs as a simple Python script with no external dependencies.

---

## Installation

### Prerequisites

Ensure you have **Python 3** installed on your system. You can check this by running:
```bash
python3 --version
```
Step 1: Download Stash

Clone the Stash repository or download the script directly:
```bash
git clone https://github.com/yourusername/stash.git
cd stash
```
Alternatively, download the standalone script (stash) and place it in a directory of your choice.

Step 2: Make Stash Executable
   1. Make the script executable:
```bash
chmod +x stash
```

   2. Move the script to a directory in your system path, such as /usr/local/bin:
```bash
sudo mv stash /usr/local/bin/
```

   3. Verify the installation by running:
```bash
stash --help
```
---
Usage

1. Initialize a Stash

Navigate to the directory you want to organize and initialize a stash:
```bash
stash init
```
This command:
   •  Creates a .stash folder to store configurations.
   •  Logs the current files in stash.json.
   •  Sets up default sorting rules (e.g., .png files to Images/, .pdf files to Documents/).

2. Update a Stash

To sort and organize new files in the directory, run:
```bash
stash update
```
What happens during an update:
   •  Stash sorts files into appropriate folders based on the rules defined in rules.json.
   •  If Stash encounters a new file type (e.g., .txt), it will ask you interactively where to place it:

No rule exists for files with the extension .txt
Where should .txt files be sorted? (Enter folder name or press Enter to skip):

Newly defined rules are saved persistently for future use.

---
Example Workflow

Step 1: Create a Stash
```bash
mkdir MyFiles
cd MyFiles
stash init
```
Step 2: Add Some Files
```
MyFiles/
├── photo1.png
├── report.pdf
├── notes.txt
```
Step 3: Update the Stash
```bash
stash update
```
Resulting Directory Structure:
```
MyFiles/
├── Documents/
│   └── report.pdf
├── Images/
│   └── photo1.png
├── notes.txt
```
If .txt has no rule, Stash will prompt:
```bash
No rule exists for files with the extension .txt
Where should .txt files be sorted? (Enter folder name or press Enter to skip):
```
---
Configuration

Rules
   •  Rules are stored in the rules.json file inside the .stash directory.
   •  Example:

   ```json
{
    "extensions": {
        "png": "Images",
        "pdf": "Documents",
        "txt": "TextFiles"
    },
    "mime_types": {
        "application/pdf": "Documents",
        "image/png": "Images"
    }
}
```


You can edit this file manually to add or modify rules.

Tips
   •  To skip sorting a specific file type when prompted, simply press Enter.
   •  If you accidentally create an incorrect rule, you can edit rules.json manually.
   •  Stash logs sorted files during updates so you always know where they are moved.
---
Uninstalling Stash

To remove Stash from your system:
   1. Delete the executable from /usr/local/bin:
```bash
sudo rm /usr/local/bin/stash
```

   2. Remove the .stash folder in any directories where Stash was used:
```bash
rm -rf .stash
```
---
Contributing

Contributions are welcome! To contribute:
   1. Fork the repository.
   2. Create a feature branch:
```bash
git checkout -b feature-name
```

   3. Commit your changes and push:
```bash
git commit -m "Add a new feature"
git push origin feature-name
```

   4. Open a pull request.
---
License

This project is licensed under the MIT License.

Support

For feedback or issues, please open an issue on the GitHub repository.

---

### Next Steps

1. Save this as `README.md` in your project repository.
2. Commit and push it to GitHub:
```bash
git add README.md
git commit -m "Add detailed README file with usage instructions"
git push origin main
```
