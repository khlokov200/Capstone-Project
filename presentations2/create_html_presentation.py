#!/usr/bin/env python3
"""
Script to create an HTML presentation from the same content.
This will be viewable in any web browser.
"""
import os
from pathlib import Path
import shutil
import base64

# Config
TITLE = "The MeteoMetrics Weather Station"
SUBTITLE = "A professional-grade weather dashboard by Tobi Odika"
SCREEN_DIR = Path("../screens")  # Path relative to the presentations2 folder
OUTPUT = "MeteoMetrics_Presentation.html"

def create_html_presentation():
    """Create an HTML presentation that works in any browser."""
    html_parts = []
    html_parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        .slide {{
            width: 100%;
            max-width: 1000px;
            margin: 20px auto;
            background-color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
            box-sizing: border-box;
        }}
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        h2 {{
            color: #3498db;
            margin-bottom: 20px;
        }}
        ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        li {{
            margin-bottom: 10px;
            position: relative;
            padding-left: 25px;
        }}
        li:before {{
            content: "•";
            color: #3498db;
            font-size: 20px;
            position: absolute;
            left: 0;
        }}
        .notes {{
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 4px solid #3498db;
            font-style: italic;
        }}
        .image-container {{
            text-align: center;
            margin: 20px auto;
        }}
        .image-container img {{
            max-width: 100%;
            max-height: 500px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .caption {{
            margin-top: 10px;
            font-weight: bold;
        }}
        .title-slide {{
            text-align: center;
            padding: 50px 30px;
        }}
        .title-slide h1 {{
            font-size: 36px;
            margin-bottom: 20px;
        }}
        .title-slide h2 {{
            font-size: 24px;
            color: #7f8c8d;
        }}
        #slide-controls {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: rgba(44, 62, 80, 0.8);
            padding: 10px;
            border-radius: 5px;
            color: white;
        }}
        #slide-controls button {{
            background: none;
            border: none;
            color: white;
            font-size: 16px;
            cursor: pointer;
            margin: 0 5px;
        }}
    </style>
</head>
<body>
""")
    
    # Title slide
    html_parts.append(f"""
    <div id="slide1" class="slide title-slide">
        <h1>{TITLE}</h1>
        <h2>{SUBTITLE}</h2>
        <div class="notes">
            <p>Introduce yourself and the project purpose. Briefly mention that it's the final capstone project, combining real-time data, analytics, and machine learning.</p>
        </div>
    </div>
    """)
    
    # Executive Summary slide
    html_parts.append("""
    <div id="slide2" class="slide">
        <h1>Executive Summary</h1>
        <ul>
            <li>15+ functional tabs with advanced weather tools</li>
            <li>Real-time data, analytics, and machine learning</li>
            <li>6+ chart types, modern UI, and zero critical bugs</li>
        </ul>
        <div class="notes">
            <p>Highlight evolution from simple tool to full meteorological platform. Mention project status as completed with full documentation.</p>
        </div>
    </div>
    """)
    
    # Key Features slide
    html_parts.append("""
    <div id="slide3" class="slide">
        <h1>Key Features</h1>
        <ul>
            <li>Real-time weather & multi-city comparison</li>
            <li>5-day forecasting & historical trends</li>
            <li>Live radar animations & severe alerts</li>
            <li>Health & wellness monitoring</li>
            <li>AI-based activity & travel suggestions</li>
        </ul>
        <div class="notes">
            <p>Briefly explain each feature category, focusing on benefits to the user.</p>
        </div>
    </div>
    """)
    
    # Technical Architecture slide
    html_parts.append("""
    <div id="slide4" class="slide">
        <h1>Technical Architecture</h1>
        <ul>
            <li>MVC pattern with modular components</li>
            <li>Tkinter frontend, matplotlib charts</li>
            <li>OpenWeatherMap API integration</li>
            <li>Machine learning for predictions</li>
        </ul>
        <div class="notes">
            <p>Describe how the architecture supports maintainability and scalability.</p>
        </div>
    </div>
    """)
    
    # UI Highlights slide
    html_parts.append("""
    <div id="slide5" class="slide">
        <h1>User Interface Highlights</h1>
        <ul>
            <li>Modern split-panel layout</li>
            <li>Professional styling & color schemes</li>
            <li>Interactive charts with multiple types</li>
            <li>Quick Actions dashboard</li>
        </ul>
        <div class="notes">
            <p>Emphasize how the UI design enhances usability and engagement.</p>
        </div>
    </div>
    """)
    
    # Screenshot slides
    images = sorted(SCREEN_DIR.glob("*.png"))
    
    captions = [
        "Quick Actions Dashboard",
        "Current Weather View",
        "Forecast Tab",
        "Live Weather Radar",
        "Analytics & Trends",
        "City Comparison",
        "Health & Wellness",
        "Activity Suggestions",
        "Weather Poetry",
        "Weather History",
        "Settings",
        "Extra Feature"
    ]
    
    notes_list = [
        "Show how Quick Actions centralizes major features.",
        "Highlight detailed metrics & real-time updates.",
        "Discuss how forecast aids planning.",
        "Demonstrate radar & live animations.",
        "Show correlation & trend analysis.",
        "Explain cross-city comparisons.",
        "Display health-related weather info.",
        "Point out smart suggestions feature.",
        "Mention creative engagement via poetry.",
        "Show historical weather logging.",
        "Demonstrate customization options.",
        "Highlight additional tools."
    ]
    
    # Create image slides
    slide_number = 6
    for img_path, caption, note in zip(images, captions, notes_list):
        # Copy the image to a local directory
        img_name = img_path.name
        
        # Encode the image as base64 to embed in HTML
        with open(img_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
            
        html_parts.append(f"""
        <div id="slide{slide_number}" class="slide">
            <h1>{caption}</h1>
            <div class="image-container">
                <img src="data:image/png;base64,{img_data}" alt="{caption}">
            </div>
            <div class="notes">
                <p>{note}</p>
            </div>
        </div>
        """)
        slide_number += 1
    
    # Testing & Quality Assurance slide
    html_parts.append("""
    <div id="slide18" class="slide">
        <h1>Testing & Quality Assurance</h1>
        <ul>
            <li>All UI components tested</li>
            <li>Chart generation validated</li>
            <li>API integration stable</li>
            <li>No critical bugs</li>
        </ul>
        <div class="notes">
            <p>Explain how thorough testing ensures stability.</p>
        </div>
    </div>
    """)
    
    # Future Enhancements slide
    html_parts.append("""
    <div id="slide19" class="slide">
        <h1>Future Enhancements</h1>
        <ul>
            <li>Mobile responsive design</li>
            <li>SQL database integration</li>
            <li>Enhanced ML models</li>
            <li>IoT weather station integration</li>
        </ul>
        <div class="notes">
            <p>Conclude with forward-looking improvements.</p>
        </div>
    </div>
    """)
    
    # Add slide controls and JavaScript
    html_parts.append("""
    <div id="slide-controls">
        <button onclick="prevSlide()">◀ Previous</button>
        <span id="slide-counter">1 / 19</span>
        <button onclick="nextSlide()">Next ▶</button>
    </div>
    
    <script>
        var currentSlide = 1;
        var totalSlides = 19;
        
        // Hide all slides except the first one
        window.onload = function() {
            for (var i = 2; i <= totalSlides; i++) {
                document.getElementById('slide' + i).style.display = 'none';
            }
        };
        
        function showSlide(n) {
            // Hide all slides
            for (var i = 1; i <= totalSlides; i++) {
                document.getElementById('slide' + i).style.display = 'none';
            }
            
            // Show the selected slide
            document.getElementById('slide' + n).style.display = 'block';
            
            // Update counter
            document.getElementById('slide-counter').textContent = n + ' / ' + totalSlides;
        }
        
        function nextSlide() {
            if (currentSlide < totalSlides) {
                currentSlide++;
                showSlide(currentSlide);
            }
        }
        
        function prevSlide() {
            if (currentSlide > 1) {
                currentSlide--;
                showSlide(currentSlide);
            }
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowRight' || e.key === ' ') {
                nextSlide();
            } else if (e.key === 'ArrowLeft') {
                prevSlide();
            }
        });
    </script>
</body>
</html>
    """)
    
    # Save the HTML presentation
    with open(OUTPUT, 'w') as f:
        f.write('\n'.join(html_parts))
    
    print(f"HTML presentation created: {OUTPUT}")
    print("This presentation can be viewed in any web browser.")

if __name__ == "__main__":
    create_html_presentation()
