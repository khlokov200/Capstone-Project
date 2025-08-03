#!/usr/bin/env python3
"""
Script to fix syntax errors in tabs.py
"""

def fix_track_severe_weather():
    """Fix the track_severe_weather function by removing orphaned code"""
    
    with open('ui/tabs.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the problematic line with StyledButton(radar_controls
    problem_line_index = None
    for i, line in enumerate(lines):
        if "StyledButton(radar_controls" in line:
            problem_line_index = i
            break
    
    if problem_line_index is not None:
        print(f"Found problematic line at index {problem_line_index}: {lines[problem_line_index].strip()}")
        
        # Find the start of the orphaned code section
        start_orphan = None
        for i in range(problem_line_index, -1, -1):
            if "# Remove legacy content" in lines[i]:
                start_orphan = i
                break
        
        # Find the end of the track_severe_weather function
        end_function = None
        for i in range(problem_line_index, len(lines)):
            if lines[i].strip().startswith("def ") and i > problem_line_index:
                end_function = i
                break
        
        if start_orphan is not None and end_function is not None:
            print(f"Removing orphaned code from line {start_orphan} to {end_function-1}")
            
            # Remove the orphaned lines
            new_lines = lines[:start_orphan] + ["\n"] + lines[end_function:]
            
            with open('ui/tabs.py', 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            print("Fixed track_severe_weather function!")
            return True
    
    print("No problems found in track_severe_weather function")
    return False

if __name__ == "__main__":
    fix_track_severe_weather()
