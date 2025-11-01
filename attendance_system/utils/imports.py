import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox


class ExcelImporter:
    """Handles importing data from Excel files"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def import_students(self, filename):
        """
        Import students from Excel file
        
        Expected columns: Student ID, Name, Course, Email (optional)
        """
        try:
            # Read Excel file
            df = pd.read_excel(filename)
            
            # Clean column names (remove extra spaces)
            df.columns = df.columns.str.strip()
            
            # Validate required columns
            required_columns = ['Student ID', 'Name']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return {
                    'success': False,
                    'message': f"Missing required columns: {', '.join(missing_columns)}",
                    'imported': 0,
                    'skipped': 0,
                    'errors': []
                }
            
            # Optional columns
            if 'Course' not in df.columns:
                df['Course'] = ''
            if 'Email' not in df.columns:
                df['Email'] = ''
            
            # Remove rows with empty Student ID or Name
            df = df.dropna(subset=['Student ID', 'Name'])
            
            # Convert Student ID to string
            df['Student ID'] = df['Student ID'].astype(str).str.strip()
            df['Name'] = df['Name'].astype(str).str.strip()
            
            imported = 0
            skipped = 0
            errors = []
            
            # Import each student
            for index, row in df.iterrows():
                student_id = row['Student ID']
                name = row['Name']
                course = str(row['Course']) if pd.notna(row['Course']) else ''
                email = str(row['Email']) if pd.notna(row['Email']) else ''
                
                try:
                    # Check if student already exists
                    if self.db.student_exists(student_id):
                        skipped += 1
                        errors.append(f"Row {index + 2}: Student {student_id} already exists")
                        continue
                    
                    # Add student
                    self.db.add_student(student_id, name, course, email)
                    imported += 1
                    
                except Exception as e:
                    errors.append(f"Row {index + 2}: {str(e)}")
                    skipped += 1
            
            return {
                'success': True,
                'message': f"Successfully imported {imported} students",
                'imported': imported,
                'skipped': skipped,
                'errors': errors
            }
            
        except FileNotFoundError:
            return {
                'success': False,
                'message': "File not found",
                'imported': 0,
                'skipped': 0,
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Import failed: {str(e)}",
                'imported': 0,
                'skipped': 0,
                'errors': []
            }
    
    def import_grades(self, filename):
        """
        Import grades from Excel file
        
        Expected columns: Student ID, Assessment Type, Assessment Name, Score, Max Score, Date (optional)
        """
        try:
            df = pd.read_excel(filename)
            df.columns = df.columns.str.strip()
            
            # Validate required columns
            required_columns = ['Student ID', 'Assessment Type', 'Assessment Name', 'Score', 'Max Score']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return {
                    'success': False,
                    'message': f"Missing required columns: {', '.join(missing_columns)}",
                    'imported': 0,
                    'skipped': 0,
                    'errors': []
                }
            
            # Add Date column if not present
            if 'Date' not in df.columns:
                df['Date'] = datetime.now().strftime("%Y-%m-%d")
            
            # Remove empty rows
            df = df.dropna(subset=['Student ID', 'Assessment Type', 'Assessment Name'])
            
            # Convert types
            df['Student ID'] = df['Student ID'].astype(str).str.strip()
            
            imported = 0
            skipped = 0
            errors = []
            
            # Valid assessment types
            valid_types = ['Attendance', 'Quizzes', 'Assignments', 'Midterm', 'Final Exam']
            
            for index, row in df.iterrows():
                student_id = row['Student ID']
                assessment_type = str(row['Assessment Type']).strip()
                assessment_name = str(row['Assessment Name']).strip()
                
                try:
                    score = float(row['Score'])
                    max_score = float(row['Max Score'])
                except (ValueError, TypeError):
                    errors.append(f"Row {index + 2}: Invalid score values")
                    skipped += 1
                    continue
                
                # Validate student exists
                if not self.db.student_exists(student_id):
                    errors.append(f"Row {index + 2}: Student {student_id} not found")
                    skipped += 1
                    continue
                
                # Validate assessment type
                if assessment_type not in valid_types:
                    errors.append(f"Row {index + 2}: Invalid assessment type '{assessment_type}'")
                    skipped += 1
                    continue
                
                # Validate scores
                if score < 0 or max_score <= 0 or score > max_score:
                    errors.append(f"Row {index + 2}: Invalid score range")
                    skipped += 1
                    continue
                
                try:
                    self.db.add_grade(student_id, assessment_type, assessment_name, score, max_score)
                    imported += 1
                except Exception as e:
                    errors.append(f"Row {index + 2}: {str(e)}")
                    skipped += 1
            
            return {
                'success': True,
                'message': f"Successfully imported {imported} grades",
                'imported': imported,
                'skipped': skipped,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f"Import failed: {str(e)}",
                'imported': 0,
                'skipped': 0,
                'errors': []
            }
    
    def import_attendance(self, filename):
        """
        Import attendance from Excel file
        
        Expected columns: Student ID, Date, Status
        Status should be: Present, Absent, Late, or Excused
        """
        try:
            df = pd.read_excel(filename)
            df.columns = df.columns.str.strip()
            
            # Validate required columns
            required_columns = ['Student ID', 'Date', 'Status']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return {
                    'success': False,
                    'message': f"Missing required columns: {', '.join(missing_columns)}",
                    'imported': 0,
                    'skipped': 0,
                    'errors': []
                }
            
            # Remove empty rows
            df = df.dropna(subset=['Student ID', 'Date', 'Status'])
            
            # Convert types
            df['Student ID'] = df['Student ID'].astype(str).str.strip()
            df['Status'] = df['Status'].astype(str).str.strip()
            
            imported = 0
            skipped = 0
            errors = []
            
            valid_statuses = ['Present', 'Absent', 'Late', 'Excused']
            
            for index, row in df.iterrows():
                student_id = row['Student ID']
                status = row['Status']
                
                # Parse date
                try:
                    if isinstance(row['Date'], str):
                        date = pd.to_datetime(row['Date']).strftime("%Y-%m-%d")
                    else:
                        date = row['Date'].strftime("%Y-%m-%d")
                except:
                    errors.append(f"Row {index + 2}: Invalid date format")
                    skipped += 1
                    continue
                
                # Validate student exists
                if not self.db.student_exists(student_id):
                    errors.append(f"Row {index + 2}: Student {student_id} not found")
                    skipped += 1
                    continue
                
                # Validate status
                if status not in valid_statuses:
                    errors.append(f"Row {index + 2}: Invalid status '{status}'")
                    skipped += 1
                    continue
                
                try:
                    self.db.add_attendance(student_id, date, status)
                    imported += 1
                except Exception as e:
                    errors.append(f"Row {index + 2}: {str(e)}")
                    skipped += 1
            
            return {
                'success': True,
                'message': f"Successfully imported {imported} attendance records",
                'imported': imported,
                'skipped': skipped,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f"Import failed: {str(e)}",
                'imported': 0,
                'skipped': 0,
                'errors': []
            }
    
    def show_import_result(self, result, parent=None):
        """Display import results in a message box"""
        if result['success']:
            message = f"{result['message']}\n\n"
            message += f"✅ Imported: {result['imported']}\n"
            message += f"⚠️ Skipped: {result['skipped']}\n"
            
            if result['errors']:
                message += f"\n❌ Errors ({len(result['errors'])}):\n"
                # Show first 10 errors only
                for error in result['errors'][:10]:
                    message += f"  • {error}\n"
                if len(result['errors']) > 10:
                    message += f"  • ... and {len(result['errors']) - 10} more\n"
            
            QMessageBox.information(parent, "Import Complete", message)
        else:
            QMessageBox.warning(parent, "Import Failed", result['message'])
        
        return result
