from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QGroupBox, QMessageBox, QDialog, QCheckBox,
    QScrollArea
)
from PyQt5.QtCore import Qt
from attendance_system.database.db_manager import DBManager
from attendance_system.utils.exports import export_students


class StudentTab(QWidget):
    """Student and attendance management tab"""
    
    def __init__(self, db: DBManager, export_callback=None):
        super().__init__()
        self.db = db
        self.export_callback = export_callback
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        section_title = QLabel("Student Management")
        section_title.setStyleSheet("""
            font-size: 22px; 
            font-weight: 700; 
            color: #0f172a; 
            margin-bottom: 8px;
        """)
        layout.addWidget(section_title)
        
        student_form = QGroupBox("Add or Edit Student")
        form_layout = QHBoxLayout()
        form_layout.setSpacing(12)
        
        self.student_id_input = QLineEdit()
        self.student_id_input.setPlaceholderText("Student ID")
        self.student_id_input.setFixedWidth(140)
        
        self.student_name_input = QLineEdit()
        self.student_name_input.setPlaceholderText("Full Name")
        
        self.student_course_input = QLineEdit()
        self.student_course_input.setPlaceholderText("Course")
        self.student_course_input.setFixedWidth(160)
        
        self.student_email_input = QLineEdit()
        self.student_email_input.setPlaceholderText("Email Address")
        
        add_student_btn = QPushButton("Add Student")
        add_student_btn.setObjectName("primaryButton")
        add_student_btn.setFixedWidth(140)
        add_student_btn.clicked.connect(self.add_student)
        
        form_layout.addWidget(self.student_id_input)
        form_layout.addWidget(self.student_name_input, 1)
        form_layout.addWidget(self.student_course_input)
        form_layout.addWidget(self.student_email_input, 1)
        form_layout.addWidget(add_student_btn)
        
        student_form.setLayout(form_layout)
        layout.addWidget(student_form)
        
        # Students table
        table_label = QLabel("Student List")
        table_label.setStyleSheet("font-size: 16px; font-weight: 600; margin-top: 8px;")
        layout.addWidget(table_label)
        
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(5)
        self.students_table.setHorizontalHeaderLabels([
            "Student ID", "Name", "Course", "Email", "Attendance Rate"
        ])
        self.students_table.horizontalHeader().setStretchLastSection(True)
        self.students_table.setAlternatingRowColors(True)
        layout.addWidget(self.students_table, 1)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        mark_attendance_btn = QPushButton("Mark Attendance")
        mark_attendance_btn.clicked.connect(self.mark_attendance)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setObjectName("secondaryButton")
        refresh_btn.clicked.connect(self.refresh_students)
        
        export_students_btn = QPushButton("Export to Excel")
        export_students_btn.setObjectName("secondaryButton")
        export_students_btn.clicked.connect(self.export_to_excel)
        
        try:
            import_btn = QPushButton("Import from Excel")
            import_btn.setObjectName("secondaryButton")
            import_btn.clicked.connect(self.show_import_dialog)
            btn_layout.addWidget(import_btn)
        except ImportError:
            pass
        
        btn_layout.addWidget(mark_attendance_btn)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(export_students_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.refresh_students()
    
    def add_student(self):
        """Add a new student"""
        student_id = self.student_id_input.text().strip()
        name = self.student_name_input.text().strip()
        course = self.student_course_input.text().strip()
        email = self.student_email_input.text().strip()
        
        if not student_id or not name:
            QMessageBox.warning(self, "Validation Error", "Student ID and Name are required!")
            return
        
        success = self.db.add_student(student_id, name, course, email)
        if success:
            QMessageBox.information(self, "Success", "Student added successfully!")
            self.student_id_input.clear()
            self.student_name_input.clear()
            self.student_course_input.clear()
            self.student_email_input.clear()
            self.refresh_students()
        else:
            QMessageBox.warning(self, "Error", "Student ID already exists!")
    
    def refresh_students(self):
        """Refresh students table"""
        students = self.db.get_students_with_attendance()
        self.students_table.setRowCount(len(students))
        
        for row, student in enumerate(students):
            attendance_pct = 0
            if student[4] > 0:
                attendance_pct = (student[5] / student[4]) * 100
            
            self.students_table.setItem(row, 0, QTableWidgetItem(student[0]))
            self.students_table.setItem(row, 1, QTableWidgetItem(student[1]))
            self.students_table.setItem(row, 2, QTableWidgetItem(student[2] or ""))
            self.students_table.setItem(row, 3, QTableWidgetItem(student[3] or ""))
            self.students_table.setItem(row, 4, QTableWidgetItem(f"{attendance_pct:.1f}%"))
    
    def mark_attendance(self):
        """Mark attendance for all students"""
        students = self.db.get_all_students()
        
        if not students:
            QMessageBox.warning(self, "Error", "No students found!")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Mark Attendance - " + datetime.now().strftime("%B %d, %Y"))
        dialog.setMinimumWidth(500)
        dialog.setMinimumHeight(600)
        layout = QVBoxLayout()
        layout.setSpacing(16)
        
        # Header
        header = QLabel("Select Present Students")
        header.setStyleSheet("font-weight: 600; font-size: 16px; padding: 8px 0px;")
        layout.addWidget(header)
        
        subtitle = QLabel("Students not checked will be marked as absent")
        subtitle.setStyleSheet("color: #64748b; font-size: 13px; margin-bottom: 8px;")
        layout.addWidget(subtitle)
        
        # Scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(10)
        
        checkboxes = {}
        for student_id, name, course, email in students:
            cb = QCheckBox(f"{name} ({student_id})")
            cb.setChecked(True)
            checkboxes[student_id] = cb
            scroll_layout.addWidget(cb)
        
        scroll_layout.addStretch()
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, 1)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        def save_attendance():
            today = datetime.now().strftime("%Y-%m-%d")
            for student_id, cb in checkboxes.items():
                status = "Present" if cb.isChecked() else "Absent"
                self.db.mark_attendance(student_id, today, status)
            QMessageBox.information(self, "Success", "Attendance saved successfully!")
            dialog.close()
            self.refresh_students()
        
        save_btn = QPushButton("Save Attendance")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(save_attendance)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondaryButton")
        cancel_btn.clicked.connect(dialog.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def export_to_excel(self):
        """Export students to Excel"""
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Students", "", "Excel Files (*.xlsx)"
        )
        if filename:
            try:
                export_students(self.db, filename)
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
            
            if dialog.exec_():
                self.refresh_students()
                QMessageBox.information(self, "Success", "Data imported successfully!")
        except ImportError as e:
            QMessageBox.warning(self, "Import Error", f"Import not available: {str(e)}")