import os
import shutil
import hashlib
from config import AppConfig
import logging

class FileOrganizer:
    def __init__(self):
        self.categories = {
            'Documents': ['.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
            'Audio': ['.mp3', '.wav', '.ogg', '.flac'],
            'Others': []
        }
        self.file_hashes = {}

    def get_file_hash(self, file_path):
        """Calculate MD5 hash of a file for duplicate detection."""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logging.error(f"Failed to hash {file_path}: {str(e)}")
            return None

    def organize_files(self, folder_path, progress_bar=None, status_text=None):
        """Organize files in the given folder into category subfolders."""
        moved_files = []
        skipped_files = []
        self.file_hashes.clear()  # Reset hashes to avoid stale data

        # Get all files in folder_path
        files = []
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path):
                    files.append((file_path, os.path.relpath(file_path, folder_path)))

        total_files = min(len(files), AppConfig.MAX_FILES_TO_PROCESS)

        for i, (file_path, rel_path) in enumerate(files):
            if i >= AppConfig.MAX_FILES_TO_PROCESS:
                skipped_files.append(f"{rel_path} (exceeded max files limit)")
                continue

            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower()

            # Update progress
            if progress_bar and status_text:
                progress = (i + 1) / total_files
                progress_bar.progress(min(progress, 1.0))
                status_text.text(f"Processing file {i + 1}/{total_files}: {file_name}")

            # Check for duplicates
            file_hash = self.get_file_hash(file_path)
            if file_hash is None:
                skipped_files.append(f"{file_name} (hashing error)")
                continue
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

            # Move file to category folder
            destination_folder = os.path.join(folder_path, category)
            os.makedirs(destination_folder, exist_ok=True)
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