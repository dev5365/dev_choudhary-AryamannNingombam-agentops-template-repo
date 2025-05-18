#  Barbeque Nation AI Agent – Retell AI + FastAPI

This project is a voice/chatbot solution for Barbeque Nation (Delhi & Bengaluru outlets) using Retell AI, built with FastAPI, Jinja templates, and a Google Sheets integration for post-conversation logging.

##  Features

- Voice/Chatbot agent using Retell AI prompts  
- Handles:  
  - FAQ responses  
  - New bookings  
  - Booking updates/cancellations  
- Uses Jinja2 for dynamic conversation state templates  
- Integrates a structured knowledge base per city  
- Logs each conversation post-call/chatbot to Google Sheets  
- Token-limited (800 tokens max) per response – information chunking handled  




##  Setup Instructions

1. Clone the repo
    ```bash
    git clone <repo-url>
    cd project/
    ```
2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
3. Add your Google Sheets credentials  
    - Create a Google Service Account via Google Cloud Console  
    - Share your target Google Sheet with the service account email  
    - Save the `credentials.json` file in the root directory  
4. Run the server  
    ```bash
    uvicorn main:app --reload --port 5000
    ```

## API Endpoints

### 1. `/conversation` – Handles conversation turns

**POST /conversation**  
Request body:
```json
{
  "current_state": "choose_action",
  "user_input": "I want to book a table",
  "context": {}
}


Response:

{
  "next_state": "collect_city",
  "reply": "Great! Which city would you like to book in – Delhi or Bengaluru?",
  "context": { ... }
}

2. /conversation-end – Logs call/chat summary to Google Sheets
POST /conversation-end
Request body:

{
  "modality": "Call",
  "call_time": "2025-01-03 12:50:07",
  "phone_number": "9833620578",
  "call_outcome": "ROOM_AVAILABILITY",
  "room_name": "Executive Room",
  "booking_date": "2025-01-03",
  "booking_time": "15:30",
  "number_of_guests": "2",
  "customer_name": "Aryamann",
  "call_summary": "User asked for room availability..."
}


## Dependencies

| Package     | Purpose                                        |
| ----------- | ---------------------------------------------- |
| fastapi     | Core backend framework                         |
| uvicorn     | ASGI server to run FastAPI                     |
| jinja2      | Template engine for dynamic prompts            |
| gspread     | Integration with Google Sheets                 |
| google-auth | Authenticate Google API using service accounts |
| pydantic    | Type validation (used internally by FastAPI)   |
| httpx       | Optional, for async HTTP requests              |


## Installation command

pip install -r requirements.txt