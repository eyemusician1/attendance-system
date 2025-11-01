from dataclasses import dataclass
from typing import Optional


@dataclass
class Grade:
    """Grade data model"""
    student_id: str
    assessment_type: str
    assessment_name: str
    score: float
    max_score: float
    date: str
    percentage: Optional[float] = None
    
    def __post_init__(self):
        """Calculate percentage after initialization"""
        if self.max_score > 0:
            self.percentage = (self.score / self.max_score) * 100
    
    def __str__(self):
        return f"{self.assessment_name}: {self.score}/{self.max_score} ({self.percentage:.1f}%)"


