import os
import logging
import shutil
from pathlib import Path
import hashlib
from config import AppConfig

logging.basicConfig(level=AppConfig.LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

class FileOrganizer:
    def __init__(self):
        self.categories = {
            'Documents': ['.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
            'Others': []
        }
        self.file_hashes = {}  # Initialize file_hashes as instance attribute

    def get_file_hash(self, file_path):
        """Calculate MD5 hash of a file to detect duplicates."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def organize_files(self, folder_path):
        """Organize files in the given folder into categorized subfolders."""
        if not os.path.isdir(folder_path):
            logging.error(f"Invalid folder path: {folder_path}")
            raise ValueError(f"Invalid folder path: {folder_path}")

        # Create category folders
        for category in self.categories:
            category_path = os.path.join(folder_path, category)
            os.makedirs(category_path, exist_ok=True)

        moved_files = []
        skipped_files = []
        max_files = AppConfig.MAX_FILES_TO_PROCESS

        # Iterate through files
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and len(moved_files) < max_files:
                file_ext = os.path.splitext(file_name)[1].lower()
                file_hash = self.get_file_hash(file_path)

                # Check for duplicates
                if file_hash in self.file_hashes:
                    logging.info(f"Skipping duplicate file: {file_name} (matches {self.file_hashes[file_hash]})")
                    skipped_files.append(f"{file_name} (duplicate of {self.file_hashes[file_hash]})")
                    continue

                # Determine category
                category = 'Others'
                for cat, extensions in self.categories.items():
                    if file_ext in extensions:
                        category = cat
                        break

                # Move file
                destination_folder = os.path.join(folder_path, category)
                destination_path = os.path.join(destination_folder, file_name)

                # Handle filename conflicts
                base, ext = os.path.splitext(file_name)
                counter = 1
                while os.path.exists(destination_path):
                    new_name = f"{base}_{counter}{ext}"
                    destination_path = os.path.join(destination_folder, new_name)
                    counter += 1

                try:
                    shutil.move(file_path, destination_path)
                    self.file_hashes[file_hash] = file_name
                    moved_files.append(f"{file_name} -> {category}/{os.path.basename(destination_path)}")
                    logging.info(f"Moved {file_name} to {category}")
                except Exception as e:
                    logging.error(f"Failed to move {file_name}: {str(e)}")
                    skipped_files.append(f"{file_name} (error: {str(e)})")

        return moved_files, skipped_files