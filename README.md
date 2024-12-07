# ![stash-ico](images/stash-ico.png) <u>Stash</u>

**Stash** is a lightweight, powerful Python-based directory management tool. It allows you to sort, organize, deepstash, and restore files with ease. Stash tracks your files, keeps them organized, and ensures that even long-unused files can be safely stored elsewhere and easily restored when needed.

---

## Features

- **Automatic Sorting**: Sort files into predefined folders (e.g., `Images`, `Documents`) based on file extensions or MIME types.
- **Interactive Rules**: Create new rules interactively when Stash encounters unknown file types.
- **Persistent Configuration**: Sorting rules are saved in `rules.json` for future use.
- **Deep Stash**: Automatically or manually move old files to an external drive for backup, replacing them with lightweight ghost files (`.ds`).
- **Restore**: Restore files:
  - All files.
  - Files within a specific timeframe.
  - Files from a specific folder and subfolders.
  - A specific individual file.
- **Status Command**: View a detailed summary of your stash, including the number of tracked, deep-stashed, and soon-to-be stashed files.
- **Manual Deepstash**: Force deepstash specific files on demand.
- **Lightweight and Portable**: Runs as a single Python script with minimal dependencies.

---

## Installation

### Prerequisites

Ensure you have **Python 3** installed:

```bash
python3 --version
```

### Step 1: Download Stash

Clone the repository:

```bash
git clone https://github.com/trevortomesh/stash.git
cd stash
```

Or download the standalone script.

### Step 2: Install Stash Globally

Run the installation script:

```bash
chmod +x install.sh
./install.sh
```

This will:

1. Make `stash` executable.
2. Place it in `/usr/local/bin/` for global use.

### Step 3: Verify Installation

```bash
stash --help
```

---

## Usage

### 1. Initialize a Stash

To start using Stash in a directory:

```bash
stash init
```

This command:

- Creates a `.stash` folder to store configurations and logs.
- Logs all files in `stash.json`.
- Sets up a default deepstash threshold (30 days).

---

### 2. Update a Stash

To sort new files and deepstash old files:

```bash
stash update
```

- Files are sorted into appropriate folders.
- Files older than the deepstash threshold (30 days by default) are deep-stashed and replaced with `.ds` ghost files.
- Files close to the threshold (within 5 days) are flagged as "soon to be deep-stashed."

---

### 3. View Stash Status

To check the current state of the stash:

```bash
stash status
```

Example Output:

```
=== Stash Status ===
Stash Name: MyFiles
External Drive: /Volumes/WD_BLACK
Deepstash Threshold: 30 days

Total Files Tracked: 50
Files in Local Storage: 35
Files in Deep Stash: 15
Files Soon to Be Deep-Stashed: 5
```

---

### 4. Manual Deepstash

Force specific files to deepstash:

```bash
stash deepstash file1.txt file2.pdf
```

This moves the specified files to the external deepstash directory and replaces them with ghost files.

---

### 5. Restore Files

Restore deep-stashed files using one of the options:

- **Restore All Files**:

  ```bash
  stash restore
  ```

- **Restore Files from the Last 7 Days**:

  ```bash
  stash restore --timeframe 7
  ```

- **Restore Files from a Specific Folder**:

  ```bash
  stash restore --folder /path/to/folder
  ```

- **Restore a Specific File**:

  ```bash
  stash restore --file /path/to/file.txt
  ```

Example Output:

```
Restoring deep-stashed files...
Restored '/Users/user/Documents/file1.pdf'
Restored '/Users/user/Desktop/file2.png'
Restoration complete. Files restored: 2
```

---

### Example Workflow

#### Step 1: Create a Stash

```bash
mkdir MyFiles
cd MyFiles
stash init
```

#### Step 2: Add Files

```
MyFiles/
├── photo1.png
├── report.pdf
├── notes.txt
```

#### Step 3: Update Stash

```bash
stash update
```

Resulting Structure:

```
MyFiles/
├── Documents/
│   └── report.pdf
├── Images/
│   └── photo1.png
├── notes.txt
```

#### Step 4: Force Deepstash a File

```bash
stash deepstash notes.txt
```

#### Step 5: Check Status

```bash
stash status
```

#### Step 6: Restore Files

Restore `notes.txt`:

```bash
stash restore --file notes.txt
```

---

## Configuration

### Rules

Rules are saved in `rules.json` within the `.stash` directory:

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

Edit this file manually to add or modify rules.

---

### Tips

- To **skip sorting** a file type during prompts, press **Enter**.
- Edit `rules.json` to fix incorrect sorting rules.
- Use `stash status` regularly to monitor the state of your files.

---

## Uninstallation

### Remove the Stash Executable

```bash
sudo rm /usr/local/bin/stash
```

### Remove `.stash` Configuration Folders

In directories where Stash was used:

```bash
rm -rf .stash
```

---

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.

2. Create a feature branch:

   ```bash
   git checkout -b feature-name
   ```

3. Commit and push:

   ```bash
   git commit -m "Add feature X"
   git push origin feature-name
   ```

4. Open a pull request.

---

## License

This project is licensed under the MIT License.

---

## Support

For feedback, questions, or issues, please open an issue on the GitHub repository.
