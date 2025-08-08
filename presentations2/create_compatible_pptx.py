#!/usr/bin/env python3
"""
Create a PowerPoint presentation using the aspose.slides library (which is more compatible)
You'll need to install it first with: pip install aspose-slides
"""
import os
import sys
from pathlib import Path

try:
    import aspose.slides as slides
except ImportError:
    print("Installing aspose-slides package...")
    os.system("pip install aspose-slides")
    try:
        import aspose.slides as slides
    except ImportError:
        print("Failed to install aspose-slides. Please install it manually: pip install aspose-slides")
        sys.exit(1)

# Config
TITLE = "The MeteoMetrics Weather Station"
SUBTITLE = "A professional-grade weather dashboard by Tobi Odika"
SCREEN_DIR = Path("../screens")  # Path relative to the presentations2 folder
OUTPUT = "MeteoMetrics_Compatible_Presentation.pptx"

def main():
    """Create a presentation using the Aspose library for better compatibility"""
    try:
        # Create presentation
        with slides.Presentation() as prs:
            # Add title slide
            title_slide = prs.slides[0]
            title_slide.shapes.add_auto_shape(
                slides.ShapeType.RECTANGLE, 100, 100, 600, 50
            ).text_frame.text = TITLE
            title_slide.shapes.add_auto_shape(
                slides.ShapeType.RECTANGLE, 100, 200, 600, 50
            ).text_frame.text = SUBTITLE
            
            # Add bullet slides
            # Executive Summary
            add_bullet_slide(prs, "Executive Summary", [
                "15+ functional tabs with advanced weather tools",
                "Real-time data, analytics, and machine learning",
                "6+ chart types, modern UI, and zero critical bugs"
            ])
            
            # Key Features
            add_bullet_slide(prs, "Key Features", [
                "Real-time weather & multi-city comparison",
                "5-day forecasting & historical trends",
                "Live radar animations & severe alerts",
                "Health & wellness monitoring",
                "AI-based activity & travel suggestions"
            ])
            
            # Technical Architecture
            add_bullet_slide(prs, "Technical Architecture", [
                "MVC pattern with modular components",
                "Tkinter frontend, matplotlib charts",
                "OpenWeatherMap API integration",
                "Machine learning for predictions"
            ])
            
            # UI Highlights
            add_bullet_slide(prs, "User Interface Highlights", [
                "Modern split-panel layout",
                "Professional styling & color schemes",
                "Interactive charts with multiple types",
                "Quick Actions dashboard"
            ])
            
            # Add image slides
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
            
            for img_path, caption in zip(images, captions):
                add_image_slide(prs, img_path, caption)
            
            # Testing & Quality Assurance
            add_bullet_slide(prs, "Testing & Quality Assurance", [
                "All UI components tested",
                "Chart generation validated",
                "API integration stable",
                "No critical bugs"
            ])
            
            # Future Enhancements
            add_bullet_slide(prs, "Future Enhancements", [
                "Mobile responsive design",
                "SQL database integration",
                "Enhanced ML models",
                "IoT weather station integration"
            ])
            
            # Save the presentation
            prs.save(OUTPUT, slides.export.SaveFormat.PPTX)
            
        print(f"Compatible presentation created: {OUTPUT}")
        print("Try opening this version if the original doesn't work.")
            
    except Exception as e:
        print(f"Error creating presentation: {e}")

def add_bullet_slide(prs, title, bullets):
    """Add a slide with bullet points"""
    slide = prs.slides.add_empty_slide(prs.slides[0].layout_slide)
    
    # Add title
    title_shape = slide.shapes.add_auto_shape(
        slides.ShapeType.RECTANGLE, 50, 50, 600, 50
    )
    title_shape.text_frame.text = title
    
    # Add bullet points
    bullet_shape = slide.shapes.add_auto_shape(
        slides.ShapeType.RECTANGLE, 50, 120, 600, 300
    )
    tf = bullet_shape.text_frame
    
    for i, bullet in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.paragraphs.add_paragraph()
        p.text = bullet
        p.paragraph_format.bullet.type = slides.BulletType.SYMBOL
        p.paragraph_format.bullet.char = "•"

def add_image_slide(prs, img_path, caption):
    """Add a slide with an image"""
    slide = prs.slides.add_empty_slide(prs.slides[0].layout_slide)
    
    # Add caption as title
    title_shape = slide.shapes.add_auto_shape(
        slides.ShapeType.RECTANGLE, 50, 50, 600, 50
    )
    title_shape.text_frame.text = caption
    
    # Add image
    try:
        slide.shapes.add_picture(str(img_path), 100, 100, 500, 400)
    except Exception as e:
        print(f"Error adding image {img_path}: {e}")
        # Add placeholder text instead
        err_shape = slide.shapes.add_auto_shape(
            slides.ShapeType.RECTANGLE, 100, 100, 500, 400
        )
        err_shape.text_frame.text = f"[Image: {img_path.name}]"

if __name__ == "__main__":
    main()
