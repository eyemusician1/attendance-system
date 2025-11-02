"""
Utility script to clear all data from the attendance database.
This will delete all records but keep the table structure intact.
"""
import os
import sqlite3

def clear_database():
    """Clear all data from the attendance database"""
    # Get the database path
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_file_dir, "attendance.db")
    
    if not os.path.exists(db_path):
        print("Database file not found. Nothing to clear.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Disable foreign key constraints temporarily
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        # Delete all data from tables (in correct order due to foreign keys)
        print("Clearing database...")
        cursor.execute("DELETE FROM attendance")
        cursor.execute("DELETE FROM grades")
        cursor.execute("DELETE FROM students")
        cursor.execute("DELETE FROM grading_config")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('students', 'attendance', 'grades', 'grading_config')")
        
        # Re-enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        conn.commit()
        conn.close()
        
        print("✅ Database cleared successfully!")
        print("All student, attendance, grade, and configuration data has been deleted.")
        print("Note: The database structure (tables) remains intact.")
        
    except Exception as e:
        print(f"❌ Error clearing database: {e}")

if __name__ == "__main__":
    response = input("⚠️  This will delete ALL data from the database. Are you sure? (yes/no): ")
    if response.lower() == "yes":
        clear_database()
    else:
        print("Operation cancelled.")




