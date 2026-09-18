from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TARGET_URL = os.getenv("TARGET_URL", "https://demo.opencart.com")
MAX_STEPS = int(os.getenv("MAX_STEPS", 20))

ALLOWLIST = {
    "domains": ["demo.opencart.com"],
    "actions": ["click", "type", "navigate", "screenshot", "scroll"],
    "blocked_actions": ["payment", "delete", "submit_order"]
}

GEMINI_MODEL = "gemini-3.6-flash"