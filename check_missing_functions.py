#!/usr/bin/env python3
"""
Script to check for missing button function implementations in tabs.py
"""

import re
import sys

def check_missing_functions():
    """Check for button commands that don't have corresponding function definitions"""
    
    with open('ui/tabs.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all button commands
    command_pattern = r'command=self\.([a-zA-Z_][a-zA-Z0-9_]*)'
    commands = re.findall(command_pattern, content)
    
    # Find all function definitions  
    def_pattern = r'def ([a-zA-Z_][a-zA-Z0-9_]*)\('
    definitions = re.findall(def_pattern, content)
    
    # Remove duplicate commands and definitions
    unique_commands = list(set(commands))
    unique_definitions = list(set(definitions))
    
    # Find missing functions
    missing = []
    for cmd in unique_commands:
        if cmd not in unique_definitions:
            missing.append(cmd)
    
    print(f"Found {len(unique_commands)} unique button commands")
    print(f"Found {len(unique_definitions)} unique function definitions")
    print(f"Missing {len(missing)} function implementations:\n")
    
    for func in sorted(missing):
        print(f"  - {func}")
        
    # Find commands that reference controller methods
    controller_commands = [cmd for cmd in unique_commands if cmd.startswith('controller.')]
    if controller_commands:
        print(f"\nController method references (external):")
        for cmd in sorted(controller_commands):
            print(f"  - {cmd}")
    
    return missing

if __name__ == "__main__":
    missing = check_missing_functions()
    sys.exit(len(missing))  # Exit with number of missing functions
