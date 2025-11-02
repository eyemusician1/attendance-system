"""
Student Tab - Modern design with ttkbootstrap
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tableview import Tableview
from tkinter import messagebox, filedialog
from datetime import datetime


class StudentTab(ttk.Frame):
    """Student management tab with attendance tracking"""
    
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        
        self.create_widgets()
        self.refresh_students()
    
    def create_widgets(self):
        """Create all widgets for the student tab"""
        # Main container with scrolling
        main_container = ScrolledFrame(self, autohide=True)
        main_container.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Section title
        title_label = ttk.Label(
            main_container,
            text="Student Management",
            style='SectionTitle.TLabel'
        )
        title_label.pack(anchor=W, pady=(0, 15))
        
        # Add student form
        self.create_add_form(main_container)
        
        # Student list
        self.create_student_list(main_container)
        
        # Action buttons
        self.create_action_buttons(main_container)
    
    def create_add_form(self, parent):
        """Create the add student form"""
        form_frame = ttk.Labelframe(
            parent,
            text="Add or Edit Student",
            padding=20,
            bootstyle="primary"
        )
        form_frame.pack(fill=X, pady=(0, 20))
        
        # Form grid
        form_grid = ttk.Frame(form_frame)
        form_grid.pack(fill=X)
        
        # Student ID
        ttk.Label(form_grid, text="Student ID:").grid(row=0, column=0, sticky=W, padx=(0, 10), pady=5)
        self.student_id_var = ttk.StringVar()
        self.student_id_entry = ttk.Entry(form_grid, textvariable=self.student_id_var, width=20)
        self.student_id_entry.grid(row=0, column=1, sticky=EW, padx=5, pady=5)
        
        # Full Name
        ttk.Label(form_grid, text="Full Name:").grid(row=0, column=2, sticky=W, padx=(20, 10), pady=5)
        self.student_name_var = ttk.StringVar()
        self.student_name_entry = ttk.Entry(form_grid, textvariable=self.student_name_var, width=30)
        self.student_name_entry.grid(row=0, column=3, sticky=EW, padx=5, pady=5)
        
        # Course
        ttk.Label(form_grid, text="Course:").grid(row=1, column=0, sticky=W, padx=(0, 10), pady=5)
        self.course_var = ttk.StringVar()
        self.course_entry = ttk.Entry(form_grid, textvariable=self.course_var, width=20)
        self.course_entry.grid(row=1, column=1, sticky=EW, padx=5, pady=5)
        
        # Email
        ttk.Label(form_grid, text="Email:").grid(row=1, column=2, sticky=W, padx=(20, 10), pady=5)
        self.email_var = ttk.StringVar()
        self.email_entry = ttk.Entry(form_grid, textvariable=self.email_var, width=30)
        self.email_entry.grid(row=1, column=3, sticky=EW, padx=5, pady=5)
        
        # Configure column weights
        form_grid.columnconfigure(1, weight=1)
        form_grid.columnconfigure(3, weight=2)
        
        # Add button
        add_btn = ttk.Button(
            form_frame,
            text="Add Student",
            command=self.add_student,
            bootstyle="success",
            width=20
        )
        add_btn.pack(pady=(15, 0))
    
    def create_student_list(self, parent):
        """Create the student list table"""
        list_frame = ttk.Labelframe(
            parent,
            text="Student List",
            padding=15,
            bootstyle="info"
        )
        list_frame.pack(fill=BOTH, expand=YES, pady=(0, 20))
        
        # Define columns
        columns = [
            {"text": "Student ID", "width": 120},
            {"text": "Name", "width": 200},
            {"text": "Course", "width": 150},
            {"text": "Email", "width": 250},
            {"text": "Attendance Rate", "width": 150}
        ]
        
        # Create table with empty rowdata
        self.students_table = Tableview(
            list_frame,
            coldata=columns,
            rowdata=[],  # Initialize with empty list
            searchable=True,
            bootstyle="primary",
            height=15,
            autofit=True
        )
        self.students_table.pack(fill=BOTH, expand=YES)
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=X, pady=(0, 10))
        
        # Left side buttons
        left_frame = ttk.Frame(btn_frame)
        left_frame.pack(side=LEFT)
        
        mark_btn = ttk.Button(
            left_frame,
            text="Mark Attendance",
            command=self.mark_attendance,
            bootstyle="primary",
            width=18
        )
        mark_btn.pack(side=LEFT, padx=(0, 10))
        
        refresh_btn = ttk.Button(
            left_frame,
            text="Refresh",
            command=self.refresh_students,
            bootstyle="secondary-outline",
            width=15
        )
        refresh_btn.pack(side=LEFT, padx=(0, 10))
        
        # Right side buttons
        right_frame = ttk.Frame(btn_frame)
        right_frame.pack(side=RIGHT)
        
        export_btn = ttk.Button(
            right_frame,
            text="Export to Excel",
            command=self.export_students,
            bootstyle="info-outline",
            width=18
        )
        export_btn.pack(side=LEFT, padx=(0, 10))
        
        import_btn = ttk.Button(
            right_frame,
            text="Import from Excel",
            command=self.import_students,
            bootstyle="info-outline",
            width=18
        )
        import_btn.pack(side=LEFT)
    
    def add_student(self):
        """Add a new student"""
        student_id = self.student_id_var.get().strip()
        name = self.student_name_var.get().strip()
        course = self.course_var.get().strip()
        email = self.email_var.get().strip()
        
        if not student_id or not name:
            messagebox.showwarning("Validation Error", "Student ID and Name are required!")
            return
        
        success = self.db.add_student(student_id, name, course, email)
        if success:
            messagebox.showinfo("Success", "Student added successfully!")
            # Clear form
            self.student_id_var.set("")
            self.student_name_var.set("")
            self.course_var.set("")
            self.email_var.set("")
            self.refresh_students()
        else:
            messagebox.showerror("Error", "Student ID already exists!")
    
    def refresh_students(self):
        """Refresh the student list"""
        students = self.db.get_students_with_attendance()
        
        # Clear existing data
        self.students_table.delete_rows()
        
        # Add new data
        for student in students:
            attendance_pct = 0
            if student[4] > 0:
                attendance_pct = (student[5] / student[4]) * 100
            
            row_data = [
                student[0],  # Student ID
                student[1],  # Name
                student[2] or "",  # Course
                student[3] or "",  # Email
                f"{attendance_pct:.1f}%"  # Attendance
            ]
            self.students_table.insert_row(END, row_data)
        
        self.students_table.load_table_data()
    
    def mark_attendance(self):
        """Mark attendance for all students"""
        students = self.db.get_all_students()
        
        if not students:
            messagebox.showwarning("Error", "No students found!")
            return
        
        # Create attendance dialog
        dialog = ttk.Toplevel(self.master)
        dialog.title(f"Mark Attendance - {datetime.now().strftime('%B %d, %Y')}")
        dialog.geometry("600x700")
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f'600x700+{x}+{y}')
        
        # Header
        header_frame = ttk.Frame(dialog, padding=20)
        header_frame.pack(fill=X)
        
        ttk.Label(
            header_frame,
            text="Select Present Students",
            font=('Segoe UI', 14, 'bold')
        ).pack(anchor=W)
        
        ttk.Label(
            header_frame,
            text="Students not checked will be marked as absent",
            foreground='gray'
        ).pack(anchor=W)
        
        # Scrollable student list
        scroll_frame = ScrolledFrame(dialog, autohide=True)
        scroll_frame.pack(fill=BOTH, expand=YES, padx=20, pady=(0, 20))
        
        checkboxes = {}
        for student_id, name, course, email in students:
            var = ttk.BooleanVar(value=True)
            cb = ttk.Checkbutton(
                scroll_frame,
                text=f"{name} ({student_id})",
                variable=var,
                bootstyle="success-round-toggle"
            )
            cb.pack(anchor=W, pady=5)
            checkboxes[student_id] = var
        
        # Buttons
        btn_frame = ttk.Frame(dialog, padding=20)
        btn_frame.pack(fill=X)
        
        def save_attendance():
            today = datetime.now().strftime("%Y-%m-%d")
            for student_id, var in checkboxes.items():
                status = "Present" if var.get() else "Absent"
                self.db.mark_attendance(student_id, today, status)
            messagebox.showinfo("Success", "Attendance saved successfully!")
            dialog.destroy()
            self.refresh_students()
        
        save_btn = ttk.Button(
            btn_frame,
            text="Save Attendance",
            command=save_attendance,
            bootstyle="success",
            width=20
        )
        save_btn.pack(side=LEFT, padx=(0, 10))
        
        cancel_btn = ttk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bootstyle="secondary",
            width=15
        )
        cancel_btn.pack(side=LEFT)
    
    def export_students(self):
        """Export students to Excel"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if filename:
            try:
                from attendance_system.utils.exports import export_students
                export_students(self.db, filename)
                messagebox.showinfo("Success", "Students exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def import_students(self):
        """Import students from Excel"""
        filename = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        if filename:
            try:
                from attendance_system.utils.imports import ExcelImporter
                importer = ExcelImporter(self.db)
                result = importer.import_students(filename)
                
                if result['success']:
                    messagebox.showinfo(
                        "Success",
                        f"Imported {result['imported']} students successfully!\n"
                        f"Skipped {result['skipped']} duplicates."
                    )
                    self.refresh_students()
                else:
                    messagebox.showerror("Error", result.get('error', 'Import failed'))
            except Exception as e:
                messagebox.showerror("Error", f"Import failed: {str(e)}")