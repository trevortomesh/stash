#!/usr/bin/env python3

import os
import json
import shutil
import argparse
from datetime import datetime, timedelta
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

        external_drive = input("Enter the path to the external drive for deep stash: ").strip()
        deepstash_days = input("Enter days before files are deep-stashed (default: 30): ").strip()

        self.stash_data = {
            "name": os.path.basename(self.directory),
            "created_at": datetime.now().isoformat(),
            "external_drive": os.path.abspath(external_drive) if external_drive else None,
            "deepstash_days": int(deepstash_days) if deepstash_days.isdigit() else 30,
            "items": []
        }

        os.makedirs(self.stash_dir, exist_ok=True)
        self._save_stash()
        self._save_rules()
        print("Stash initialized successfully.")

    def update(self, verbose=False):
        print("Updating stash...")
        now = datetime.now()

        if not self.stash_data.get("external_drive"):
            while True:
                external_drive = input("No deepstash location set. Enter the path to the external drive for deep stash: ").strip()
                if external_drive and os.path.isdir(external_drive):
                    self.stash_data["external_drive"] = os.path.abspath(external_drive)
                    self._save_stash()
                    print(f"Deepstash location set to: {self.stash_data['external_drive']}")
                    break
                else:
                    print("Invalid path. Please enter a valid directory path.")

        external_drive = self.stash_data["external_drive"]
        deepstash_days = self.stash_data.get("deepstash_days", 30)

        all_files = []
        subdirs_to_sort = []

        top_level = os.listdir(self.directory)
        for item in top_level:
            full_path = os.path.join(self.directory, item)
            if os.path.isdir(full_path):
                if item not in (self.STASH_DIR, "Keep", self.FOLDER_SORT_DIR) and item not in set(self.rules.get("extensions", {}).values()):
                    subdirs_to_sort.append(full_path)
            elif os.path.isfile(full_path) and not item.startswith('.') and not item.endswith(".ds"):
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

        deepstashed_count = 0
        soon_to_be_stashed = []

        folders_dir = os.path.join(self.directory, self.FOLDER_SORT_DIR)
        if os.path.exists(folders_dir):
            for folder_name in os.listdir(folders_dir):
                folder_path = os.path.join(folders_dir, folder_name)
                if not os.path.isdir(folder_path):
                    continue
                try:
                    folder_mtime = datetime.fromtimestamp(os.path.getmtime(folder_path))
                    days_since_modified = (now - folder_mtime).days
                    if days_since_modified >= deepstash_days:
                        self._move_folder_to_deepstash(folder_path, external_drive)
                        deepstashed_count += 1
                    elif days_since_modified >= (deepstash_days - 5):
                        soon_to_be_stashed.append((folder_path, deepstash_days - days_since_modified))
                except Exception as e:
                    err_msg = str(e)
                    if err_msg not in self.error_cache:
                        print(f"Error processing folder '{folder_path}': {err_msg}")
                        self.error_cache.add(err_msg)

        for file_path in all_files:
            try:
                self._sort_file(file_path)
            except Exception as e:
                if verbose:
                    print(f"Error sorting file '{file_path}': {e}")

        self._save_stash()
        self._save_rules()
        print(f"Update complete. Files deep-stashed: {deepstashed_count}")
        print(f"Folders soon to be deep-stashed: {len(soon_to_be_stashed)}")
        for path, days in soon_to_be_stashed:
            print(f"  → {path} in {days} days")

    def status(self):
        print("Stash status:")
        print(json.dumps(self.stash_data, indent=4))

    def force(self, target):
        full_path = os.path.join(self.directory, target)
        external_drive = self.stash_data.get("external_drive")
        if not external_drive:
            print("No deepstash location set.")
            return
        if os.path.isdir(full_path):
            self._move_folder_to_deepstash(full_path, external_drive)
            print(f"Folder '{target}' forcibly deep-stashed.")
        elif os.path.isfile(full_path):
            self._move_file_to_deepstash(full_path, external_drive)
            print(f"File '{target}' forcibly deep-stashed.")
        else:
            print(f"Target '{target}' does not exist.")

    def restore(self, target):
        if not target.endswith(".ds"):
            target += ".ds"
        ghost_path = os.path.join(self.directory, self.STASH_DIR, target)
        if not os.path.exists(ghost_path):
            print(f"No .ds file found for '{target}'.")
            return
        with open(ghost_path, "r") as f:
            data = json.load(f)
        if data["type"] == "folder":
            shutil.copytree(data["deep_stash_path"], data["original_path"], dirs_exist_ok=True)
            print(f"Restored folder: {data['original_path']}")
        else:
            shutil.copy2(data["deep_stash_path"], data["original_path"])
            print(f"Restored file: {data['original_path']}")

    def _move_folder_to_deepstash(self, folder_path, external_drive):
        deepstash_dir = os.path.join(external_drive, "deepstash")
        os.makedirs(deepstash_dir, exist_ok=True)
        dest = os.path.join(deepstash_dir, os.path.basename(folder_path))
        shutil.copytree(folder_path, dest, dirs_exist_ok=True)
        shutil.rmtree(folder_path)

        ghost_file_path = f"{folder_path}.ds"
        with open(ghost_file_path, "w") as ghost_file:
            json.dump({
                "type": "folder",
                "deep_stash_path": dest,
                "original_path": folder_path,
                "modified_at": datetime.now().isoformat()
            }, ghost_file)

    def _move_file_to_deepstash(self, file_path, external_drive):
        deepstash_dir = os.path.join(external_drive, "deepstash")
        os.makedirs(deepstash_dir, exist_ok=True)
        dest = os.path.join(deepstash_dir, os.path.basename(file_path))
        shutil.copy2(file_path, dest)
        os.remove(file_path)

        ghost_file_path = f"{file_path}.ds"
        with open(ghost_file_path, "w") as ghost_file:
            json.dump({
                "type": "file",
                "deep_stash_path": dest,
                "original_path": file_path,
                "modified_at": datetime.now().isoformat()
            }, ghost_file)

    def _sort_file(self, file_path):
        extension = os.path.splitext(file_path)[1][1:].lower()
        mime_type, _ = mimetypes.guess_type(file_path)
        target_folder = None

        if extension in self.rules.get("extensions", {}):
            target_folder = self.rules["extensions"][extension]
        elif mime_type in self.rules.get("mime_types", {}):
            target_folder = self.rules["mime_types"][mime_type]

        if not target_folder:
            raise ValueError(f"No sorting rule for extension '.{extension}'")

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
    update_parser = subparsers.add_parser("update", help="Update the stash.")
    update_parser.add_argument("--verbose", action="store_true", help="Show detailed update actions.")

    status_parser = subparsers.add_parser("status", help="Show stash status.")
    force_parser = subparsers.add_parser("force", help="Force deepstash of a file or folder.")
    force_parser.add_argument("target", help="The file or folder to force stash.")
    restore_parser = subparsers.add_parser("restore", help="Restore a specific file or folder from stash.")
    restore_parser.add_argument("target", help="The name of the .ds file or item to restore.")

    args = parser.parse_args()
    stash = DirectoryStash()

    if args.command == "init":
        stash.initialize()
    elif args.command == "update":
        stash.update(verbose=args.verbose)
    elif args.command == "status":
        stash.status()
    elif args.command == "force":
        stash.force(args.target)
    elif args.command == "restore":
        stash.restore(args.target)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
