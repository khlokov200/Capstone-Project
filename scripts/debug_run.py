#!/usr/bin/env python
"""
Wrapper script to run the main app with output redirected to a log file
"""
import sys
import os
import datetime

def main():
    # Create a timestamp for the log file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"debug_log_{timestamp}.txt"
    
    # Print information
    print(f"Starting application with debug logging to: {log_file}")
    print("Close the application to view the log file.")
    
    # Open log file and redirect stdout and stderr
    log_fd = open(log_file, 'w')
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr
    sys.stdout = log_fd
    sys.stderr = log_fd
    
    try:
        # Print header info to log
        print("=== Weather App Debug Log ===")
        print(f"Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Python: {sys.version}")
        print(f"Working Dir: {os.getcwd()}")
        print("=" * 50)
        print()
        
        # Import and run main
        print("Importing main module...")
        import main as app_main
        
        print("Starting application...")
        app_main.main()
    except Exception as e:
        # Make sure exceptions are logged
        import traceback
        print(f"ERROR: {str(e)}")
        traceback.print_exc()
    finally:
        # Restore stdout and stderr
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr
        log_fd.close()
        print(f"\nApplication closed. Debug log saved to: {log_file}")

if __name__ == "__main__":
    main()
