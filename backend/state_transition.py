# state_transition.py

def get_next_state(current_state, user_input, context):
    """
    Determine the next state in the conversation based on
    current state, user input, and context (like booking info).

    Args:
        current_state (str): Current active state.
        user_input (str): User's latest message.
        context (dict): Context including booking info, flags, etc.

    Returns:
        str: Next state to transition to.
    """

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
            return "choose_action"  # Ask again

    elif current_state == "collect_city":
        if user_input_lower in ["delhi", "bengaluru", "bangalore"]:
            context['booking']['city'] = user_input_lower
            return "collect_date"
        else:
            return "collect_city"  # Invalid city, ask again

    elif current_state == "collect_date":
        # You could add date validation here
        context['booking']['date'] = user_input
        return "collect_guests"

    elif current_state == "collect_guests":
        # Basic guest count validation
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
            return "collect_city"  # Start over
        else:
            return "confirm_booking"

    elif current_state == "faq_handler":
        # After answering FAQ, go back to choose action
        return "choose_action"

    elif current_state in ["update_booking", "cancel_booking"]:
        # After update/cancel, end conversation
        return "end_conversation"

    elif current_state == "end_conversation":
        # Conversation ended
        return "choose_action"

    else:
        return "choose_action"  # Default fallback
