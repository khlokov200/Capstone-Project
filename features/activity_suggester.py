# features/activity_suggester.py

import random

class ActivitySuggester:
    def __init__(self):
        self.activity_map = {
            "clear": ["Go for a walk", "Have a picnic", "Go for a bike ride"],
            "clouds": ["Visit a museum", "Go to a coffee shop", "Watch a movie"],
            "rain": ["Read a book", "Do indoor yoga", "Bake something warm"],
            "snow": ["Build a snowman", "Go sledding", "Drink hot chocolate"],
            "default": ["Relax at home", "Do some journaling", "Organize your room"]
        }
    
    def suggest(self, description):
        key = next((k for k in self.activity_map if k in description.lower()), "default")
        return random.choice(self.activity_map[key])