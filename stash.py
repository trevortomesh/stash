import os
import json
import mimetypes
import shutil
from datetime import datetime
import argparse
import readline


class DirectoryStash:
    STASH_DIR = ".stash"
    STASH_FILE = "stash.json"
    RULES_FILE = "rules.json"
    SCRIPT_NAME = "stash.py"

    def __init__(self, directory=None):
        self.directory = os.path.abspath(directory or os.getcwd())
        self.stash_dir = os.path.join(self.directory, self.STASH_DIR)
        self.stash_file = os.path.join(self.stash_dir, self.STASH_FILE)
        self.rules_file = os.path.join(self.stash_dir, self.RULES_FILE)
        self.rules = self._load_rules()

    def initialize(self):
        if not os.path.isdir(self.directory):
            print(f"Error: {self.directory} is not a valid directory.")
            return

        os.makedirs(self.stash_dir, exist_ok=True)

        if os.path.exists(self.stash_file):
            print("Stash already initialized in this directory.")
            return

        default_rules = {
            "extensions": {
                "png": "Images",
                "pdf": "Documents"
            },
            "mime_types": {
                "application/pdf": "Documents",
                "image/png": "Images"
            }
        }

        # Save default rules
        with open(self.rules_file, "w") as file:
            json.dump(default_rules, file, indent=4)
        print(f"Default rules file created at {self.rules_file}")

        stash_data = {
            "name": os.path.basename(self.directory),
            "created_at": datetime.now().isoformat(),
            "items": []
        }
        self._save_stash(stash_data)

        # Sort and handle unsorted files
        self.update(prompt_unsorted=True)
        print(f"Stash initialized successfully in {self.directory}.")

    def update(self, prompt_unsorted=False):
        if not os.path.exists(self.stash_file):
            print("Error: Stash is not initialized. Run 'init' first.")
            return

        stash_data = self._load_stash()
        current_files = self._get_root_files()
        existing_files = {item["filename"] for item in stash_data["items"]}
        sorted_files = []

        new_items = []
        for file in current_files:
            if file == self.SCRIPT_NAME or file in existing_files:
                continue  # Skip stash.py and already processed files

            file_path = os.path.join(self.directory, file)
            sorted_path = self._sort_file(file_path, prompt_unsorted)
            if sorted_path != file_path:
                file = os.path.relpath(sorted_path, self.directory)
                sorted_files.append((file_path, sorted_path))
            new_items.append({
                "filename": file,
                "absolute_path": os.path.abspath(sorted_path),
                "size": os.path.getsize(sorted_path),
                "created_at": datetime.fromtimestamp(os.path.getctime(sorted_path)).isoformat(),
                "modified_at": datetime.fromtimestamp(os.path.getmtime(sorted_path)).isoformat(),
                "type": mimetypes.guess_type(sorted_path)[0] or "unknown"
            })

        if new_items:
            stash_data["items"].extend(new_items)
            self._save_stash(stash_data)

        # Display sorted files
        if sorted_files:
            print("\nFiles sorted:")
            for original, destination in sorted_files:
                print(f"  - {original} -> {destination}")
        else:
            print("\nNo new files were sorted.")

    def _sort_file(self, file_path, prompt_unsorted):
        file_extension = os.path.splitext(file_path)[1][1:].lower()
        mime_type, _ = mimetypes.guess_type(file_path)

        # Check rules
        category = None
        if file_extension in self.rules.get("extensions", {}):
            category = self.rules["extensions"][file_extension]
        elif mime_type in self.rules.get("mime_types", {}):
            category = self.rules["mime_types"][mime_type]

        # Prompt user if no rule exists and prompt_unsorted is True
        if not category and prompt_unsorted:
            category = self._ask_unsorted_file(file_extension)
            # Save the decision, even if it's a skip
            self.rules["extensions"][file_extension] = category
            self._save_rules()

        # Skip sorting if no category is assigned
        if not category:
            return file_path

        # Move file to the sorted directory
        sorted_dir = os.path.join(self.directory, category)
        os.makedirs(sorted_dir, exist_ok=True)
        new_path = os.path.join(sorted_dir, os.path.basename(file_path))
        shutil.move(file_path, new_path)
        return new_path

    def _ask_unsorted_file(self, file_extension):
        if file_extension in self.rules.get("extensions", {}):
            return self.rules["extensions"][file_extension]

        print(f"No rule exists for files with the extension .{file_extension}")
        readline.set_completer(self._folder_completer)
        readline.parse_and_bind("tab: complete")
        while True:
            folder = input(f"Where should .{file_extension} files be sorted? (Enter folder name or press Enter to skip): ").strip()
            if folder == "":  # Pressing Enter skips
                print(f"Skipping .{file_extension} files.")
                return None
            return folder

    def _folder_completer(self, text, state):
        folders = [f for f in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, f))]
        matches = [folder for folder in folders if folder.startswith(text)]
        return matches[state] if state < len(matches) else None

    def _get_root_files(self):
        """Get only files in the root directory (not in subdirectories) and skip stash.py."""
        return [
            f for f in os.listdir(self.directory)
            if os.path.isfile(os.path.join(self.directory, f)) and f != self.SCRIPT_NAME
        ]

    def _load_rules(self):
        if os.path.exists(self.rules_file):
            with open(self.rules_file, "r") as file:
                return json.load(file)
        return {"extensions": {}, "mime_types": {}}

    def _save_rules(self):
        with open(self.rules_file, "w") as file:
            json.dump(self.rules, file, indent=4)

    def _load_stash(self):
        with open(self.stash_file, "r") as file:
            return json.load(file)

    def _save_stash(self, stash_data):
        with open(self.stash_file, "w") as file:
            json.dump(stash_data, file, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Manage a stash in a directory.")
    parser.add_argument(
        "command",
        metavar="command",
        type=str,
        choices=["init", "update"],
        help="Command to execute: 'init' to initialize, 'update' to update stash."
    )
    parser.add_argument(
        "directory",
        metavar="directory",
        type=str,
        nargs="?",
        default=None,
        help="The stash directory (defaults to the current working directory)."
    )

    args = parser.parse_args()

    stash = DirectoryStash(args.directory)
    if args.command == "init":
        stash.initialize()
    elif args.command == "update":
        stash.update()


if __name__ == "__main__":
    main()
