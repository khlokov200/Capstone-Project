| Field                   | Your Entry          |
| ----------------------- | ------------------- |
| Name                    | Tobi O.             |
| GitHub Username         | khlokov200          |
| Preferred Feature Track | Smart               |
| Team Interest           | Yes – Project Owner |


Project Structure:
WeatherDashboard/
├── main.py            # GUI + main logic
├── config.py          # API key config
├── data/
│   └── weather_log.csv  # saved weather data
├── docs/
│   └── README.md      # project description
├── tests/
│   └── test_main.py   # sample test
└── .gitignore


Week 11 Reflection

Section 1: 

Key Takeaways:
This Capstone project will require early planning and thoughtful architecture.

I will Maintain a clean folder structure and version control.

API integration should be started early due to setup/limits.

Testing and documentation will be important in the final weeks.

Concept Connections:

Strongest: API integration, Tkinter GUI design, file I/O, GitHub workflow.

What Needs practice: Robust error handling, modularizing large scripts, UI polish.

Early Challenges:

Getting and safely storing API keys (.env setup).

Organizing feature modules inside /features/.

Understanding how to sketch app architecture clearly.

Support Strategies:

I will book office hours for API troubleshooting.

Referencing prior class demos and peer GitHub repos.

Using Slack to get quick feedback on design choices.


Section 2: Feature Selection Rationale
#	Feature Name	Difficulty (1–3)	Why You Chose It / Learning Goal
1	Weather Forecast	2	Learn to parse JSON data from API & update GUI dynamically.
2	Journal Logger	2	Build user input features and store structured text data.
3	Charting Trends	3	Practice with matplotlib and displaying dynamic plots.
–	Smart Alerts (Enhancement)	–	Try adding logic to notify users of severe weather conditions.

 Section 3: High-Level Architecture Sketch
Outline:

/main.py – Launches app and controls flow

/config.py – API key and config settings

/features/

forecast.py

journal.py

charting.py

/data/ – Stores logs, local caches

/docs/ – Reports, reflections

/tests/ – Unit tests

Data Model Plan
File/Table Name	Format	Example Row
weather_history.txt	txt	2025-06-09,New Brunswick,78,Sunny
journal_entries.json	json	{"date": "2025-06-09", "mood": "Calm", "notes": "Nice day"}
forecast_cache.json	json	{"city": "Chicago", "forecast": [...]}

ection 5: Personal Project Timeline (Weeks 12–17)
Week	Monday	Tuesday	Wednesday	Thursday	Key Milestone
12	API setup	Error handling	Tkinter shell	Buffer day	Basic working app
13	Feature 1	–	–	Integrate	Forecast module complete
14	Feature 2	–	Review & test	Finish	Journal module complete
15	Feature 3	Polish UI	Error passing	Refactor	Charting module complete
16	Enhancement	Docs	Tests	Packaging	App ready for showcase


Section 6: Risk Assessment
Risk	Likelihood	Impact	Mitigation Plan
API Rate Limit	Medium	Medium	Cache results; add retries & delay logic
GUI Bugs	Medium	High	Test early; modularize UI for easier debug
Feature Overload	High	High	Prioritize core features; enhancements optional


Section 7: Support Requests
Help setting up .env securely for API key use.

Guidance on integrating multiple features into one Tkinter window.

Debugging UI updates with matplotlib charts.