# jinja_renderer.py
from jinja2 import Environment, FileSystemLoader
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, 'state_prompts')

env = Environment(loader=FileSystemLoader(PROMPTS_DIR))

def render_prompt(state, context):
    """
    Render the Jinja template for the current state with context.

    Args:
        state (str): current conversation state (matches .jinja filename)
        context (dict): dictionary of variables for template rendering

    Returns:
        str: rendered prompt string
    """
    template_file = f"{state}.jinja"
    template = env.get_template(template_file)
    return template.render(**context)
