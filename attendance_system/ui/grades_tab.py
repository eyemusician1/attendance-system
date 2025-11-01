from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QGroupBox, QMessageBox, QComboBox, QDoubleSpinBox,
    QLabel, QFileDialog
)
from attendance_system.database.db_manager import DBManager
from attendance_system.utils.exports import export_grades


class GradesTab(QWidget):
    """Grades management tab"""
    
    def __init__(self, db: DBManager, calculate_callback=None):
        super().__init__()
        self.db = db
        self.calculate_callback = calculate_callback
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        section_title = QLabel("Grade Management")
        section_title.setStyleSheet("""
            font-size: 22px; 
            font-weight: 700; 
            color: #0f172a; 
            margin-bottom: 8px;
        """)
        layout.addWidget(section_title)
        
        grade_form = QGroupBox("Add Grade or Score")
        form_layout = QHBoxLayout()
        form_layout.setSpacing(12)
        
        self.grade_student_id = QLineEdit()
        self.grade_student_id.setPlaceholderText("Student ID")
        self.grade_student_id.setFixedWidth(140)
        
        self.assessment_type = QComboBox()
        self.assessment_type.addItems([
            "Attendance", "Quizzes", "Assignments", "Midterm", "Final Exam"
        ])
        self.assessment_type.setFixedWidth(160)
        
        self.assessment_name = QLineEdit()
        self.assessment_name.setPlaceholderText("Assessment Name")
        
        self.score_input = QDoubleSpinBox()
        self.score_input.setMaximum(1000)
        self.score_input.setPrefix("Score: ")
        self.score_input.setFixedWidth(130)
        
        self.max_score_input = QDoubleSpinBox()
        self.max_score_input.setMaximum(1000)
        self.max_score_input.setValue(100)
        self.max_score_input.setPrefix("Max: ")
        self.max_score_input.setFixedWidth(130)
        
        add_grade_btn = QPushButton("Add Grade")
        add_grade_btn.setObjectName("primaryButton")
        add_grade_btn.setFixedWidth(140)
        add_grade_btn.clicked.connect(self.add_grade)
        
        form_layout.addWidget(self.grade_student_id)
        form_layout.addWidget(self.assessment_type)
        form_layout.addWidget(self.assessment_name, 1)
        form_layout.addWidget(self.score_input)
        form_layout.addWidget(self.max_score_input)
        form_layout.addWidget(add_grade_btn)
        
        grade_form.setLayout(form_layout)
        layout.addWidget(grade_form)
        
        # Grades table
        table_label = QLabel("Grade Records")
        table_label.setStyleSheet("font-size: 16px; font-weight: 600; margin-top: 8px;")
        layout.addWidget(table_label)
        
        self.grades_table = QTableWidget()
        self.grades_table.setColumnCount(8)
        self.grades_table.setHorizontalHeaderLabels([
            "Student ID", "Name", "Type", "Assessment", "Score", "Max", "Percentage", "Date"
        ])
        self.grades_table.horizontalHeader().setStretchLastSection(True)
        self.grades_table.setAlternatingRowColors(True)
        layout.addWidget(self.grades_table, 1)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        try:
            import_btn = QPushButton("Import Grades")
            import_btn.setObjectName("secondaryButton")
            import_btn.clicked.connect(self.show_import_dialog)
            btn_layout.addWidget(import_btn)
        except ImportError:
            pass
        
        calc_grades_btn = QPushButton("Calculate Final Grades")
        calc_grades_btn.clicked.connect(self.calculate_final_grades)
        
        refresh_grades_btn = QPushButton("Refresh")
        refresh_grades_btn.setObjectName("secondaryButton")
        refresh_grades_btn.clicked.connect(self.refresh_grades)
        
        export_grades_btn = QPushButton("Export to Excel")
        export_grades_btn.setObjectName("secondaryButton")
        export_grades_btn.clicked.connect(self.export_to_excel)
        
        btn_layout.addWidget(calc_grades_btn)
        btn_layout.addWidget(refresh_grades_btn)
        btn_layout.addWidget(export_grades_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.refresh_grades()
    
    def add_grade(self):
        """Add a grade entry"""
        student_id = self.grade_student_id.text().strip()
        assessment_type = self.assessment_type.currentText()
        assessment_name = self.assessment_name.text().strip()
        score = self.score_input.value()
        max_score = self.max_score_input.value()
        
        if not student_id or not assessment_name:
            QMessageBox.warning(
                self, "Validation Error", 
                "Student ID and Assessment Name are required!"
            )
            return
        
        if max_score == 0:
            QMessageBox.warning(self, "Validation Error", "Max score cannot be zero!")
            return
        
        if not self.db.get_student(student_id):
            QMessageBox.warning(self, "Error", "Student ID not found!")
            return
        
        try:
            date = datetime.now().strftime("%Y-%m-%d")
            self.db.add_grade(student_id, assessment_type, assessment_name, score, max_score, date)
            QMessageBox.information(self, "Success", "Grade added successfully!")
            
            self.grade_student_id.clear()
            self.assessment_name.clear()
            self.score_input.setValue(0)
            self.max_score_input.setValue(100)
            
            self.refresh_grades()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def refresh_grades(self):
        """Refresh grades table"""
        grades = self.db.get_all_grades()
        self.grades_table.setRowCount(len(grades))
        
        for row, grade in enumerate(grades):
            percentage = (grade[4] / grade[5]) * 100 if grade[5] > 0 else 0
            
            self.grades_table.setItem(row, 0, QTableWidgetItem(grade[0]))
            self.grades_table.setItem(row, 1, QTableWidgetItem(grade[1]))
            self.grades_table.setItem(row, 2, QTableWidgetItem(grade[2]))
            self.grades_table.setItem(row, 3, QTableWidgetItem(grade[3]))
            self.grades_table.setItem(row, 4, QTableWidgetItem(f"{grade[4]:.1f}"))
            self.grades_table.setItem(row, 5, QTableWidgetItem(f"{grade[5]:.1f}"))
            self.grades_table.setItem(row, 6, QTableWidgetItem(f"{percentage:.1f}%"))
            self.grades_table.setItem(row, 7, QTableWidgetItem(grade[6]))
    
    def calculate_final_grades(self):
        """Calculate final grades"""
        if self.calculate_callback:
            self.calculate_callback()
    
    def export_to_excel(self):
        """Export grades to Excel"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Grades", "", "Excel Files (*.xlsx)"
        )
        if filename:
            try:
                export_grades(self.db, filename)
                QMessageBox.information(self, "Success", "File exported successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Export failed: {str(e)}")
    
    def show_import_dialog(self):
        """Show import dialog"""
        try:
            from attendance_system.utils.imports import ExcelImporter
            from attendance_system.ui.import_dialog import ImportDialog
            
            importer = ExcelImporter(self.db)
            dialog = ImportDialog(importer, self)
            dialog.import_type.setCurrentText("Grades")
            
            if dialog.exec_():
                self.refresh_grades()
                QMessageBox.information(self, "Success", "Grades imported successfully!")
        except ImportError as e:
            QMessageBox.warning(self, "Import Error", f"Import not available: {str(e)}")