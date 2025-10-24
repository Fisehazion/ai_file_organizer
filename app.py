import streamlit as st
from file_organizer import FileOrganizer
import os
import shutil
from config import AppConfig
import logging

logging.basicConfig(level=AppConfig.LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

# Main UI
st.title("AI File Organizer")
st.markdown("""
    Organize your local folders with ease! Enter the path to a folder, and the app will categorize files into 
    **Documents**, **Images**, **Videos**, and **Others** based on their extensions. Duplicate files are skipped.
""")

# Initialize FileOrganizer
organizer = FileOrganizer()

# Input for local folder path
folder_path = st.text_input("Enter the path to your local folder (e.g., C:/Users/user/Desktop/TestFolder):", "")

if st.button("Organize"):
    if not folder_path:
        st.error("Please enter a valid folder path.")
    elif not os.path.isdir(folder_path):
        st.error(f"Invalid folder path: {folder_path}")
    else:
        with st.spinner("Organizing files..."):
            try:
                # Get list of files to process
                files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                total_files = min(len(files), AppConfig.MAX_FILES_TO_PROCESS)
                moved_files = []
                skipped_files = []

                # Initialize progress bar and status text
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Process files with progress updates
                for i, file_name in enumerate(files):
                    if i >= AppConfig.MAX_FILES_TO_PROCESS:
                        break
                    file_path = os.path.join(folder_path, file_name)
                    file_ext = os.path.splitext(file_name)[1].lower()
                    file_hash = organizer.get_file_hash(file_path)

                    # Update progress
                    progress = (i + 1) / total_files
                    progress_bar.progress(min(progress, 1.0))
                    status_text.text(f"Processing file {i + 1}/{total_files}: {file_name}")

                    # Check for duplicates
                    if file_hash in organizer.file_hashes:
                        logging.info(f"Skipping duplicate file: {file_name} (matches {organizer.file_hashes[file_hash]})")
                        skipped_files.append(f"{file_name} (duplicate of {organizer.file_hashes[file_hash]})")
                        continue

                    # Determine category
                    category = 'Others'
                    for cat, extensions in organizer.categories.items():
                        if file_ext in extensions:
                            category = cat
                            break

                    # Move file
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
                        organizer.file_hashes[file_hash] = file_name
                        moved_files.append(f"{file_name} -> {category}/{os.path.basename(destination_path)}")
                        logging.info(f"Moved {file_name} to {category}")
                    except Exception as e:
                        logging.error(f"Failed to move {file_name}: {str(e)}")
                        skipped_files.append(f"{file_name} (error: {str(e)})")

                # Clear progress bar and show results
                progress_bar.empty()
                status_text.empty()
                st.success("Folder organized!")
                
                if moved_files:
                    st.subheader("Moved Files:")
                    for move in moved_files:
                        st.write(f"- {move}")
                
                if skipped_files:
                    st.subheader("Skipped Files:")
                    for skip in skipped_files:
                        st.write(f"- {skip}")
                
                if not moved_files and not skipped_files:
                    st.info("No files were found to organize.")
            except Exception as e:
                st.error(f"Error organizing folder: {str(e)}")
                logging.error(f"Error organizing folder {folder_path}: {str(e)}")

st.markdown("""
    ### How It Works
    - Files are categorized based on their extensions:
      - **Documents**: .txt, .doc, .docx, .pdf, .xls, .xlsx, .ppt, .pptx
      - **Images**: .jpg, .jpeg, .png, .gif, .bmp, .tiff
      - **Videos**: .mp4, .avi, .mkv, .mov, .wmv
      - **Others**: All other file types
    - Duplicate files (based on content) are skipped.
    - Files with the same name are renamed automatically (e.g., file.txt -> file_1.txt).
""")

# Footer with Social Media Links and Glowing Developer Credit
st.markdown("---")
st.markdown("""
    <style>
        .footer {
            text-align: center;
            padding: 20px 0;
        }
        .social-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 10px;
        }
        .social-links a {
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
            color: #333;
            font-size: 16px;
        }
        .social-links a:hover {
            color: #007bff;
        }
        .glow-text {
            font-size: 18px;
            font-weight: bold;
            color: #00f;
            text-shadow: 0 0 5px #00f, 0 0 10px #00f, 0 0 20px #00f;
            animation: glow 1.5s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from {
                text-shadow: 0 0 5px #00f, 0 0 10px #00f, 0 0 20px #00f;
            }
            to {
                text-shadow: 0 0 10px #00f, 0 0 20px #00f, 0 0 30px #00f;
            }
        }
    </style>
    <div class="footer">
        <div class="social-links">
            <a href="https://www.linkedin.com/in/fisehatsion-adisu-abute-929279208" target="_blank">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" alt="LinkedIn" width="24" height="24">
                LinkedIn
            </a>
            <a href="https://www.instagram.com/fisehatsionadisu?igsh=NW93Mzd2aW5qN3hz" target="_blank">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/instagram.svg" alt="Instagram" width="24" height="24">
                Instagram
            </a>
            <a href="https://www.facebook.com/dfisa.adisu" target="_blank">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/facebook.svg" alt="Facebook" width="24" height="24">
                Facebook
            </a>
            <a href="https://t.me/fisiha1224" target="_blank">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/telegram.svg" alt="Telegram" width="24" height="24">
                Telegram
            </a>
            <a href="https://github.com/Fisehazion" target="_blank">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" alt="GitHub" width="24" height="24">
                GitHub
            </a>
        </div>
        <div class="glow-text">Developed by Fisehatsion Adisu @ 2025</div>
    </div>
""", unsafe_allow_html=True)