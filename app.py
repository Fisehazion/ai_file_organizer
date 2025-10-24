import streamlit as st
from file_organizer import FileOrganizer
import os
import shutil
import zipfile
import tempfile
from config import AppConfig
import logging

logging.basicConfig(level=AppConfig.LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

# Main UI
st.title("AI File Organizer")
st.markdown("""
    Organize your files with ease! Upload a zip file of your folder, and the app will categorize files into 
    **Documents**, **Images**, **Videos**, and **Others** based on their extensions. Duplicate files are skipped.
""")

# Initialize FileOrganizer
organizer = FileOrganizer()

# File upload for web app
uploaded_file = st.file_uploader("Upload a zip file containing your files (e.g., TestFolder.zip):", type="zip")

if st.button("Organize"):
    if not uploaded_file:
        st.error("Please upload a zip file.")
    else:
        with st.spinner("Organizing files..."):
            try:
                # Create temporary directories
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Save uploaded zip
                    zip_path = os.path.join(temp_dir, "uploaded.zip")
                    with open(zip_path, "wb") as f:
                        f.write(uploaded_file.read())  # Read directly to avoid memory issues

                    # Unzip to temp folder
                    unzip_dir = os.path.join(temp_dir, "unzip")
                    os.makedirs(unzip_dir, exist_ok=True)
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(unzip_dir)

                    # Initialize progress bar and status text
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    # Organize files using FileOrganizer
                    moved_files, skipped_files = organizer.organize_files(unzip_dir, progress_bar, status_text)

                    # Create output zip
                    output_zip = os.path.join(temp_dir, "organized_files.zip")
                    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                        for root, _, files in os.walk(unzip_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, unzip_dir)
                                zip_ref.write(file_path, arcname)

                    # Clear progress bar and show results
                    progress_bar.empty()
                    status_text.empty()
                    st.success("Files organized! Download the organized files below.")

                    # Provide download link with saved file
                    with open(output_zip, "rb") as f:
                        st.download_button(
                            label="Download Organized Files",
                            data=f.read(),
                            file_name="organized_files.zip",
                            mime="application/zip"
                        )

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
                st.error(f"Error organizing files: {str(e)}")
                logging.error(f"Error organizing files: {str(e)}")

st.markdown("""
    ### How It Works
    - Upload a zip file containing your files.
    - Files are categorized based on their extensions:
      - **Documents**: .txt, .doc, .docx, .pdf, .xls, .xlsx, .ppt, .pptx
      - **Images**: .jpg, .jpeg, .png, .gif, .bmp, .tiff
      - **Videos**: .mp4, .avi, .mkv, .mov, .wmv
      - **Others**: All other file types
    - Duplicate files (based on content) are skipped.
    - Files with the same name are renamed automatically (e.g., file.txt -> file_1.txt).
    - Download the organized files as a zip.
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