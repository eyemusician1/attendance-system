"""
Entry point for ttkbootstrap version of Student Management System
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import and run the application
if __name__ == "__main__":
    from attendance_system.ui_tkinter.main_app import MainApplication
    
    app = MainApplication()
    app.mainloop()