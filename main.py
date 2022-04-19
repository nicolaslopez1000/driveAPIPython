import os
from Google import Create_Service
from pprint import pprint
from datetime import datetime
import io
import os
from googleapiclient.http import MediaIoBaseDownload

CLIENT_SECRET_FILE = 'client-secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'


class GoogleDriveService:
    def __init__(self):
        self.service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION)

    def get_shared_folders(self):
        response = self.service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and sharedWithMe=True",
            spaces='drive',
        ).execute()
        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            pprint(file)
        return response.get('files', [])

    def get_folders_inside_folder(self, folder_id):
        response = self.service.files().list(
            q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
            spaces='drive',
        ).execute()
        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            pprint(file)

        return response.get('files', [])

    def get_files_inside_folder(self, folder_id):
        response = self.service.files().list(
            q=f"'{folder_id}' in parents and mimeType!='application/vnd.google-apps.folder'",
            spaces='drive',
        ).execute()
        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            pprint(file)

        return response.get('files', [])

    def move_file_to_folder(self, file_id, folder_destination_id):
        # Retrieve the existing parents to remove
        file = self.service.files().get(fileId=file_id,
                                        fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = self.service.files().update(fileId=file_id,
                                           addParents=folder_destination_id,
                                           removeParents=previous_parents,
                                           fields='id, parents').execute()
        return file

    def dowload_file(self, file_id, file_name):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        d = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        file_name, file_extension = os.path.splitext(file_name)
        file_name = f"{file_name}-{d}.{file_extension}"

        with open(os.path.join('downloads', file_name), 'wb') as f:
            f.write(fh.read())
