import sys
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from attendance_system.database.db_manager import DBManager
from attendance_system.ui.styles import PROFESSIONAL_LIGHT, PROFESSIONAL_DARK
from attendance_system.ui.student_tab import StudentTab
from attendance_system.ui.grades_tab import GradesTab
from attendance_system.ui.config_tab import ConfigTab
from attendance_system.ui.reports_tab import ReportsTab


class MainWindow(QMainWindow):
    """Professional main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setGeometry(100, 100, 1400, 900)
        self.current_theme = "light"
        
        # Initialize backend
        self.db = DBManager()
        
        # Apply theme
        self.apply_theme(self.current_theme)
        
        # Setup UI
        self.setup_ui()
    
    def apply_theme(self, theme="light"):
        """Apply professional theme"""
        self.current_theme = theme
        if theme == "dark":
            self.setStyleSheet(PROFESSIONAL_DARK)
        else:
            self.setStyleSheet(PROFESSIONAL_LIGHT)
    
    def setup_ui(self):
        """Setup clean professional UI"""
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header section
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # Create tabs
        self.student_tab = StudentTab(self.db)
        self.grades_tab = GradesTab(self.db, calculate_callback=self.calculate_final_grades)
        self.config_tab = ConfigTab(self.db)
        self.reports_tab = ReportsTab(self.db)
        
        self.tabs.addTab(self.student_tab, "Students")
        self.tabs.addTab(self.grades_tab, "Grades")
        self.tabs.addTab(self.config_tab, "Settings")
        self.tabs.addTab(self.reports_tab, "Reports")
        
        content_container = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(32, 32, 32, 32)
        content_layout.setSpacing(0)
        content_layout.addWidget(self.tabs)
        content_container.setLayout(content_layout)
        
        main_layout.addWidget(content_container, 1)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def create_header(self):
        """Create professional header"""
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #e2e8f0;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(32, 0, 32, 0)
        layout.setSpacing(20)
        
        # Title section
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        title = QLabel("Student Management System")
        title.setObjectName("titleLabel")
        
        subtitle = QLabel("Manage attendance, grades, and student records")
        subtitle.setObjectName("subtitleLabel")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Theme toggle button
        theme_btn = QPushButton("Dark Mode")
        theme_btn.setObjectName("secondaryButton")
        theme_btn.setFixedSize(120, 44)
        theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn = theme_btn
        layout.addWidget(theme_btn)
        
        header_widget.setLayout(layout)
        return header_widget
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.current_theme == "light":
            self.apply_theme("dark")
            self.theme_btn.setText("Light Mode")
        else:
            self.apply_theme("light")
            self.theme_btn.setText("Dark Mode")
    
    def calculate_final_grades(self):
        """Calculate grades and navigate to reports"""
        self.reports_tab.generate_report()
        self.tabs.setCurrentIndex(3)
    
    def closeEvent(self, event):
        """Clean shutdown"""
        self.db.close()
        event.accept()