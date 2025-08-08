#!/usr/bin/env python3
"""
Script to convert a PPTX file to a different format for better compatibility.
"""
import sys
import subprocess
from pathlib import Path
import tempfile

def convert_pptx(input_pptx):
    """Convert a PowerPoint file to a more compatible format."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir = Path(tmpdir)
        
        # Export the PPTX file to a format that Keynote can easily read
        output_file = Path("MeteoMetrics_Presentation_Compatible.pptx")
        
        try:
            # Using LibreOffice if available (headless mode)
            print(f"Attempting to convert {input_pptx} to a more compatible format...")
            
            # Try to find soffice (LibreOffice command line)
            soffice_paths = [
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",
                "/usr/bin/soffice",
                "/usr/local/bin/soffice",
            ]
            
            soffice_path = None
            for path in soffice_paths:
                if Path(path).exists():
                    soffice_path = path
                    break
            
            if soffice_path:
                # Convert using LibreOffice
                cmd = [
                    soffice_path, 
                    "--headless", 
                    "--convert-to", 
                    "pptx",
                    "--outdir", 
                    str(temp_dir), 
                    str(input_pptx)
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                
                # Copy from temp dir to current dir
                temp_output = list(temp_dir.glob("*.pptx"))[0]
                import shutil
                shutil.copy(temp_output, output_file)
                print(f"Conversion successful! Saved as {output_file}")
                return True
            else:
                print("LibreOffice not found. Trying alternative conversion...")
                return False
                
        except Exception as e:
            print(f"Error during conversion: {e}")
            return False

if __name__ == "__main__":
    input_file = Path("MeteoMetrics_Weather_Station_Presentation.pptx")
    if not input_file.exists():
        print(f"Error: File {input_file} does not exist.")
        sys.exit(1)
    
    result = convert_pptx(input_file)
    if not result:
        print("Could not convert file automatically. Try these alternatives:")
        print("1. Open the file with Microsoft PowerPoint (if available)")
        print("2. Upload the file to Google Slides and then download it again")
        print("3. Try the compatibility mode in your presentation software")
