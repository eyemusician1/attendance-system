from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    """Student data model"""
    student_id: str
    name: str
    course: Optional[str] = ""
    email: Optional[str] = ""
    attendance_percentage: Optional[float] = None
    
    def __str__(self):
        return f"{self.name} ({self.student_id})"


