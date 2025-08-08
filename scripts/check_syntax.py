"""
Check syntax of modified files
"""
import ast

def check_file_syntax(file_path):
    """Check Python file for syntax errors"""
    print(f"Checking {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        ast.parse(content)
        print(f"✅ {file_path} - Syntax OK")
        return True
    except SyntaxError as e:
        print(f"❌ {file_path} - Syntax Error: {e}")
        print(f"  Line {e.lineno}, Column {e.offset}: {e.text.strip()}")
        return False

if __name__ == "__main__":
    # Files to check
    files = [
        "ui/tabs.py",
    ]
    
    for file_path in files:
        check_file_syntax(file_path)
