from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"

# App metadata
APP_TITLE = "BT3017 Visual Learning Studio"
APP_ICON = "🧠"
APP_LAYOUT = "wide"

# Topics
TOPICS = [
    "PCA",
    "Audio Features",
    "Graph Learning",
]

TOPIC_PAGE_MAP = {
    "PCA": "pages/2_PCA.py",
    "Audio Features": "pages/3_Audio_Features.py",
    "Graph Learning": "pages/4_Graph_Learning.py",
}

# Quiz settings
QUIZ_QUESTIONS_PER_TOPIC = 3

# Theme / styling
PRIMARY_COLOR = "#4F7DF3"
BACKGROUND_COLOR = "#F7FAFF"
CARD_BACKGROUND = "#FFFFFF"
TEXT_COLOR = "#16325C"

# Files
CSS_FILE = ASSETS_DIR / "styles.css"
QUIZ_BANK_FILE = DATA_DIR / "quiz_bank.json"
TOPIC_CONTENT_FILE = DATA_DIR / "topic_content.json"