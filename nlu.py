from dateparser.search import search_dates
from datetime import datetime
import re

# Filler phrases to remove from task text
FILLER_PHRASES = [
    "to", "remind me to", "i need to", "i have to", "please", "remind me",
    "add", "task", "remind", "on", "me"
]

# Indian-friendly date keywords
DATE_KEYWORDS = [
    "today", "tomorrow", "day after tomorrow",
    "sunday","monday","tuesday","wednesday","thursday","friday","saturday",
    "january","february","march","april","may","june",
    "july","august","september","october","november","december",
    "morning","afternoon","evening","night","next", "in"
]

# Regex to detect day numbers (1st, 2nd, 3rd, 4th...)
DAY_NUMBER_PATTERN = r"\b\d{1,2}(st|nd|rd|th)?\b"


def extract_task_and_date(text):
    """
    Extract the task description and due date from a natural language string.
    Returns: (task_text: str, due_date: datetime.date)
    """
    text_lower = text.lower()

    # Use search_dates to find date phrase
    results = search_dates(
        text_lower,
        settings={
            "PREFER_DATES_FROM": "future",  # always prefer future dates
            "DATE_ORDER": "DMY",            # Indian date format
            "RELATIVE_BASE": datetime.now(), # must be datetime, not date
            "RETURN_AS_TIMEZONE_AWARE": False,
            "SKIP_TOKENS": FILLER_PHRASES
        }
    )

    if results:
        date_phrase, parsed_datetime = results[0]
        due_date = parsed_datetime.date()
        # Remove exact date phrase from task text
        pattern = re.escape(date_phrase.lower())
        task_text = re.sub(pattern, "", text_lower)
    else:
        # fallback to today if no date is detected
        due_date = datetime.now().date()
        task_text = text_lower

    # Remove numeric day references (4th, 22nd, etc.)
    task_text = re.sub(DAY_NUMBER_PATTERN, "", task_text)

    # Remove month names and other date keywords
    for k in DATE_KEYWORDS:
        task_text = re.sub(r"\b" + re.escape(k) + r"\b", "", task_text)

    # Remove filler phrases
    for phrase in FILLER_PHRASES:
        task_text = task_text.replace(phrase, "")

    # Collapse multiple spaces
    task_text = re.sub(r"\s+", " ", task_text).strip()

    return task_text, due_date
