import os

from dotenv import load_dotenv

load_dotenv()


class EnvConfig:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    REQUEST_FILTERS_FILE = os.getenv("REQUEST_FILTERS_FILE")
