import pandas as pd
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFileDialog, QTextEdit, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt


class ImportDialog(QDialog):
    """Professional import dialog"""
    
    def __init__(self, importer, parent=None):
        super().__init__(parent)
        self.importer = importer
        self.setWindowTitle("Import Data from Excel")
        self.setModal(True)
        self.setMinimumWidth(650)
        self.setMinimumHeight(500)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("Import Data from Excel")
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: 700; 
            color: #0f172a;
            margin-bottom: 8px;
        """)
        layout.addWidget(title)
        
        subtitle = QLabel("Select import type and choose your Excel file")
        subtitle.setStyleSheet("color: #64748b; font-size: 14px; margin-bottom: 12px;")
        layout.addWidget(subtitle)
        
        # Import type selection
        type_group = QGroupBox("Import Type")
        type_layout = QVBoxLayout()
        type_layout.setSpacing(12)
        
        self.import_type = QComboBox()
        self.import_type.addItems(["Students", "Grades", "Attendance"])
        self.import_type.currentTextChanged.connect(self.update_format_info)
        
        type_layout.addWidget(QLabel("What would you like to import?"))
        type_layout.addWidget(self.import_type)
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # Format information
        format_group = QGroupBox("Required Excel Format")
        format_layout = QVBoxLayout()
        
        self.format_info = QTextEdit()
        self.format_info.setReadOnly(True)
        self.format_info.setMaximumHeight(150)
        self.format_info.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        format_layout.addWidget(self.format_info)
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        self.update_format_info()
        
        # File selection
        file_layout = QHBoxLayout()
        file_layout.setSpacing(12)
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #64748b; font-style: italic;")
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("secondaryButton")
        browse_btn.setFixedWidth(100)
        browse_btn.clicked.connect(self.browse_file)
        
        file_layout.addWidget(QLabel("Selected File:"))
        file_layout.addWidget(self.file_label, 1)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        # Download template button
        template_btn = QPushButton("Download Template")
        template_btn.setObjectName("secondaryButton")
        template_btn.clicked.connect(self.download_template)
        layout.addWidget(template_btn)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        button_layout.addStretch()
        
        import_btn = QPushButton("Import Data")
        import_btn.setObjectName("primaryButton")
        import_btn.setMinimumWidth(120)
        import_btn.clicked.connect(self.import_data)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondaryButton")
        cancel_btn.setMinimumWidth(120)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(import_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def update_format_info(self):
        """Update format information"""
        import_type = self.import_type.currentText()
        
        if import_type == "Students":
            info = """<b>Required Columns:</b><br>
• Student ID (required)<br>
• Name (required)<br>
• Course (optional)<br>
• Email (optional)<br><br>

<b>Example:</b><br>
2021001 | John Doe | BSCS | john@email.com"""
        elif import_type == "Grades":
            info = """<b>Required Columns:</b><br>
• Student ID (required)<br>
• Assessment Type (Attendance, Quizzes, Assignments, Midterm, Final Exam)<br>
• Assessment Name (required)<br>
• Score (number)<br>
• Max Score (number)<br><br>

<b>Example:</b><br>
2021001 | Quizzes | Quiz 1 | 45 | 50"""
        else:  # Attendance
            info = """<b>Required Columns:</b><br>
• Student ID (required)<br>
• Date (format: YYYY-MM-DD)<br>
• Status (Present, Absent, Late, Excused)<br><br>

<b>Example:</b><br>
2021001 | 2024-01-15 | Present"""
        
        self.format_info.setHtml(info)
    
    def browse_file(self):
        """Browse for Excel file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)"
        )
        
        if filename:
            self.selected_file = filename
            import os
            self.file_label.setText(os.path.basename(filename))
            self.file_label.setStyleSheet("color: #059669; font-weight: 600;")
    
    def download_template(self):
        """Download template"""
        import_type = self.import_type.currentText()
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Template", f"{import_type.lower()}_template.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if filename:
            try:
                if import_type == "Students":
                    df = pd.DataFrame({
                        'Student ID': ['2021001', '2021002', '2021003'],
                        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
                        'Course': ['BSCS', 'BSIT', 'BSCS'],
                        'Email': ['john@email.com', 'jane@email.com', 'bob@email.com']
                    })
                elif import_type == "Grades":
                    df = pd.DataFrame({
                        'Student ID': ['2021001', '2021001', '2021002'],
                        'Assessment Type': ['Quizzes', 'Assignments', 'Quizzes'],
                        'Assessment Name': ['Quiz 1', 'Assignment 1', 'Quiz 1'],
                        'Score': [45, 90, 42],
                        'Max Score': [50, 100, 50]
                    })
                else:  # Attendance
                    df = pd.DataFrame({
                        'Student ID': ['2021001', '2021002', '2021003'],
                        'Date': ['2024-01-15', '2024-01-15', '2024-01-15'],
                        'Status': ['Present', 'Absent', 'Present']
                    })
                
                df.to_excel(filename, index=False)
                QMessageBox.information(self, "Success", "Template downloaded successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to download template: {str(e)}")
    
    def import_data(self):
        """Perform import"""
        if not hasattr(self, 'selected_file'):
            QMessageBox.warning(self, "Error", "Please select a file first!")
            return
        
        import_type = self.import_type.currentText()
        
        try:
            if import_type == "Students":
                result = self.importer.import_students(self.selected_file)
            elif import_type == "Grades":
                result = self.importer.import_grades(self.selected_file)
            else:
                result = self.importer.import_attendance(self.selected_file)
            
            self.importer.show_import_result(result, self)
            
            if result['success']:
                self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Import failed: {str(e)}")