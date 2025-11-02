"""
Main Application Window using ttkbootstrap
Modern, professional student management system
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

from attendance_system.database.db_manager import DBManager
from attendance_system.ui_tkinter.student_tab import StudentTab
from attendance_system.ui_tkinter.grades_tab import GradesTab
from attendance_system.ui_tkinter.config_reports import ConfigTab, ReportsTab


class MainApplication(ttk.Window):
    """Main application window with modern ttkbootstrap design"""
    
    def __init__(self):
        # Initialize with a modern theme
        super().__init__(themename="cosmo")  # cosmo, flatly, litera, minty, pulse, etc.
        
        self.title("Student Management System")
        self.geometry("1400x900")
        
        # Initialize database
        self.db = DBManager()
        
        # Configure window
        self.setup_styles()
        self.create_header()
        self.create_main_content()
        
        # Center window
        self.center_window()
        
        # Protocol for closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Setup custom styles for the application"""
        style = ttk.Style()
        
        # Configure custom button styles
        style.configure('Header.TLabel', font=('Segoe UI', 24, 'bold'))
        style.configure('Subtitle.TLabel', font=('Segoe UI', 11), foreground='gray')
        style.configure('SectionTitle.TLabel', font=('Segoe UI', 18, 'bold'))
        style.configure('CardTitle.TLabel', font=('Segoe UI', 13, 'bold'))
        
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_header(self):
        """Create the application header"""
        header_frame = ttk.Frame(self, bootstyle="light")
        header_frame.pack(fill=X, padx=30, pady=(20, 10))
        
        # Left side - Title and subtitle
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=LEFT, fill=BOTH, expand=YES)
        
        title_label = ttk.Label(
            title_frame,
            text="Student Management System",
            style='Header.TLabel'
        )
        title_label.pack(anchor=W)
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Manage attendance, grades, and student records efficiently",
            style='Subtitle.TLabel'
        )
        subtitle_label.pack(anchor=W)
        
        # Right side - Theme toggle
        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=RIGHT)
        
        self.theme_btn = ttk.Button(
            btn_frame,
            text="Switch Theme",
            command=self.toggle_theme,
            bootstyle="secondary-outline",
            width=15
        )
        self.theme_btn.pack(pady=5)
        
        # Separator
        separator = ttk.Separator(self, orient=HORIZONTAL)
        separator.pack(fill=X, padx=30, pady=10)
    
    def create_main_content(self):
        """Create the main content area with tabs"""
        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill=BOTH, expand=YES, padx=30, pady=(0, 20))
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(main_container, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=YES)
        
        # Create tabs
        self.student_tab = StudentTab(self.notebook, self.db)
        self.grades_tab = GradesTab(self.notebook, self.db, self.calculate_final_grades)
        self.config_tab = ConfigTab(self.notebook, self.db)
        self.reports_tab = ReportsTab(self.notebook, self.db)
        
        # Add tabs to notebook
        self.notebook.add(self.student_tab, text="  Students  ")
        self.notebook.add(self.grades_tab, text="  Grades  ")
        self.notebook.add(self.config_tab, text="  Settings  ")
        self.notebook.add(self.reports_tab, text="  Reports  ")
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_theme = self.style.theme.name
        
        # List of available themes
        themes = ['cosmo', 'flatly', 'litera', 'minty', 'pulse', 
                  'solar', 'superhero', 'darkly', 'cyborg', 'vapor']
        
        # Rotate through themes
        try:
            current_index = themes.index(current_theme)
            next_index = (current_index + 1) % len(themes)
            new_theme = themes[next_index]
        except ValueError:
            new_theme = 'cosmo'
        
        self.style.theme_use(new_theme)
    
    def calculate_final_grades(self):
        """Calculate final grades and switch to reports tab"""
        self.reports_tab.generate_report()
        self.notebook.select(3)  # Switch to reports tab
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.db.close()
            self.quit()
            self.destroy()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()