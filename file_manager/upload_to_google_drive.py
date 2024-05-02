from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from configuration.configuration import get_google_config_path
import os

# Set up Google Drive API credentials
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Path to your downloaded JSON file
CLIENT_SECRET_FILE = get_google_config_path()
creds = None
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
creds = flow.run_local_server(port=0)

# Build the Drive service
drive_service = build('drive', 'v3', credentials=creds)


def upload_excel_to_drive(file_path: str, folder_id: list[str]):
    # Get the filename from the file path
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': folder_id,
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }

    try:
        media = MediaFileUpload(
            file_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        file = drive_service.files().create(
            body=file_metadata, media_body=media, fields='id', supportsAllDrives=True
        ).execute()
        print('Successfully Uploaded to Google Drive the File ID:', file.get('id'))
    except Exception as e:
        print(f'Unable to upload file due to {e}')
