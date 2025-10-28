"""
Persistence layer for gradebook data.
Reads/writes a JSON file.
"""

import json
import os
import logging
from json import JSONDecodeError
from typing import Dict, Any

# Set up logging
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Default data file
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
DEFAULT_PATH = os.path.join(DATA_DIR, "gradebook.json")


def load_data(path: str = DEFAULT_PATH) -> Dict[str, Any]:
    """
    Load gradebook data from disk.
    Returns a dict with keys: students, courses, enrollments.
    If file doesn't exist -> start empty.
    If JSON is invalid -> log error and raise.
    """
    if not os.path.exists(path):
        logging.info("Data file not found. Starting with empty dataset.")
        return {"students": [], "courses": [], "enrollments": []}

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Basic shape check
        data.setdefault("students", [])
        data.setdefault("courses", [])
        data.setdefault("enrollments", [])

        logging.info("Loaded data successfully.")
        return data

    except FileNotFoundError:
        logging.info("Data file not found (race). Starting empty.")
        return {"students": [], "courses": [], "enrollments": []}

    except JSONDecodeError as e:
        logging.error(f"Could not parse JSON: {e}")
        raise ValueError(
            "Your data file is corrupted or not valid JSON. "
            "Please fix or delete data/gradebook.json."
        )

    except Exception as e:
        logging.error(f"Unexpected error loading data: {e}")
        raise


def save_data(data: Dict[str, Any], path: str = DEFAULT_PATH) -> None:
    """
    Save gradebook data to disk as JSON.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info("Saved data successfully.")
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        raise