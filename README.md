<p align="center">
  <img src="images/stash-with-text.png" alt="Stash logo" width="300"/>
</p>

<p align="center">
  <img alt="Python 3.6+" src="https://img.shields.io/badge/Python-3.6+-blue?logo=python&logoColor=white&style=flat-square"/>
  <img alt="Vibe-Coded" src="https://img.shields.io/badge/Vibe%20Coded-%F0%9F%92%8C-purple?style=flat-square"/>
  <a href="https://github.com/trevortomesh/fearfully-coded">
    <img alt="Fearfully Coded" src="https://img.shields.io/badge/🕊️Fearfully%20Coded-blue?style=flat-square"/>
  </a>
</p>

----

# ![stash-ico](images/stash-ico.png) <u>Stash</u>

**Stash** is a lightweight, powerful Python-based directory management tool. It allows you to sort and organize files with ease.

---

## Features

- **Automatic Sorting**: Sort files into predefined folders (e.g., `Images`, `Documents`) based on file extensions or MIME types.
- **Interactive Rules**: Create new rules interactively when Stash encounters unknown file types.
- **Persistent Configuration**: Sorting rules are saved in `rules.json` for future use.
- **Status Command**: View a detailed summary of your stash, including the number of tracked files.
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

### Step 2: Install with pip

Install Stash using pip:

```bash
pip install stash-organizer
```

Or, if you cloned the repository locally:

```bash
pip install .
```

Verify the installation by running:

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

---

### 2. Update a Stash

To sort new files:

```bash
stash update
```

- Files are sorted into appropriate folders.

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

Total Files Tracked: 50
Files in Local Storage: 35
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

#### Step 4: Check Status

```bash
stash status
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

---

## Related Projects

- **DeepStash** – A sister project to Stash that provides advanced long-term archival and external drive backup for deeply cold files.  
  [https://github.com/trevortomesh/deep-stash](https://github.com/trevortomesh/deep-stash)

----
## 🧠 Philosophy
Stash began as a conceptual data structure — a digital “box” where users could throw anything with the intention of sorting it later. Inspired by the human habit of stashing files and folders into catch-all directories, this project set out to turn that chaos into structured automation.
What started as an abstract idea evolved into a real-world command-line tool that helps users organize their filesystem with minimal effort and maximum flexibility.
----
## 🤖 Note

This tool was created using **vibe coding** — describing what I wanted to an AI assistant, refining the results through iteration. No detailed plan — just intuition, adaptation, and execution.

----
## 🕊️ Dedication

This project is dedicated to the Lord.

All logic, structure, and order — including the very foundations of programming — reflect the perfection of His design. May this tool, in its small way, point toward the beauty and coherence He has written into the fabric of creation.

> **"I praise you, for I am fearfully and wonderfully made.  
> Wonderful are your works; my soul knows it very well."**  
> — Psalm 139:14

**Soli Deo Gloria.**
