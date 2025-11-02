"""
Grades Tab - Modern design with ttkbootstrap
Enhanced with auto-fill Student ID on row selection
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tableview import Tableview
from tkinter import messagebox, filedialog
from datetime import datetime


class GradesTab(ttk.Frame):
    """Grades management tab"""

    def __init__(self, parent, db, calculate_callback):
        super().__init__(parent)
        self.db = db
        self.calculate_callback = calculate_callback

        self.create_widgets()
        self.refresh_grades()

    def create_widgets(self):
        """Create all widgets for the grades tab"""
        # Main container with scrolling
        main_container = ScrolledFrame(self, autohide=True)
        main_container.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Section title
        title_label = ttk.Label(
            main_container,
            text="Grade Management",
            style='SectionTitle.TLabel'
        )
        title_label.pack(anchor=W, pady=(0, 15))

        # Add grade form
        self.create_add_form(main_container)

        # Grades list
        self.create_grades_list(main_container)

        # Action buttons
        self.create_action_buttons(main_container)

    def create_add_form(self, parent):
        """Create the add grade form"""
        form_frame = ttk.Labelframe(
            parent,
            text="Add Grade or Score",
            padding=20,
            bootstyle="primary"
        )
        form_frame.pack(fill=X, pady=(0, 20))

        # Info label
        info_label = ttk.Label(
            form_frame,
            text="💡 Tip: Click on any grade record below to auto-fill the Student ID",
            foreground='gray',
            font=('Segoe UI', 9, 'italic')
        )
        info_label.pack(anchor=W, pady=(0, 10))

        # Form grid
        form_grid = ttk.Frame(form_frame)
        form_grid.pack(fill=X)

        # Row 1
        ttk.Label(form_grid, text="Student ID:").grid(row=0, column=0, sticky=W, padx=(0, 10), pady=5)
        self.student_id_var = ttk.StringVar()
        self.student_id_entry = ttk.Entry(form_grid, textvariable=self.student_id_var, width=18)
        self.student_id_entry.grid(row=0, column=1, sticky=EW, padx=5, pady=5)

        ttk.Label(form_grid, text="Assessment Type:").grid(row=0, column=2, sticky=W, padx=(20, 10), pady=5)
        self.assessment_type_var = ttk.StringVar()
        self.assessment_type_combo = ttk.Combobox(
            form_grid,
            textvariable=self.assessment_type_var,
            values=["Attendance", "Quizzes", "Assignments", "Midterm", "Final Exam"],
            state="readonly",
            width=18
        )
        self.assessment_type_combo.current(0)
        self.assessment_type_combo.grid(row=0, column=3, sticky=EW, padx=5, pady=5)

        ttk.Label(form_grid, text="Assessment Name:").grid(row=0, column=4, sticky=W, padx=(20, 10), pady=5)
        self.assessment_name_var = ttk.StringVar()
        self.assessment_name_entry = ttk.Entry(form_grid, textvariable=self.assessment_name_var, width=25)
        self.assessment_name_entry.grid(row=0, column=5, sticky=EW, padx=5, pady=5)

        # Row 2
        ttk.Label(form_grid, text="Score:").grid(row=1, column=0, sticky=W, padx=(0, 10), pady=5)
        self.score_var = ttk.DoubleVar(value=0)
        self.score_spinbox = ttk.Spinbox(form_grid, from_=0, to=1000, textvariable=self.score_var, width=18)
        self.score_spinbox.grid(row=1, column=1, sticky=EW, padx=5, pady=5)

        ttk.Label(form_grid, text="Max Score:").grid(row=1, column=2, sticky=W, padx=(20, 10), pady=5)
        self.max_score_var = ttk.DoubleVar(value=100)
        self.max_score_spinbox = ttk.Spinbox(form_grid, from_=0, to=1000, textvariable=self.max_score_var, width=18)
        self.max_score_spinbox.grid(row=1, column=3, sticky=EW, padx=5, pady=5)

        # Configure column weights
        form_grid.columnconfigure(1, weight=1)
        form_grid.columnconfigure(3, weight=1)
        form_grid.columnconfigure(5, weight=2)

        # Buttons frame
        btn_container = ttk.Frame(form_frame)
        btn_container.pack(pady=(15, 0))

        add_btn = ttk.Button(
            btn_container,
            text="Add Grade",
            command=self.add_grade,
            bootstyle="success",
            width=20
        )
        add_btn.pack(side=LEFT, padx=(0, 10))

        clear_btn = ttk.Button(
            btn_container,
            text="Clear Form",
            command=self.clear_form,
            bootstyle="secondary-outline",
            width=15
        )
        clear_btn.pack(side=LEFT)

    def create_grades_list(self, parent):
        """Create the grades list table"""
        list_frame = ttk.Labelframe(
            parent,
            text="Grade Records - Click a row to auto-fill Student ID above",
            padding=15,
            bootstyle="info"
        )
        list_frame.pack(fill=BOTH, expand=YES, pady=(0, 20))

        # Define columns
        columns = [
            {"text": "Student ID", "width": 100},
            {"text": "Name", "width": 150},
            {"text": "Type", "width": 120},
            {"text": "Assessment", "width": 180},
            {"text": "Score", "width": 80},
            {"text": "Max", "width": 80},
            {"text": "Percentage", "width": 100},
            {"text": "Date", "width": 100}
        ]

        # Create table with empty rowdata
        self.grades_table = Tableview(
            list_frame,
            coldata=columns,
            rowdata=[],  # Initialize with empty list
            searchable=True,
            bootstyle="primary",
            height=15,
            autofit=True
        )
        self.grades_table.pack(fill=BOTH, expand=YES)

        # Bind row selection event
        self.grades_table.view.bind('<<TreeviewSelect>>', self.on_row_select)

    def create_action_buttons(self, parent):
        """Create action buttons"""
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=X, pady=(0, 10))

        # Left side buttons
        left_frame = ttk.Frame(btn_frame)
        left_frame.pack(side=LEFT)

        calc_btn = ttk.Button(
            left_frame,
            text="Calculate Final Grades",
            command=self.calculate_grades,
            bootstyle="primary",
            width=22
        )
        calc_btn.pack(side=LEFT, padx=(0, 10))

        refresh_btn = ttk.Button(
            left_frame,
            text="Refresh",
            command=self.refresh_grades,
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
            command=self.export_grades,
            bootstyle="info-outline",
            width=18
        )
        export_btn.pack(side=LEFT, padx=(0, 10))

        import_btn = ttk.Button(
            right_frame,
            text="Import from Excel",
            command=self.import_grades,
            bootstyle="info-outline",
            width=18
        )
        import_btn.pack(side=LEFT)

    def on_row_select(self, event):
        """Handle row selection - auto-fill Student ID"""
        try:
            # Get selected item
            selected_items = self.grades_table.view.selection()
            if selected_items:
                # Get the first selected item
                item = selected_items[0]
                # Get the values of the selected row
                values = self.grades_table.view.item(item)['values']

                if values:
                    # Extract Student ID (first column)
                    student_id = values[0]
                    # Auto-fill the Student ID field
                    self.student_id_var.set(student_id)

                    # Optional: Also fill assessment type if you want
                    assessment_type = values[2]  # Type column
                    try:
                        # Try to set the assessment type combo if it matches
                        combo_values = self.assessment_type_combo['values']
                        if assessment_type in combo_values:
                            self.assessment_type_combo.set(assessment_type)
                    except:
                        pass

                    # Highlight the Student ID entry briefly to show it was filled
                    self.student_id_entry.config(bootstyle="success")
                    self.after(500, lambda: self.student_id_entry.config(bootstyle=""))

        except Exception as e:
            # Silent fail - don't interrupt user experience
            pass

    def add_grade(self):
        """Add a new grade"""
        student_id = self.student_id_var.get().strip()
        assessment_type = self.assessment_type_var.get()
        assessment_name = self.assessment_name_var.get().strip()
        score = self.score_var.get()
        max_score = self.max_score_var.get()

        if not student_id or not assessment_name:
            messagebox.showwarning("Validation Error", "Student ID and Assessment Name are required!")
            return

        if max_score == 0:
            messagebox.showwarning("Validation Error", "Max score cannot be zero!")
            return

        if not self.db.get_student(student_id):
            messagebox.showerror("Error", "Student ID not found!")
            return

        try:
            date = datetime.now().strftime("%Y-%m-%d")
            self.db.add_grade(student_id, assessment_type, assessment_name, score, max_score, date)
            messagebox.showinfo("Success", "Grade added successfully!")

            # Clear form
            self.clear_form()

            self.refresh_grades()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        """Clear the form fields"""
        self.student_id_var.set("")
        self.assessment_name_var.set("")
        self.score_var.set(0)
        self.max_score_var.set(100)
        self.assessment_type_combo.current(0)
    
    def refresh_grades(self):
        """Refresh the grades list"""
        grades = self.db.get_all_grades()
        
        # Clear existing data
        self.grades_table.delete_rows()
        
        # Add new data
        for grade in grades:
            percentage = (grade[4] / grade[5]) * 100 if grade[5] > 0 else 0
            
            row_data = [
                grade[0],  # Student ID
                grade[1],  # Name
                grade[2],  # Type
                grade[3],  # Assessment
                f"{grade[4]:.1f}",  # Score
                f"{grade[5]:.1f}",  # Max
                f"{percentage:.1f}%",  # Percentage
                grade[6]  # Date
            ]
            self.grades_table.insert_row(END, row_data)
        
        self.grades_table.load_table_data()
    
    def calculate_grades(self):
        """Calculate final grades"""
        if self.calculate_callback:
            self.calculate_callback()
    
    def export_grades(self):
        """Export grades to Excel"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if filename:
            try:
                from attendance_system.utils.exports import export_grades
                export_grades(self.db, filename)
                messagebox.showinfo("Success", "Grades exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def import_grades(self):
        """Import grades from Excel"""
        filename = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        if filename:
            try:
                from attendance_system.utils.imports import ExcelImporter
                importer = ExcelImporter(self.db)
                result = importer.import_grades(filename)
                
                if result['success']:
                    messagebox.showinfo(
                        "Success",
                        f"Imported {result['imported']} grades successfully!\n"
                        f"Skipped {result['skipped']} records."
                    )
                    self.refresh_grades()
                else:
                    messagebox.showerror("Error", result.get('error', 'Import failed'))
            except Exception as e:
                messagebox.showerror("Error", f"Import failed: {str(e)}")