"""
Professional theme styles for PyQt5 application
Clean, modern design without icons
"""

PROFESSIONAL_LIGHT = """
/* ===========================
   PROFESSIONAL CLEAN THEME
   =========================== */

QMainWindow {
    background-color: #f5f7fa;
}

QWidget {
    font-family: 'Segoe UI', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 14px;
    color: #2c3e50;
}

/* ===========================
   TAB WIDGET
   =========================== */
QTabWidget::pane {
    border: none;
    background-color: transparent;
}

QTabBar {
    background-color: transparent;
    border-bottom: 1px solid #dce1e8;
}

QTabBar::tab {
    background-color: transparent;
    color: #7f8c9a;
    padding: 16px 28px;
    margin-right: 4px;
    border: none;
    border-bottom: 3px solid transparent;
    font-weight: 500;
    font-size: 14px;
}

QTabBar::tab:hover:!selected {
    color: #4a5568;
    background-color: #f8f9fb;
}

QTabBar::tab:selected {
    color: #2563eb;
    border-bottom-color: #2563eb;
    font-weight: 600;
    background-color: transparent;
}

/* ===========================
   TABLES
   =========================== */
QTableWidget {
    background-color: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    gridline-color: #f1f5f9;
    selection-background-color: #e0f2fe;
    selection-color: #0c4a6e;
    padding: 4px;
}

QTableWidget::item {
    padding: 14px 16px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #e0f2fe;
}

QHeaderView::section {
    background-color: #f8fafc;
    color: #64748b;
    padding: 14px 16px;
    border: none;
    border-bottom: 2px solid #e2e8f0;
    font-weight: 600;
    font-size: 13px;
}

QHeaderView::section:hover {
    background-color: #f1f5f9;
}

/* ===========================
   BUTTONS
   =========================== */
QPushButton {
    background-color: #2563eb;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 14px;
    min-height: 40px;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e40af;
}

QPushButton:disabled {
    background-color: #cbd5e1;
    color: #94a3b8;
}

QPushButton#primaryButton {
    background-color: #059669;
}

QPushButton#primaryButton:hover {
    background-color: #047857;
}

QPushButton#dangerButton {
    background-color: #dc2626;
}

QPushButton#dangerButton:hover {
    background-color: #b91c1c;
}

QPushButton#secondaryButton {
    background-color: #f1f5f9;
    color: #475569;
    border: 1px solid #e2e8f0;
}

QPushButton#secondaryButton:hover {
    background-color: #e2e8f0;
    border-color: #cbd5e1;
}

/* ===========================
   INPUT FIELDS
   =========================== */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit {
    padding: 12px 16px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    background-color: white;
    color: #1e293b;
    selection-background-color: #bfdbfe;
    font-size: 14px;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QTextEdit:focus {
    border: 2px solid #2563eb;
    padding: 11px 15px;
}

QLineEdit::placeholder {
    color: #94a3b8;
}

QComboBox {
    padding: 11px 16px;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #64748b;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    background-color: white;
    selection-background-color: #e0f2fe;
    selection-color: #0c4a6e;
    padding: 4px;
    outline: none;
}

/* ===========================
   GROUP BOX
   =========================== */
QGroupBox {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    margin-top: 24px;
    padding: 20px;
    background-color: white;
    font-weight: 600;
    color: #1e293b;
    font-size: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 12px;
    color: #1e293b;
    background-color: white;
    font-weight: 600;
}

/* ===========================
   LABELS
   =========================== */
QLabel#titleLabel {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.5px;
}

QLabel#subtitleLabel {
    font-size: 15px;
    font-weight: 400;
    color: #64748b;
}

/* ===========================
   SCROLL BARS
   =========================== */
QScrollBar:vertical {
    border: none;
    background-color: #f8fafc;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #cbd5e1;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94a3b8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #f8fafc;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #cbd5e1;
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #94a3b8;
}

/* ===========================
   CHECKBOX
   =========================== */
QCheckBox {
    spacing: 12px;
    color: #1e293b;
    font-size: 14px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #cbd5e1;
    border-radius: 6px;
    background-color: white;
}

QCheckBox::indicator:hover {
    border-color: #2563eb;
}

QCheckBox::indicator:checked {
    background-color: #2563eb;
    border-color: #2563eb;
    image: none;
}

/* ===========================
   DIALOG
   =========================== */
QDialog {
    background-color: #f5f7fa;
}

QMessageBox {
    background-color: white;
}

QMessageBox QLabel {
    color: #1e293b;
    font-size: 14px;
}
"""

PROFESSIONAL_DARK = """
/* ===========================
   PROFESSIONAL DARK THEME
   =========================== */

QMainWindow {
    background-color: #0a0e1a;
}

QWidget {
    font-family: 'Segoe UI', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 14px;
    color: #e2e8f0;
    background-color: #0a0e1a;
}

QTabWidget::pane {
    border: none;
    background-color: transparent;
}

QTabBar {
    background-color: transparent;
    border-bottom: 1px solid #1e293b;
}

QTabBar::tab {
    background-color: transparent;
    color: #94a3b8;
    padding: 16px 28px;
    margin-right: 4px;
    border: none;
    border-bottom: 3px solid transparent;
    font-weight: 500;
    font-size: 14px;
}

QTabBar::tab:hover:!selected {
    color: #cbd5e1;
    background-color: #151d2d;
}

QTabBar::tab:selected {
    color: #60a5fa;
    border-bottom-color: #60a5fa;
    font-weight: 600;
}

QTableWidget {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    gridline-color: #1e293b;
    selection-background-color: #1e3a8a;
    selection-color: #e0f2fe;
}

QTableWidget::item {
    padding: 14px 16px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #1e3a8a;
}

QHeaderView::section {
    background-color: #0f172a;
    color: #94a3b8;
    padding: 14px 16px;
    border: none;
    border-bottom: 2px solid #1e293b;
    font-weight: 600;
    font-size: 13px;
}

QHeaderView::section:hover {
    background-color: #1e293b;
}

QPushButton {
    background-color: #3b82f6;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 14px;
    min-height: 40px;
}

QPushButton:hover {
    background-color: #2563eb;
}

QPushButton:pressed {
    background-color: #1d4ed8;
}

QPushButton:disabled {
    background-color: #334155;
    color: #64748b;
}

QPushButton#primaryButton {
    background-color: #059669;
}

QPushButton#primaryButton:hover {
    background-color: #047857;
}

QPushButton#dangerButton {
    background-color: #dc2626;
}

QPushButton#dangerButton:hover {
    background-color: #b91c1c;
}

QPushButton#secondaryButton {
    background-color: #1e293b;
    color: #cbd5e1;
    border: 1px solid #334155;
}

QPushButton#secondaryButton:hover {
    background-color: #334155;
}

QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit {
    padding: 12px 16px;
    border: 1px solid #334155;
    border-radius: 8px;
    background-color: #0f172a;
    color: #e2e8f0;
    selection-background-color: #1e3a8a;
    font-size: 14px;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QTextEdit:focus {
    border: 2px solid #3b82f6;
    padding: 11px 15px;
}

QLineEdit::placeholder {
    color: #64748b;
}

QComboBox::down-arrow {
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #94a3b8;
}

QComboBox QAbstractItemView {
    border: 1px solid #334155;
    border-radius: 8px;
    background-color: #0f172a;
    selection-background-color: #1e3a8a;
    color: #e2e8f0;
}

QGroupBox {
    border: 1px solid #1e293b;
    border-radius: 12px;
    margin-top: 24px;
    padding: 20px;
    background-color: #0f172a;
    font-weight: 600;
    color: #e2e8f0;
}

QGroupBox::title {
    color: #e2e8f0;
    background-color: #0f172a;
}

QLabel#titleLabel {
    font-size: 28px;
    font-weight: 700;
    color: #f1f5f9;
}

QLabel#subtitleLabel {
    font-size: 15px;
    color: #94a3b8;
}

QScrollBar:vertical {
    background-color: #0f172a;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #334155;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #475569;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 2px solid #334155;
    border-radius: 6px;
    background-color: #0f172a;
}

QCheckBox::indicator:hover {
    border-color: #3b82f6;
}

QCheckBox::indicator:checked {
    background-color: #3b82f6;
    border-color: #3b82f6;
}

QDialog {
    background-color: #0a0e1a;
}

QMessageBox {
    background-color: #0f172a;
}
"""