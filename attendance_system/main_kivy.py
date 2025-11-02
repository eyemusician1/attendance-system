"""
Entry point for Kivy version
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    from attendance_system.ui_kivy.main_app import StudentManagementApp
    StudentManagementApp().run()