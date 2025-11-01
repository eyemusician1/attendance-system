from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QMessageBox, QGroupBox
)
from attendance_system.database.db_manager import DBManager


class ConfigTab(QWidget):
    """Grading configuration tab"""
    
    def __init__(self, db: DBManager):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_config()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        section_title = QLabel("Grading Configuration")
        section_title.setStyleSheet("""
            font-size: 22px; 
            font-weight: 700; 
            color: #0f172a; 
            margin-bottom: 8px;
        """)
        layout.addWidget(section_title)
        
        description = QLabel("Configure the grading weights for each component. Total must equal 100%.")
        description.setStyleSheet("""
            QLabel {
                font-size: 14px; 
                color: #64748b; 
                margin-bottom: 16px;
            }
        """)
        layout.addWidget(description)
        
        # Config table
        self.config_table = QTableWidget()
        self.config_table.setColumnCount(2)
        self.config_table.setHorizontalHeaderLabels(["Component", "Weight (%)"])
        self.config_table.setColumnWidth(0, 300)
        self.config_table.setColumnWidth(1, 200)
        self.config_table.setAlternatingRowColors(True)
        self.config_table.setMaximumHeight(300)
        layout.addWidget(self.config_table)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        save_config_btn = QPushButton("Save Configuration")
        save_config_btn.clicked.connect(self.save_config)
        
        reset_config_btn = QPushButton("Reset to Default")
        reset_config_btn.setObjectName("secondaryButton")
        reset_config_btn.clicked.connect(self.reset_config)
        
        btn_layout.addWidget(save_config_btn)
        btn_layout.addWidget(reset_config_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Grade scale card
        scale_group = QGroupBox("Grade Point Scale")
        scale_layout = QVBoxLayout()
        scale_layout.setSpacing(12)
        
        scale_text = QLabel(
            "<b style='font-size: 15px;'>Grading Scale:</b><br><br>"
            "<span style='font-size: 14px; color: #475569; line-height: 2.2;'>"
            "100% = <b>1.00</b> | "
            "90% = <b>1.25</b> | "
            "85% = <b>1.75</b> | "
            "80% = <b>2.00</b><br>"
            "75% = <b>2.25</b> | "
            "70% = <b>2.50</b> | "
            "65% = <b>2.75</b> | "
            "60% = <b>3.00</b><br>"
            "Below 60% = <b style='color: #dc2626;'>5.00 (Failed)</b>"
            "</span>"
        )
        scale_text.setStyleSheet("padding: 16px;")
        scale_layout.addWidget(scale_text)
        scale_group.setLayout(scale_layout)
        layout.addWidget(scale_group)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def load_config(self):
        """Load configuration into table"""
        config = self.db.get_grading_config()
        self.config_table.setRowCount(len(config))
        for row, (component, weight) in enumerate(config):
            self.config_table.setItem(row, 0, QTableWidgetItem(component))
            weight_item = QTableWidgetItem(str(weight))
            self.config_table.setItem(row, 1, weight_item)
    
    def save_config(self):
        """Save configuration"""
        total_weight = 0
        updates = []
        
        for row in range(self.config_table.rowCount()):
            component = self.config_table.item(row, 0).text()
            try:
                weight = float(self.config_table.item(row, 1).text())
                total_weight += weight
                updates.append((component, weight))
            except ValueError:
                QMessageBox.warning(
                    self, "Error", f"Invalid weight value in row {row + 1}"
                )
                return
        
        if abs(total_weight - 100.0) > 0.01:
            QMessageBox.warning(
                self, "Validation Error", 
                f"Total weight must equal 100% (currently {total_weight:.1f}%)"
            )
            return
        
        try:
            for component, weight in updates:
                self.db.update_grading_config(component, weight)
            QMessageBox.information(self, "Success", "Grading configuration saved!")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def reset_config(self):
        """Reset to defaults"""
        try:
            self.db.reset_grading_config()
            self.load_config()
            QMessageBox.information(self, "Success", "Configuration reset to default!")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))