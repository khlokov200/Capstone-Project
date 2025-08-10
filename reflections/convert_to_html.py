#!/usr/bin/env python
"""
Script to convert Jupyter notebook to HTML for easy PDF conversion
"""
import nbconvert
import os
import sys

def convert_notebook_to_html(notebook_path):
    """Convert a Jupyter notebook to HTML"""
    print(f"Converting {notebook_path} to HTML...")
    
    # Execute the conversion command
    os.system(f"jupyter nbconvert --to html {notebook_path}")
    
    html_path = os.path.splitext(notebook_path)[0] + '.html'
    print(f"HTML created: {html_path}")
    print(f"\nTo convert to PDF:\n1. Open the HTML file in a web browser\n2. Use the browser's Print function\n3. Select 'Save as PDF' as the destination")
    return html_path

if __name__ == "__main__":
    notebook_path = "meteometrics_project_reflection.ipynb"
    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]
    
    convert_notebook_to_html(notebook_path)
