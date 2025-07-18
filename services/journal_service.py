"""
Journal Service - Handles weather journal functionality
"""
import os
import csv
from datetime import datetime


class JournalService:
    """Service for weather journal entries"""
    
    def __init__(self, log_file="data/journal_log.csv"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def save_entry(self, text, mood):
        """Save a journal entry"""
        file_exists = os.path.isfile(self.log_file)
        with open(self.log_file, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["DateTime", "Entry", "Mood"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                text, mood
            ])
