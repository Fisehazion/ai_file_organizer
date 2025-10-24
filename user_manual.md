User Manual for AI File Organizer App
Overview
The AI File Organizer App helps you organize files in a local folder or Google Drive folder using AI-powered categorization and duplicate detection. Built with Streamlit for an easy web interface, it supports seamless Google Drive integration via folder links.
Prerequisites

Anaconda: Installed for managing the app environment.
Google Drive Access: A Google account with a shared folder link for Drive organization.
Browser: Chrome, Firefox, or any modern browser.
Internet: Required for Google Drive and initial setup.

Setup Instructions
1. Install Dependencies

Open Anaconda Prompt.
Create and activate a new environment:conda create -n file_organizer python=3.11
conda activate file_organizer


Install required packages:conda install streamlit pandas scikit-learn
pip install transformers pydrive2 google-api-python-client google-auth-oauthlib google-auth-httplib2



2. Google Drive Setup

Go to Google Cloud Console.
Create a project and enable the Google Drive API.
Under "Credentials," create an OAuth 2.0 Client ID for a "Web application."
Add Authorized JavaScript origins: http://localhost:8501 (and your deployed URL, if applicable).
Add Authorized redirect URIs: http://localhost:8501/ (and deployed URL, if applicable).


Download the client_secrets.json, rename it to credentials.json, and place it in the ai_file_organizer/ folder.
Ensure your Google Drive folder is shared (set to "Anyone with the link" for testing).

3. Run the App

Navigate to the project folder:cd path/to/ai_file_organizer


Launch the Streamlit app:streamlit run app.py


Your browser will open to http://localhost:8501.

Using the App
1. Open the App

Access the app via the browser at http://localhost:8501.

2. Choose Organization Mode

Select Local Folder or Google Drive using the radio buttons.

3. Organize Local Folder

Enter the full path to a local folder (e.g., C:\Users\YourName\Documents\MyFolder).
Click Organize.
The app will:
Read file contents (text files supported).
Use AI to categorize files into subfolders (e.g., Documents, Images).
Move files to respective subfolders.



4. Organize Google Drive Folder

Paste the Google Drive folder link (e.g., https://drive.google.com/drive/folders/ABC123).
Click Organize.
On first run, authenticate via the browser (follow the OAuth prompts).
The app will:
Extract the folder ID from the link.
Categorize files based on names/extensions (e.g., Documents for .txt, .pdf).
Create subfolders in Drive (e.g., Documents, Images).
Move files to appropriate subfolders.



5. View Results

Check the Streamlit interface for success/error messages.
Verify organized files in the local folder or Google Drive.

Configuration

Edit config.py to tweak settings:
AI_MODEL_NAME: Change the AI model (e.g., bert-base-uncased for a different model).
DUPLICATE_THRESHOLD: Adjust duplicate detection sensitivity (0-1).
MAX_FILES_TO_PROCESS: Limit the number of files processed.



Troubleshooting

Authentication Error: Ensure credentials.json is in the project folder and OAuth URIs are correct.
Invalid Folder Link: Verify the Google Drive folder is shared and the link is correct.
Slow Performance: Reduce MAX_FILES_TO_PROCESS in config.py.
Dependencies Issue: Reinstall packages in the Conda environment.

Notes

Security: Do not share credentials.json publicly. Add it to .gitignore.
Limits: The app processes up to 100 files by default (configurable).
Future Updates: Check config.py for new features like email notifications.
