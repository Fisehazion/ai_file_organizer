User Manual for AI File Organizer App
Overview
The AI File Organizer App helps you organize files by uploading a zip file through a user-friendly Streamlit web interface. It categorizes files into Documents, Images, Videos, and Others based on their extensions, skips duplicates using AI-powered detection, and provides a downloadable organized zip file. Deployed on Streamlit Cloud, it’s perfect for quick file organization without local setup.
Prerequisites

Anaconda: Installed for local development or testing (optional for users).
Browser: Chrome, Firefox, or any modern browser.
Internet: Required to access the deployed app and upload/download zip files.

Setup Instructions (For Developers)

Install Dependencies

Open Anaconda Prompt.
Create and activate a new environment:conda create -n file_organizer python=3.9
conda activate file_organizer


Install required package:pip install streamlit




Clone the Repository

Clone the project:git clone https://github.com/Fisehazion/ai_file_organizer.git
cd ai_file_organizer




Run the App Locally (Optional)

Launch the Streamlit app:streamlit run app.py


Your browser will open to http://localhost:8501.


Access the Deployed App

Visit https://ai-file-organizer-jwh2cxrumjcloxyou7vvqp.streamlit.app to use the app directly without local setup.



Using the App

Open the App

Access the deployed app at https://ai-file-organizer-jwh2cxrumjcloxyou7vvqp.streamlit.app or locally at http://localhost:8501.


Upload and Organize Zip File

Create a zip file of your folder (e.g., right-click TestFolder > Send to > Compressed (zipped) folder).
Upload the zip file (e.g., TestFolder.zip) via the file uploader.
Click Organize.
The app will:
Extract files from the zip.
Categorize files based on extensions:
Documents: .txt, .doc, .docx, .pdf, .xls, .xlsx, .ppt, .pptx
Images: .jpg, .jpeg, .png, .gif, .bmp, .tiff
Videos: .mp4, .avi, .mkv, .mov, .wmv
Others: All other file types


Skip duplicate files (based on content hash).
Rename files to avoid conflicts (e.g., file.txt → file_1.txt).
Display a progress bar and file processing status.




Download Organized Files

After organization, click Download Organized Files to get organized_files.zip.
Unzip the file to see folders (Documents/, Images/, Videos/, Others/) with categorized files (e.g., Documents/#ኮርስ የዮሐንስ ወንጌል አን�5ምታ.pdf).


View Results

Check the Streamlit interface for success messages and lists of moved or skipped files.
Verify the organized structure in the downloaded zip.



Configuration

Edit config.py to tweak settings:
LOG_LEVEL: Adjust logging verbosity (e.g., logging.INFO).
MAX_FILES_TO_PROCESS: Limit the number of files processed (default: 500).



Troubleshooting

Invalid Zip File: Ensure the uploaded file is a valid .zip. Try re-zipping the folder.
Unorganized Zip Output: Verify the downloaded organized_files.zip contains only Documents/, Images/, Videos/, Others/ folders. If not, check Streamlit Cloud logs.
Slow Performance: Reduce MAX_FILES_TO_PROCESS in config.py.
Dependencies Issue: Reinstall Streamlit in the Conda environment:pip install streamlit



Notes

Security: Do not share sensitive files in the zip, as the app processes them on Streamlit Cloud.
Limits: The app processes up to 500 files by default (configurable in config.py).
Future Updates: Check config.py for new features or settings.
Deployment: The app is hosted at https://ai-file-organizer-jwh2cxrumjcloxyou7vvqp.streamlit.app. For local use, follow setup instructions.
