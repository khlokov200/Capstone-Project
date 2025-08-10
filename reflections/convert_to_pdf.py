#!/usr/bin/env python
"""
Simple script to convert Jupyter notebook to PDF using nbconvert
"""
import nbconvert
import os
import sys
from nbconvert.exporters import PDFExporter
from nbconvert.writers import FilesWriter

def convert_notebook_to_pdf(notebook_path):
    """Convert a Jupyter notebook to PDF"""
    print(f"Converting {notebook_path} to PDF...")
    
    # Configure the exporter
    exporter = PDFExporter()
    exporter.exclude_input = True  # Only show output cells in the PDF
    
    # Convert the notebook
    output, resources = exporter.from_filename(notebook_path)
    
    # Write the output to a file
    writer = FilesWriter()
    writer.write(output, resources, os.path.splitext(notebook_path)[0])
    
    pdf_path = os.path.splitext(notebook_path)[0] + '.pdf'
    print(f"PDF created: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    notebook_path = "meteometrics_project_reflection.ipynb"
    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]
    
    convert_notebook_to_pdf(notebook_path)
