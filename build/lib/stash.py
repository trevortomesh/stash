#!/usr/bin/env python3

import os
import json
import shutil
import argparse
from datetime import datetime
import mimetypes

class DirectoryStash:
    STASH_DIR = ".stash"
    STASH_FILE = "stash.json"
    RULES_FILE = "rules.json"
    FOLDER_SORT_DIR = "Folders"

    def __init__(self, directory=None):
        self.directory = os.path.abspath(directory or os.getcwd())
        self.stash_dir = os.path.join(self.directory, self.STASH_DIR)
        self.stash_file = os.path.join(self.stash_dir, self.STASH_FILE)
        self.rules_file = os.path.join(self.stash_dir, self.RULES_FILE)
        self.stash_data = self._load_stash()
        self.rules = self._load_rules()
        self.error_cache = set()

    def initialize(self):
        if os.path.exists(self.stash_file):
            print("Stash already initialized.")
            return

        self.stash_data = {
            "name": os.path.basename(self.directory),
            "created_at": datetime.now().isoformat(),
            "items": []
        }

        os.makedirs(self.stash_dir, exist_ok=True)
        self._save_stash()
        self._save_rules()
        print("Stash initialized successfully.")

    def update(self, verbose=False):
        print("Updating stash...")
        now = datetime.now()

        all_files = []
        subdirs_to_sort = []

        top_level = os.listdir(self.directory)
        for item in top_level:
            full_path = os.path.join(self.directory, item)
            if os.path.isdir(full_path):
                if item not in (self.STASH_DIR, "Keep", self.FOLDER_SORT_DIR) and item not in set(self.rules.get("extensions", {}).values()):
                    subdirs_to_sort.append(full_path)
            elif os.path.isfile(full_path) and not item.startswith('.'):
                all_files.append(full_path)

        for folder in subdirs_to_sort:
            if os.path.abspath(folder) == os.path.abspath(os.path.join(self.directory, self.FOLDER_SORT_DIR)):
                continue
            dest = os.path.join(self.directory, self.FOLDER_SORT_DIR, os.path.basename(folder))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            try:
                shutil.move(folder, dest)
                if verbose:
                    print(f"Moved folder '{folder}' to '{dest}'")
            except Exception as e:
                if verbose:
                    print(f"Could not move '{folder}' to '{dest}': {e}")

        for file_path in all_files:
            try:
                result = self._sort_file(file_path)
                if result and verbose:
                    print(f"Moved '{file_path}' to '{result}'")
            except Exception as e:
                print(f"Skipped '{file_path}': {e}")

        self._save_stash()
        self._save_rules()
        print("Update complete.")

    def status(self):
        print("Stash status:")
        print(json.dumps(self.stash_data, indent=4))

    def _sort_file(self, file_path):
        extension = os.path.splitext(file_path)[1][1:].lower()
        if extension in self.rules.get("ignore", []):
            return  # Skip this file
        mime_type, _ = mimetypes.guess_type(file_path)
        target_folder = None

        if extension in self.rules.get("extensions", {}):
            target_folder = self.rules["extensions"][extension]
        elif mime_type in self.rules.get("mime_types", {}):
            target_folder = self.rules["mime_types"][mime_type]

        if not target_folder:
            response = input(f"No rule for '.{extension}'. Where should these files go? [Leave blank to skip]: ").strip()
            if not response:
                raise ValueError(f"No sorting rule for extension '.{extension}'")
            self.rules["extensions"][extension] = response
            self._save_rules()
            target_folder = response

        target_dir = os.path.join(self.directory, target_folder)
        os.makedirs(target_dir, exist_ok=True)
        new_path = os.path.join(target_dir, os.path.basename(file_path))
        shutil.move(file_path, new_path)
        return new_path

    def _load_rules(self):
        return json.load(open(self.rules_file, "r")) if os.path.exists(self.rules_file) else {"extensions": {}, "mime_types": {}}

    def _save_rules(self):
        with open(self.rules_file, "w") as file:
            json.dump(self.rules, file, indent=4)

    def _load_stash(self):
        return json.load(open(self.stash_file, "r")) if os.path.exists(self.stash_file) else {"items": []}

    def _save_stash(self):
        os.makedirs(self.stash_dir, exist_ok=True)
        with open(self.stash_file, "w") as file:
            json.dump(self.stash_data, file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Manage a directory stash.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Initialize the stash.")
    update_parser = subparsers.add_parser(
        "update",
        help="Update the stash (sorts files in root, prompts for new types, supports 'ignore' list in rules.json)."
    )
    update_parser.add_argument("--verbose", action="store_true", help="Show detailed update actions.")

    status_parser = subparsers.add_parser("status", help="Show stash status.")

    args = parser.parse_args()
    stash = DirectoryStash()

    if args.command == "init":
        stash.initialize()
    elif args.command == "update":
        stash.update(verbose=args.verbose)
    elif args.command == "status":
        stash.status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
