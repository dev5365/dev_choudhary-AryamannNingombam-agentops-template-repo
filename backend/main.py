import json
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel
from datetime import datetime
from log_to_sheet import log_conversation_to_sheet

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, 'state_prompts')
KB_PATH = os.path.join(BASE_DIR, 'knowledge_base')

env = Environment(loader=FileSystemLoader(PROMPTS_DIR))


# --- Load Knowledge Base ---
def load_city_kb(city):
    path = os.path.join(KB_PATH, f"{city.lower()}.json")
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# --- State Transition Logic ---
def get_next_state(current_state, user_input, context):
    user_input_lower = user_input.strip().lower()

    if current_state == "choose_action":
        if "faq" in user_input_lower or "question" in user_input_lower:
            return "faq_handler"
        elif "book" in user_input_lower or "new booking" in user_input_lower:
            return "collect_city"
        elif "update" in user_input_lower:
            return "update_booking"
        elif "cancel" in user_input_lower:
            return "cancel_booking"
        else:
            return "choose_action"

    elif current_state == "collect_city":
        if user_input_lower in ["delhi", "bengaluru", "bangalore"]:
            context['booking']['city'] = user_input_lower
            return "collect_date"
        else:
            return "collect_city"

    elif current_state == "collect_date":
        context['booking']['date'] = user_input
        return "collect_guests"

    elif current_state == "collect_guests":
        if user_input.isdigit() and int(user_input) > 0:
            context['booking']['guests'] = int(user_input)
            return "confirm_booking"
        else:
            return "collect_guests"

    elif current_state == "confirm_booking":
        if "yes" in user_input_lower:
            context['booking']['confirmed'] = True
            return "end_conversation"
        elif "no" in user_input_lower:
            return "collect_city"
        else:
            return "confirm_booking"

    elif current_state == "faq_handler":
        return "choose_action"

    elif current_state in ["update_booking", "cancel_booking"]:
        return "end_conversation"

    elif current_state == "end_conversation":
        return "choose_action"

    else:
        return "choose_action"


# --- Jinja Prompt Rendering ---
def render_prompt(state, context):
    try:
        template = env.get_template(f"{state}.jinja")
    except Exception as e:
        return f"Error loading template for state {state}: {str(e)}"
    return template.render(**context)


# --- Main Conversation Endpoint ---
@app.post("/conversation")
async def conversation(request: Request):
    data = await request.json()
    current_state = data.get('current_state', 'choose_action')
    user_input = data.get('user_input', '')
    context = data.get('context', {})

    if 'booking' not in context:
        context['booking'] = {}

    if 'knowledge_base' not in context:
        city = context['booking'].get('city', 'delhi')
        kb = load_city_kb(city)
        context['knowledge_base'] = kb if kb else {"faqs": []}

    next_state = get_next_state(current_state, user_input, context)

    prompt_text = render_prompt(next_state, {
        "state": next_state,
        "booking": context.get('booking', {}),
        "user_input": user_input,
        "knowledge_base": context.get('knowledge_base', {})
    })

    return JSONResponse({
        "next_state": next_state,
        "reply": prompt_text,
        "context": context
    })


# --- Post-Call Conversation Logging Endpoint ---
class ConversationLog(BaseModel):
    modality: str  # "Call" or "Chatbot"
    call_time: str  # "YYYY-MM-DD HH:MM:SS"
    phone_number: str
    call_outcome: str
    room_name: str = "NA"
    booking_date: str = "NA"
    booking_time: str = "NA"
    number_of_guests: str = "NA"
    customer_name: str = "NA"
    call_summary: str


@app.post("/conversation-end")
async def end_conversation(log: ConversationLog):
    success = log_conversation_to_sheet(log.dict())
    return {"status": "logged" if success else "error"}
