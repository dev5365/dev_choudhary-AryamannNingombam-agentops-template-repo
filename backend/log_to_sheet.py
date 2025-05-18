import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

SHEET_NAME = "BBQ Conversations"

def log_conversation_to_sheet(data: dict):
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1

        row = [
            data.get("modality", "Chatbot"),
            data.get("call_time", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            data.get("phone_number", "NA"),
            data.get("call_outcome", "MISC"),
            data.get("room_name", "NA"),
            data.get("booking_date", "NA"),
            data.get("booking_time", "NA"),
            data.get("number_of_guests", "NA"),
            data.get("customer_name", "NA"),
            data.get("call_summary", "No summary available.")
        ]

        sheet.append_row(row)
        print("Conversation logged successfully.")
        return True
    except Exception as e:
        print(f"Failed to log conversation: {e}")
        return False
