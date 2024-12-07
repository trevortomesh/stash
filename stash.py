#!/usr/bin/env python3

import os
import json
import shutil
from datetime import datetime, timedelta
import argparse


class DirectoryStash:
    STASH_DIR = ".stash"
    STASH_FILE = "stash.json"

    def __init__(self, directory=None):
        self.directory = os.path.abspath(directory or os.getcwd())
        self.stash_dir = os.path.join(self.directory, self.STASH_DIR)
        self.stash_file = os.path.join(self.stash_dir, self.STASH_FILE)
        self.stash_data = self._load_stash()

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
        print("Stash initialized successfully.")

    def update(self):
        print("Updating stash...")
        now = datetime.now()
        deepstash_days = self.stash_data.get("deepstash_days", 30)
        external_drive = self.stash_data.get("external_drive")

        if not external_drive:
            print("Error: No external drive configured for deep stash.")
            return

        deepstashed_count = 0
        soon_to_be_stashed = 0

        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".ds") or root.startswith(self.stash_dir):
                    continue  # Skip ghost files and internal .stash files

                file_path = os.path.join(root, file)

                # Ensure the file still exists before proceeding
                if not os.path.exists(file_path):
                    print(f"Skipping missing file: {file_path}")
                    continue

                try:
                    last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                except FileNotFoundError:
                    print(f"File not found, skipping: {file_path}")
                    continue

                days_since_modified = (now - last_modified).days

                # Handle deepstashing
                if days_since_modified >= deepstash_days:
                    self._move_to_deepstash(file_path, external_drive)
                    deepstashed_count += 1
                elif days_since_modified >= (deepstash_days - 5):
                    soon_to_be_stashed += 1

        self._save_stash()
        print(f"Update complete. Files deep-stashed: {deepstashed_count}")
        print(f"Files soon to be deep-stashed: {soon_to_be_stashed}")

    def status(self):
        print("=== Stash Status ===")
        total_files = len(self.stash_data["items"])
        local_files = sum(1 for item in self.stash_data["items"] if item.get("location") == "LOCAL")
        deepstashed_files = sum(1 for item in self.stash_data["items"] if item.get("location") == "DEEP_STASH")

        print(f"Total Files Tracked: {total_files}")
        print(f"Files in Local Storage: {local_files}")
        print(f"Files in Deep Stash: {deepstashed_files}")

    def force_deepstash(self, files):
        external_drive = self.stash_data.get("external_drive")
        if not external_drive:
            print("Error: No external drive configured for deep stash.")
            return

        for file in files:
            file_path = os.path.abspath(file)
            if not os.path.exists(file_path):
                print(f"File not found: {file}")
                continue

            self._move_to_deepstash(file_path, external_drive)
        self._save_stash()

    def restore(self, timeframe=None, folder=None, file_to_restore=None):
        print("Restoring deep-stashed files...")
        now = datetime.now()

        for root, _, files in os.walk(self.directory):
            for file in files:
                if not file.endswith(".ds"):
                    continue

                ghost_file_path = os.path.join(root, file)
                with open(ghost_file_path, "r") as ghost_file:
                    data = json.load(ghost_file)

                deep_stash_path = data["deep_stash_path"]
                original_path = data["original_path"]

                if file_to_restore and os.path.abspath(file_to_restore) != os.path.abspath(original_path):
                    continue

                if folder and not os.path.abspath(original_path).startswith(os.path.abspath(folder)):
                    continue

                if timeframe:
                    days_ago = now - timedelta(days=int(timeframe))
                    modified_date = datetime.fromisoformat(data["modified_at"])
                    if modified_date < days_ago:
                        continue

                if os.path.exists(deep_stash_path):
                    os.makedirs(os.path.dirname(original_path), exist_ok=True)
                    shutil.copy2(deep_stash_path, original_path)
                    os.remove(ghost_file_path)
                    print(f"Restored '{original_path}'")

    def _move_to_deepstash(self, file_path, external_drive):
        deepstash_dir = os.path.join(external_drive, "deepstash")
        os.makedirs(deepstash_dir, exist_ok=True)
        deepstash_path = os.path.join(deepstash_dir, os.path.basename(file_path))
        shutil.copy2(file_path, deepstash_path)
        os.remove(file_path)

        ghost_file_path = f"{file_path}.ds"
        with open(ghost_file_path, "w") as ghost_file:
            json.dump({"deep_stash_path": deepstash_path, "original_path": file_path}, ghost_file)
        print(f"Deep-stashed '{file_path}' -> '{deepstash_path}'")

    def _load_stash(self):
        return json.load(open(self.stash_file, "r")) if os.path.exists(self.stash_file) else {"items": []}

    def _save_stash(self):
        with open(self.stash_file, "w") as file:
            json.dump(self.stash_data, file, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Manage a directory stash.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Initialize the stash.")
    subparsers.add_parser("update", help="Update the stash.")
    subparsers.add_parser("status", help="Show stash status.")
    deepstash_parser = subparsers.add_parser("deepstash", help="Force deepstash files.")
    deepstash_parser.add_argument("files", nargs="+", help="Files to deepstash.")

    restore_parser = subparsers.add_parser("restore", help="Restore files.")
    restore_parser.add_argument("--timeframe", type=int, help="Restore files within N days.")
    restore_parser.add_argument("--folder", type=str, help="Restore files from a folder.")
    restore_parser.add_argument("--file", type=str, help="Restore a specific file.")

    args = parser.parse_args()
    stash = DirectoryStash()

    if args.command == "init":
        stash.initialize()
    elif args.command == "update":
        stash.update()
    elif args.command == "status":
        stash.status()
    elif args.command == "deepstash":
        stash.force_deepstash(args.files)
    elif args.command == "restore":
        stash.restore(timeframe=args.timeframe, folder=args.folder, file_to_restore=args.file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()