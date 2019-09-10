import os
import warnings

from pathlib import Path

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def upload(client_secrets_path, files_paths, folder_id="root",
           credentials_path=None, save_credentials=False):
    """Uploads specified files to Google Drive."""
    client_secrets_path = Path(client_secrets_path).resolve()

    if not os.path.exists(client_secrets_path):
        raise FileNotFoundError(
            "Calling 'upload' function requires 'client_secrets.json' "
            "file existing."
        )

    GoogleAuth.DEFAULT_SETTINGS["client_config_file"] = str(client_secrets_path)

    gauth = GoogleAuth()

    if credentials_path is not None:
        credentials_path = Path(credentials_path).resolve()
        # Try to load saved client credentials.
        gauth.LoadCredentialsFile(str(credentials_path))
    elif save_credentials:
        save_credentials = False
        warnings.warn(
            "Credentials will not be saved due to not providing the "
            "`credentials_path`.",
            UserWarning
        )

    if gauth.credentials is None:
        # Authenticate if they're not there.
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired.
        gauth.Refresh()
    else:
        # Initialize the saved creds.
        gauth.Authorize()
    if save_credentials:
        # Save the current credentials to a file.
        gauth.SaveCredentialsFile(str(credentials_path))

    drive = GoogleDrive(gauth)

    for file_path in files_paths:
        file_path = Path(file_path).resolve()
        file = drive.CreateFile({
            "title": os.path.split(file_path)[-1],
            "parents": [{
                "id": folder_id,
                "kind": "drive#file"
            }]
        })
        file.SetContentFile(str(file_path))
        file.Upload()
        print(
            "The file: {} of mimeType: {} was succesfully uploaded to "
            "the folder of id: {}."
            .format(file["title"], file["mimeType"], folder_id)
        )
