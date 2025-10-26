import streamlit as st
from file_organizer import FileOrganizer
import os
import zipfile
import tempfile
import shutil
from config import AppConfig
import logging

# Conditional imports for AI functionality
try:
    import PyPDF2
    from transformers import pipeline
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

logging.basicConfig(level=AppConfig.LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

# Main UI
st.title("SmartSort")
st.markdown("""
    Organize your files with ease! Upload a zip file of your folder, and **SmartSort** will categorize files into 
    **Documents**, **Images**, **Videos**, **Audio**, and **Others** based on their extensions. AI-based content analysis for text files is available locally.
""")

# Initialize FileOrganizer
organizer = FileOrganizer()

# File upload for web app
uploaded_file = st.file_uploader("Upload a zip file containing your files (e.g., TestFolder.zip):", type="zip")

# AI categorization toggle (only if AI is available)
use_ai = st.checkbox("Use AI-based categorization for text files (e.g., .pdf, .txt)", value=False, disabled=not AI_AVAILABLE)

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
                        f.write(uploaded_file.read())

                    # Unzip to temp folder
                    unzip_dir = os.path.join(temp_dir, "unzip")
                    os.makedirs(unzip_dir, exist_ok=True)
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(unzip_dir)

                    # Initialize AI classifier if enabled and available
                    classifier = None
                    if use_ai and AI_AVAILABLE:
                        classifier = pipeline("text-classification", model=AppConfig.AI_MODEL_NAME)

                    # Organize files using FileOrganizer
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    moved_files, skipped_files = organizer.organize_files(unzip_dir, progress_bar, status_text, use_ai=use_ai, classifier=classifier)

                    # Create clean output directory for organized files
                    output_dir = os.path.join(temp_dir, "output")
                    os.makedirs(output_dir, exist_ok=True)

                    # Move only organized category folders to output_dir
                    for category in ['Documents', 'Images', 'Videos', 'Audio', 'Others']:
                        src_category = os.path.join(unzip_dir, category)
                        dst_category = os.path.join(output_dir, category)
                        if os.path.exists(src_category):
                            shutil.move(src_category, dst_category)

                    # Create output zip from organized folders
                    output_zip = os.path.join(temp_dir, "organized_files.zip")
                    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                        for root, _, files in os.walk(output_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, output_dir)
                                zip_ref.write(file_path, arcname)

                    # Clear progress bar and show results
                    progress_bar.empty()
                    status_text.empty()
                    st.success("Files organized! Download the organized files below.")

                    # Provide download link
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
            except zipfile.BadZipFile:
                st.error("Invalid or corrupted zip file. Please upload a valid .zip.")
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
      - **Audio**: .mp3, .wav, .ogg, .flac
      - **Others**: All other file types
    - **AI Categorization** (available locally): Text files (.txt, .pdf) are analyzed for content (e.g., classified as 'Reports', 'Invoices') using a pre-trained AI model.
    - Duplicate files (based on content) are skipped.
    - Files with the same name are renamed automatically (e.g., file.txt -> file_1.txt).
    - Download the organized files as a zip.
""")

# Footer with Social Media Links and Glowing Developer Credit
st.markdown("---")
st.markdown("""
    <style>
        /* Responsive container */
        .main-container {
            max-width: 90vw;
            margin: 0 auto;
            padding: 2rem 1rem;
        }
        /* Title styling */
        h1 {
            font-size: min(5vw, 2.5rem) !important;
            text-align: center;
        }
        /* Markdown and text styling */
        .stMarkdown, .stText {
            font-size: min(4vw, 1.2rem);
            line-height: 1.5;
        }
        /* File uploader and button styling */
        .stFileUploader, .stButton > button {
            width: 100%;
            max-width: 500px;
            margin: 1rem auto;
            font-size: min(4vw, 1rem);
        }
        /* Progress bar and status text */
        .stProgress, .stEmpty {
            max-width: 500px;
            margin: 1rem auto;
        }
        /* Success and error messages */
        .stSuccess, .stError, .stInfo {
            font-size: min(4vw, 1rem);
            padding: 0.5rem;
        }
        /* Subheader and list items */
        .stSubheader, .stMarkdown li {
            font-size: min(4vw, 1.1rem);
        }
        /* Footer styling */
        .footer {
            text-align: center;
            padding: min(4vw, 2rem) 0;
        }
        .social-links {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: min(5vw, 1.5rem);
            margin-bottom: min(2vw, 0.5rem);
        }
        .social-links a {
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: min(2vw, 0.5rem);
            color: #333;
            font-size: min(4vw, 1rem);
        }
        .social-links a:hover {
            color: #007bff;
        }
        .social-links img {
            width: min(6vw, 1.5rem);
            height: min(6vw, 1.5rem);
        }
        .glow-text {
            font-size: min(4.5vw, 1.2rem);
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
        /* Mobile-specific adjustments */
        @media (max-width: 600px) {
            .stFileUploader, .stButton > button {
                max-width: 90vw;
            }
            .stProgress, .stEmpty {
                max-width: 90vw;
            }
            .social-links {
                gap: min(8vw, 1rem);
            }
            .social-links a {
                font-size: min(5vw, 0.9rem);
            }
            .social-links img {
                width: min(8vw, 1.2rem);
                height: min(8vw, 1.2rem);
            }
        }
    </style>
    <div class="main-container">
        <div class="footer">
            <div class="social-links">
                <a href="https://www.linkedin.com/in/fisehatsion-adisu-abute-929279208" target="_blank">
                    <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/linkedin.svg" alt="LinkedIn">
                    LinkedIn
                </a>
                <a href="https://www.instagram.com/fisehatsionadisu?igsh=NW93Mzd2aW5qN3hz" target="_blank">
                    <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/instagram.svg" alt="Instagram">
                    Instagram
                </a>
                <a href="https://www.facebook.com/dfisa.adisu" target="_blank">
                    <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/facebook.svg" alt="Facebook">
                    Facebook
                </a>
                <a href="https://t.me/connectcollab001" target="_blank">
                    <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/telegram.svg" alt="Telegram">
                    Telegram
                </a>
                <a href="https://github.com/Fisehazion" target="_blank">
                    <img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg" alt="GitHub">
                    GitHub
                </a>
            </div>
            <div class="glow-text">Developed by Fisehatsion Adisu @ 2025</div>
        </div>
    </div>
""", unsafe_allow_html=True)