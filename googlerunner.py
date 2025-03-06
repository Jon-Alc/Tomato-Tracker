import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from private.tokens import GOOGLE_SHEET_ID, GOOGLE_CREDENTIALS_PATH, GOOGLE_SHEET_NAME

"""
references:
quickstart     - https://developers.google.com/sheets/api/quickstart/python
read and write - https://developers.google.com/sheets/api/guides/values#python
"""

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]



class GoogleRunner():
  


    def __init__(self):

        self.sheet = self._initialize()

    

    def _initialize(self):

        creds = None
        google_token_path = "private/googletoken.json"

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(google_token_path):
            creds = Credentials.from_authorized_user_file(google_token_path, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_CREDENTIALS_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)
        
            # Save the credentials for the next run
            with open(google_token_path, "w") as token:
                    token.write(creds.to_json())

        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        return sheet



    def update_sheet(self, sheet_range: str, sheet_values: list):
        
        update_range = f"{GOOGLE_SHEET_NAME}!{sheet_range}"
        body = {"values": sheet_values}

        try:
            
            result = (
                self.sheet.values()
                .update(
                    spreadsheetId=GOOGLE_SHEET_ID,
                    valueInputOption="USER_ENTERED",
                    range=update_range,
                    includeValuesInResponse=True, # don't delete cells in case of disaster
                    body=body,
                )
                .execute()
            )

            print(f"{result.get('updatedCells')} cells updated.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
        


    def get_last_entry_row_number(self):

        cell_range = f"{GOOGLE_SHEET_NAME}!B1"

        try:
            result = (
                self.sheet.values()
                .get(spreadsheetId=GOOGLE_SHEET_ID, range=cell_range)
                .execute()
            )
            values = result.get("values")

            if values:
                # values = [['3']], return only the number as an int
                return int(values[0][0])
            
            return None
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error



    def update_last_entry_row_number(self, last_row: str):

        update_range = f"{GOOGLE_SHEET_NAME}!B1"
        body = {"values": [[last_row]]}

        try:
            
            result = (
                self.sheet.values()
                .update(
                    spreadsheetId=GOOGLE_SHEET_ID,
                    valueInputOption="USER_ENTERED",
                    range=update_range,
                    body=body,
                )
                .execute()
            )

            print(f"Last row entry is at line {last_row}.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error