# import os
# from dataclasses import dataclass
# from dotenv import load_dotenv

# load_dotenv()  # This loads variables from .env

# # Get API key from environment variable
# API_KEY = os.getenv("WEATHER_API_KEY")
# SELECTED_FEATURES = ["feature1", "feature2"]  # Replace with your actual feature names

# @dataclass
# class Config:
#     """Application configuration with secure defaults."""
#     api_key: str            # Required credential to authenticate with the weather API
#     database_path: str      # Path to the SQLite database file for storing weather data
#     log_level: str = "INFO" # Controls logging verbosity: DEBUG, INFO, WARNING, etc.
#     max_retries: int = 3    # Number of retry attempts for failed API requests
#     request_timeout: int = 10 # Max wait time (in seconds) before an API call is aborted
    
#     @classmethod
#     def from_environment(cls):
#         """Instantiate Config using environment variables."""
#         api_key = os.getenv('WEATHER_API_KEY')
#         if not api_key:
#             raise ValueError("WEATHER_API_KEY environment variable required")
#         return cls(
#             api_key=api_key,
#             database_path=os.getenv('DATABASE_PATH', 'weather_data.db'),
#             log_level=os.getenv('LOG_LEVEL', 'INFO'),
#             max_retries=int(os.getenv('MAX_RETRIES', '3')),
#             request_timeout=int(os.getenv('REQUEST_TIMEOUT', '10'))
