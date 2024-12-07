# ![stash-ico](/Users/trevortomesh/Github/stash/images/stash-ico.png)<u>Stash</u> 

**Stash** is a simple, yet powerful Python-based tool that helps you organize and manage files in a directory. It sorts files into folders based on their extensions or MIME types, with the ability to define custom sorting rules interactively.

---

## Features

- **Automatic Sorting**: Organize files based on file extensions or MIME types.
- **Interactive Rules**: Define rules for new file types on the fly.
- **Persistent Rules**: Automatically saves sorting rules to `rules.json`.
- **File Logging**: See where files are sorted during an update.
- **Lightweight**: No dependencies beyond standard Python libraries.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/stash.git
   cd stash
   ```

2. **Make the Script Executable**:
   ```bash
   chmod +x stash
   ```

3. **Move to a System Path**:
   ```bash
   sudo mv stash /usr/local/bin/
   ```

4. Verify the installation:
   ```bash
   stash --help
   ```

---

## Usage

### 1. Initialize a Stash

Run the following command to initialize the current directory as a stash:
```bash
stash init
```

---

### 2. Update a Stash

To sort new files added to the directory, run:
```bash
stash update
```

---

## License

This project is licensed under the [MIT License](LICENSE).
