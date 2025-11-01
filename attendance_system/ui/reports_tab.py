from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QColor
from attendance_system.database.db_manager import DBManager
from attendance_system.utils.calculations import generate_report
from attendance_system.utils.exports import export_report


class ReportsTab(QWidget):
    """Reports and analytics tab"""
    
    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        section_title = QLabel("Grade Reports & Analytics")
        section_title.setStyleSheet("""
            font-size: 22px; 
            font-weight: 700; 
            color: #0f172a; 
            margin-bottom: 8px;
        """)
        layout.addWidget(section_title)
        
        # Statistics display
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("""
            QLabel {
                padding: 24px;
                border-radius: 12px;
                background-color: white;
                border: 1px solid #e2e8f0;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.stats_label)
        
        # Title for grades table
        grades_label = QLabel("Final Grades Summary")
        grades_label.setStyleSheet("""
            font-size: 16px; 
            font-weight: 600; 
            color: #1e293b; 
            margin-top: 12px;
        """)
        layout.addWidget(grades_label)
        
        # Final grades table
        self.final_grades_table = QTableWidget()
        self.final_grades_table.setColumnCount(9)
        self.final_grades_table.setHorizontalHeaderLabels([
            "Student ID", "Name", "Attendance", "Quizzes", "Assignments", 
            "Midterm", "Final Exam", "Final Grade", "Letter"
        ])
        self.final_grades_table.horizontalHeader().setStretchLastSection(True)
        self.final_grades_table.setAlternatingRowColors(True)
        layout.addWidget(self.final_grades_table, 1)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        refresh_report_btn = QPushButton("Refresh Report")
        refresh_report_btn.clicked.connect(self.generate_report)
        
        export_report_btn = QPushButton("Export Report")
        export_report_btn.setObjectName("secondaryButton")
        export_report_btn.clicked.connect(self.export_to_excel)
        
        btn_layout.addWidget(refresh_report_btn)
        btn_layout.addWidget(export_report_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def generate_report(self):
        """Generate comprehensive report"""
        report_data = generate_report(self.db)
        
        self.final_grades_table.setRowCount(len(report_data))
        
        passing_count = 0
        total_avg = 0
        
        for row, data in enumerate(report_data):
            self.final_grades_table.setItem(row, 0, QTableWidgetItem(data['student_id']))
            self.final_grades_table.setItem(row, 1, QTableWidgetItem(data['name']))
            
            col = 2
            for component in ['Attendance', 'Quizzes', 'Assignments', 'Midterm', 'Final Exam']:
                value = data['grades'].get(component, 0)
                item = QTableWidgetItem(f"{value:.1f}%")
                self.final_grades_table.setItem(row, col, item)
                col += 1
            
            final_item = QTableWidgetItem(f"{data['final']:.2f}%")
            letter_item = QTableWidgetItem(str(data['letter']))
            
            if data['final'] >= 90:
                color = QColor(220, 252, 231)
            elif data['final'] >= 80:
                color = QColor(254, 249, 195)
            elif data['final'] >= 70:
                color = QColor(255, 237, 213)
            else:
                color = QColor(254, 226, 226)
            
            final_item.setBackground(color)
            letter_item.setBackground(color)
            
            self.final_grades_table.setItem(row, 7, final_item)
            self.final_grades_table.setItem(row, 8, letter_item)
            
            if data['final'] >= 60:
                passing_count += 1
            total_avg += data['final']
        
        # Update statistics
        if len(report_data) > 0:
            avg_grade = total_avg / len(report_data)
            pass_rate = (passing_count / len(report_data)) * 100
            
            stats_text = f"""
            <div style="line-height: 2.0;">
            <b style="font-size: 16px;">Class Statistics</b><br><br>
            <span style="color: #64748b;">
            <b>Total Students:</b> {len(report_data)} | 
            <b>Average Grade:</b> {avg_grade:.2f}% | 
            <b>Pass Rate:</b> {pass_rate:.1f}% ({passing_count}/{len(report_data)})<br><br>
            </span>
            <span style="color: #475569;">
            <b>Grade Distribution:</b><br>
            A's: <b>{sum(1 for d in report_data if d['letter'] == 'A')}</b> | 
            B's: <b>{sum(1 for d in report_data if d['letter'] == 'B')}</b> | 
            C's: <b>{sum(1 for d in report_data if d['letter'] == 'C')}</b> | 
            D's: <b>{sum(1 for d in report_data if d['letter'] == 'D')}</b> | 
            F's: <b>{sum(1 for d in report_data if d['letter'] == 'F')}</b>
            </span>
            </div>
            """
            self.stats_label.setText(stats_text)
        else:
            self.stats_label.setText(
                "<span style='color: #64748b;'>No student data available</span>"
            )
    
    def export_to_excel(self):
        """Export report to Excel"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Report", "", "Excel Files (*.xlsx)"
        )
        if filename:
            try:
                export_report(self.db, filename)
                QMessageBox.information(self, "Success", "Report exported successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Export failed: {str(e)}")