from typing import Dict, List
from attendance_system.database.db_manager import DBManager


def get_letter_grade(percentage: float) -> float:
    """Convert percentage to grade point based on the grading scale:
    100% = 1.00, 90% = 1.25, 85% = 1.75, 80% = 2.00,
    75% = 2.25, 70% = 2.50, 65% = 2.75, 60% = 3.00,
    below 60% = 5.00
    """
    if percentage >= 100:
        return 1.00
    elif percentage >= 90:
        return 1.25
    elif percentage >= 85:
        return 1.75
    elif percentage >= 80:
        return 2.00
    elif percentage >= 75:
        return 2.25
    elif percentage >= 70:
        return 2.50
    elif percentage >= 65:
        return 2.75
    elif percentage >= 60:
        return 3.00
    else:
        return 5.00


def calculate_final_grade(db: DBManager, student_id: str) -> Dict:
    """Calculate final grade for a student"""
    # Get grading weights
    config = db.get_grading_config()
    weights = {comp: weight / 100.0 for comp, weight in config}
    
    grades = {}
    
    # Calculate attendance score
    total, present = db.get_attendance_stats(student_id)
    attendance_pct = (present / total * 100) if total > 0 else 0
    grades['Attendance'] = attendance_pct
    
    # Calculate average for each assessment type
    for component in ['Quizzes', 'Assignments', 'Midterm', 'Final Exam']:
        avg = db.get_student_grades_by_type(student_id, component)
        grades[component] = avg if avg else 0.0
    
    # Calculate weighted final grade
    final_grade = sum(grades.get(comp, 0) * weights.get(comp, 0) for comp in weights.keys())
    letter = get_letter_grade(final_grade)
    
    return {
        'grades': grades,
        'final': final_grade,
        'letter': letter
    }


def generate_report(db: DBManager) -> List[Dict]:
    """Generate comprehensive grade report for all students"""
    students = db.get_all_students()
    report_data = []
    
    for student_id, name, course, email in students:
        grade_data = calculate_final_grade(db, student_id)
        report_data.append({
            'student_id': student_id,
            'name': name,
            'course': course,
            'email': email,
            **grade_data
        })
    
    return report_data


