import os
import sys
import sqlite3
from typing import List, Tuple, Optional, Dict


class DBManager:
    """Manages all database operations for the attendance system"""

    def __init__(self, db_path: str = None):
        """Initialize database connection"""
        if db_path is None:
            db_path = self._get_database_path()

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.init_tables()

    def _get_database_path(self) -> str:
        """
        Get the correct database path for both .py and .exe
        This ensures the database works in development and production
        """
        # Determine if running as script or frozen exe
        if getattr(sys, 'frozen', False):
            # Running as compiled .exe (PyInstaller)
            application_path = os.path.dirname(sys.executable)
        else:
            # Running as Python script
            # Go up one level from database/ to attendance_system/
            application_path = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )

        # Create 'data' directory for database
        data_dir = os.path.join(application_path, 'data')

        # Create directory if it doesn't exist
        try:
            os.makedirs(data_dir, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create data directory: {e}")
            # Fallback to user's documents folder
            data_dir = os.path.join(
                os.path.expanduser('~'),
                'Documents',
                'AttendanceSystem',
                'data'
            )
            os.makedirs(data_dir, exist_ok=True)

        db_path = os.path.join(data_dir, 'attendance.db')
        print(f"Database location: {db_path}")
        return db_path

    def init_tables(self):
        """Initialize database tables with enhanced schema"""
        # Students table
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS students
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                student_id
                                TEXT
                                UNIQUE,
                                name
                                TEXT,
                                course
                                TEXT,
                                email
                                TEXT
                            )
                            """)

        # Attendance table
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS attendance
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                student_id
                                TEXT,
                                date
                                TEXT,
                                status
                                TEXT,
                                FOREIGN
                                KEY
                            (
                                student_id
                            ) REFERENCES students
                            (
                                student_id
                            )
                                )
                            """)

        # Grades table
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS grades
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                student_id
                                TEXT,
                                assessment_type
                                TEXT,
                                assessment_name
                                TEXT,
                                score
                                REAL,
                                max_score
                                REAL,
                                date
                                TEXT,
                                FOREIGN
                                KEY
                            (
                                student_id
                            ) REFERENCES students
                            (
                                student_id
                            )
                                )
                            """)

        # Grading configuration table
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS grading_config
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                component
                                TEXT
                                UNIQUE,
                                weight
                                REAL
                            )
                            """)

        # Initialize default grading config if not exists
        self.cursor.execute("SELECT COUNT(*) FROM grading_config")
        if self.cursor.fetchone()[0] == 0:
            default_config = [
                ('Attendance', 10.0),
                ('Quizzes', 20.0),
                ('Assignments', 30.0),
                ('Midterm', 20.0),
                ('Final Exam', 20.0)
            ]
            self.cursor.executemany(
                "INSERT INTO grading_config (component, weight) VALUES (?, ?)",
                default_config
            )

        self.conn.commit()

    # ==================== STUDENT OPERATIONS ====================

    def add_student(self, student_id: str, name: str, course: str = "", email: str = "") -> bool:
        """Add a new student"""
        try:
            self.cursor.execute(
                "INSERT INTO students (student_id, name, course, email) VALUES (?, ?, ?, ?)",
                (student_id, name, course, email)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_students(self) -> List[Tuple]:
        """Get all students"""
        self.cursor.execute("SELECT student_id, name, course, email FROM students ORDER BY name")
        return self.cursor.fetchall()

    def get_student(self, student_id: str) -> Optional[Tuple]:
        """Get a specific student"""
        self.cursor.execute("SELECT student_id, name, course, email FROM students WHERE student_id = ?", (student_id,))
        return self.cursor.fetchone()

    def student_exists(self, student_id: str) -> bool:
        """Check if a student exists by student_id"""
        self.cursor.execute("SELECT id FROM students WHERE student_id = ?", (student_id,))
        return self.cursor.fetchone() is not None

    def get_students_with_attendance(self) -> List[Tuple]:
        """Get students with attendance statistics"""
        self.cursor.execute("""
                            SELECT s.student_id,
                                   s.name,
                                   s.course,
                                   s.email,
                                   COUNT(a.id)                                           as total_days,
                                   SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_days
                            FROM students s
                                     LEFT JOIN attendance a ON s.student_id = a.student_id
                            GROUP BY s.student_id
                            ORDER BY s.name
                            """)
        return self.cursor.fetchall()

    def delete_student(self, student_id: str) -> bool:
        """Delete a student and all related records"""
        try:
            self.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            self.cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
            self.cursor.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
            self.conn.commit()
            return True
        except Exception:
            return False

    # ==================== ATTENDANCE OPERATIONS ====================

    def mark_attendance(self, student_id: str, date: str, status: str):
        """Mark attendance for a student"""
        self.cursor.execute(
            "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
            (student_id, date, status)
        )
        self.conn.commit()

    def get_attendance_stats(self, student_id: str) -> Tuple[int, int]:
        """Get attendance statistics for a student"""
        self.cursor.execute("""
                            SELECT COUNT(*)                                            as total,
                                   SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present
                            FROM attendance
                            WHERE student_id = ?
                            """, (student_id,))
        return self.cursor.fetchone()

    def get_attendance_by_day(self, student_id: str) -> Dict[str, bool]:
        """Get attendance status for each day of the week (Mon-Sat) for current week"""
        from datetime import datetime, timedelta

        # Get current week (Monday to Saturday)
        today = datetime.now()
        # Get Monday of current week
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday)

        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        attendance_dict = {day: False for day in days_of_week}

        # Get attendance records for current week
        for i in range(6):  # Mon to Sat
            day_date = (monday + timedelta(days=i)).strftime("%Y-%m-%d")
            self.cursor.execute("""
                                SELECT status
                                FROM attendance
                                WHERE student_id = ? AND date = ?
                                """, (student_id, day_date))
            result = self.cursor.fetchone()
            if result:
                attendance_dict[days_of_week[i]] = (result[0] == 'Present')

        return attendance_dict

    def mark_attendance_by_day(self, student_id: str, day_name: str, status: bool):
        """Mark attendance for a specific day of the current week"""
        from datetime import datetime, timedelta

        # Map day name to index
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if day_name not in days_of_week:
            return

        day_index = days_of_week.index(day_name)

        # Get Monday of current week
        today = datetime.now()
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday)
        day_date = (monday + timedelta(days=day_index)).strftime("%Y-%m-%d")

        # Check if record exists
        self.cursor.execute("""
                            SELECT id
                            FROM attendance
                            WHERE student_id = ? AND date = ?
                            """, (student_id, day_date))

        status_str = "Present" if status else "Absent"

        if self.cursor.fetchone():
            # Update existing record
            self.cursor.execute("""
                                UPDATE attendance
                                SET status = ?
                                WHERE student_id = ? AND date = ?
                                """, (status_str, student_id, day_date))
        else:
            # Insert new record
            self.cursor.execute("""
                                INSERT INTO attendance (student_id, date, status)
                                VALUES (?, ?, ?)
                                """, (student_id, day_date, status_str))

        self.conn.commit()

    def get_attendance_percentage(self, student_id: str) -> float:
        """Get attendance percentage for a student"""
        total, present = self.get_attendance_stats(student_id)
        return (present / total * 100) if total > 0 else 0.0

    # ==================== GRADE OPERATIONS ====================

    def add_grade(self, student_id: str, assessment_type: str, assessment_name: str,
                  score: float, max_score: float, date: str):
        """Add a grade entry"""
        self.cursor.execute(
            "INSERT INTO grades (student_id, assessment_type, assessment_name, score, max_score, date) VALUES (?, ?, ?, ?, ?, ?)",
            (student_id, assessment_type, assessment_name, score, max_score, date)
        )
        self.conn.commit()

    def get_all_grades(self) -> List[Tuple]:
        """Get all grades with student names"""
        self.cursor.execute("""
                            SELECT g.student_id,
                                   s.name,
                                   g.assessment_type,
                                   g.assessment_name,
                                   g.score,
                                   g.max_score,
                                   g.date
                            FROM grades g
                                     JOIN students s ON g.student_id = s.student_id
                            ORDER BY g.date DESC, s.name
                            """)
        return self.cursor.fetchall()

    def get_student_grades_by_type(self, student_id: str, assessment_type: str) -> Optional[float]:
        """Get average grade for a student by assessment type"""
        self.cursor.execute("""
                            SELECT AVG(score * 100.0 / max_score)
                            FROM grades
                            WHERE student_id = ?
                              AND assessment_type = ?
                            """, (student_id, assessment_type))
        result = self.cursor.fetchone()[0]
        return result if result else 0.0

    def delete_grade(self, grade_id: int) -> bool:
        """Delete a grade entry"""
        try:
            self.cursor.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
            self.conn.commit()
            return True
        except Exception:
            return False

    # ==================== CONFIGURATION OPERATIONS ====================

    def get_grading_config(self) -> List[Tuple]:
        """Get grading configuration"""
        self.cursor.execute("SELECT component, weight FROM grading_config ORDER BY id")
        return self.cursor.fetchall()

    def update_grading_config(self, component: str, weight: float):
        """Update grading configuration"""
        self.cursor.execute(
            "UPDATE grading_config SET weight = ? WHERE component = ?",
            (weight, component)
        )
        self.conn.commit()

    def add_grading_component(self, component: str, weight: float):
        """Add a new grading component"""
        try:
            self.cursor.execute(
                "INSERT INTO grading_config (component, weight) VALUES (?, ?)",
                (component, weight)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Component already exists
            return False

    def delete_grading_component(self, component: str):
        """Delete a grading component"""
        try:
            self.cursor.execute(
                "DELETE FROM grading_config WHERE component = ?",
                (component,)
            )
            self.conn.commit()
            return True
        except Exception:
            return False

    def reset_grading_config(self):
        """Reset to default grading configuration"""
        # Clear all existing components
        self.cursor.execute("DELETE FROM grading_config")

        # Insert default components
        default_config = [
            ('Attendance', 10.0),
            ('Quizzes', 20.0),
            ('Assignments', 30.0),
            ('Midterm', 20.0),
            ('Final Exam', 20.0)
        ]
        self.cursor.executemany(
            "INSERT INTO grading_config (component, weight) VALUES (?, ?)",
            default_config
        )
        self.conn.commit()

    # ==================== BACKUP & MAINTENANCE ====================

    def backup_database(self) -> str:
        """Create a backup of the database"""
        import shutil
        from datetime import datetime

        backup_dir = os.path.join(os.path.dirname(self.db_path), 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f'attendance_backup_{timestamp}.db')

        # Close connection temporarily
        self.conn.close()

        # Copy database file
        shutil.copy2(self.db_path, backup_path)

        # Reconnect
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        return backup_path

    def get_database_info(self) -> Dict[str, any]:
        """Get database information"""
        info = {}
        info['path'] = self.db_path
        info['size_mb'] = round(os.path.getsize(self.db_path) / (1024 * 1024), 2)

        # Count records
        self.cursor.execute("SELECT COUNT(*) FROM students")
        info['total_students'] = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM grades")
        info['total_grades'] = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM attendance")
        info['total_attendance'] = self.cursor.fetchone()[0]

        return info

    # ==================== CLEANUP ====================

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Destructor - ensure connection is closed"""
        try:
            self.close()
        except:
            pass