"""
Config and Reports Tabs - Modern design with ttkbootstrap
Enhanced with editable weight configuration
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.tableview import Tableview
from tkinter import messagebox, filedialog


class ConfigTab(ttk.Frame):
    """Grading configuration tab with editable weights"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.weight_entries = {}  # Store entry widgets for each component

        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        """Create all widgets for the config tab"""
        # Main container with scrolling
        main_container = ScrolledFrame(self, autohide=True)
        main_container.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Section title
        title_label = ttk.Label(
            main_container,
            text="Grading Configuration",
            style='SectionTitle.TLabel'
        )
        title_label.pack(anchor=W, pady=(0, 5))

        subtitle_label = ttk.Label(
            main_container,
            text="Configure the grading weights for each component. Total must equal 100%.",
            foreground='gray'
        )
        subtitle_label.pack(anchor=W, pady=(0, 20))

        # Config table frame - Using custom grid instead of Tableview
        table_frame = ttk.Labelframe(
            main_container,
            text="Component Weights",
            padding=20,
            bootstyle="primary"
        )
        table_frame.pack(fill=BOTH, expand=YES, pady=(0, 20))

        # Create custom editable table
        self.create_editable_table(table_frame)

        # Total weight display
        self.total_frame = ttk.Frame(table_frame)
        self.total_frame.pack(fill=X, pady=(10, 0))

        ttk.Label(
            self.total_frame,
            text="Total Weight:",
            font=('Segoe UI', 11, 'bold')
        ).pack(side=LEFT, padx=(0, 10))

        self.total_label = ttk.Label(
            self.total_frame,
            text="0.0%",
            font=('Segoe UI', 11, 'bold'),
            foreground='red'
        )
        self.total_label.pack(side=LEFT)

        # Add component form
        add_frame = ttk.Labelframe(
            main_container,
            text="Add New Component",
            padding=15,
            bootstyle="success"
        )
        add_frame.pack(fill=X, pady=(0, 20))

        form_grid = ttk.Frame(add_frame)
        form_grid.pack(fill=X)

        ttk.Label(form_grid, text="Component Name:").grid(row=0, column=0, sticky=W, padx=(0, 10), pady=5)
        self.new_component_var = ttk.StringVar()
        self.new_component_entry = ttk.Entry(form_grid, textvariable=self.new_component_var, width=25)
        self.new_component_entry.grid(row=0, column=1, sticky=EW, padx=5, pady=5)

        ttk.Label(form_grid, text="Weight (%):").grid(row=0, column=2, sticky=W, padx=(20, 10), pady=5)
        self.new_weight_var = ttk.DoubleVar(value=0)
        self.new_weight_entry = ttk.Entry(form_grid, textvariable=self.new_weight_var, width=15)
        self.new_weight_entry.grid(row=0, column=3, sticky=EW, padx=5, pady=5)

        form_grid.columnconfigure(1, weight=1)

        add_component_btn = ttk.Button(
            add_frame,
            text="Add Component",
            command=self.add_component,
            bootstyle="success-outline",
            width=18
        )
        add_component_btn.pack(pady=(10, 0))

        # Buttons
        btn_frame = ttk.Frame(main_container)
        btn_frame.pack(fill=X, pady=(0, 20))

        save_btn = ttk.Button(
            btn_frame,
            text="Save Configuration",
            command=self.save_config,
            bootstyle="success",
            width=20
        )
        save_btn.pack(side=LEFT, padx=(0, 10))

        reset_btn = ttk.Button(
            btn_frame,
            text="Reset to Default",
            command=self.reset_config,
            bootstyle="secondary-outline",
            width=18
        )
        reset_btn.pack(side=LEFT)

        # Grade scale info
        scale_frame = ttk.Labelframe(
            main_container,
            text="Grade Point Scale",
            padding=20,
            bootstyle="info"
        )
        scale_frame.pack(fill=X)

        scale_text = ttk.Label(
            scale_frame,
            text=(
                "Grading Scale:\n\n"
                "100% = 1.00  |  90% = 1.25  |  85% = 1.75  |  80% = 2.00\n"
                "75% = 2.25   |  70% = 2.50  |  65% = 2.75  |  60% = 3.00\n"
                "Below 60% = 5.00 (Failed)"
            ),
            font=('Segoe UI', 11)
        )
        scale_text.pack()

    def create_editable_table(self, parent):
        """Create custom editable table with grid"""
        # Table container with border
        table_container = ttk.Frame(parent, bootstyle="info")
        table_container.pack(fill=BOTH, expand=YES)

        # Header row
        header_frame = ttk.Frame(table_container, bootstyle="primary")
        header_frame.pack(fill=X)

        ttk.Label(
            header_frame,
            text="Component",
            font=('Segoe UI', 11, 'bold'),
            bootstyle="inverse-primary",
            width=25,
            padding=10
        ).pack(side=LEFT, fill=X, expand=YES)

        ttk.Label(
            header_frame,
            text="Weight (%)",
            font=('Segoe UI', 11, 'bold'),
            bootstyle="inverse-primary",
            width=15,
            padding=10
        ).pack(side=LEFT, fill=X, expand=YES)

        ttk.Label(
            header_frame,
            text="Actions",
            font=('Segoe UI', 11, 'bold'),
            bootstyle="inverse-primary",
            width=10,
            padding=10
        ).pack(side=LEFT)

        # Data rows container
        self.data_container = ttk.Frame(table_container)
        self.data_container.pack(fill=BOTH, expand=YES)

    def load_config(self):
        """Load configuration into editable table"""
        # Clear existing entries
        for widget in self.data_container.winfo_children():
            widget.destroy()
        self.weight_entries.clear()

        config = self.db.get_grading_config()

        # Create row for each component
        for idx, (component, weight) in enumerate(config):
            self.create_component_row(component, weight)

        # Update total display
        self.update_total()

    def create_component_row(self, component, weight):
        """Create a single component row with delete button"""
        row_frame = ttk.Frame(self.data_container)
        row_frame.pack(fill=X, pady=1)

        # Component label
        ttk.Label(
            row_frame,
            text=component,
            font=('Segoe UI', 10),
            width=25,
            padding=(10, 8)
        ).pack(side=LEFT, fill=X, expand=YES)

        # Weight entry
        weight_var = ttk.DoubleVar(value=weight)
        weight_entry = ttk.Entry(
            row_frame,
            textvariable=weight_var,
            font=('Segoe UI', 10),
            width=15,
            justify=CENTER
        )
        weight_entry.pack(side=LEFT, fill=X, expand=YES, padx=10, pady=5)

        # Bind to update total on change
        weight_var.trace_add('write', lambda *args: self.update_total())

        # Delete button
        delete_btn = ttk.Button(
            row_frame,
            text="Delete",
            command=lambda c=component: self.delete_component(c),
            bootstyle="danger-outline",
            width=8
        )
        delete_btn.pack(side=LEFT, padx=5)

        self.weight_entries[component] = weight_var

    def update_total(self):
        """Update the total weight display"""
        total = 0.0
        try:
            for weight_var in self.weight_entries.values():
                total += weight_var.get()
        except:
            pass

        self.total_label.config(text=f"{total:.1f}%")

        # Color code based on validity
        if abs(total - 100.0) < 0.01:
            self.total_label.config(foreground='green')
        else:
            self.total_label.config(foreground='red')

    def add_component(self):
        """Add a new grading component"""
        component_name = self.new_component_var.get().strip()
        weight = self.new_weight_var.get()

        if not component_name:
            messagebox.showwarning("Validation Error", "Component name is required!")
            return

        if component_name in self.weight_entries:
            messagebox.showerror("Error", "Component already exists!")
            return

        if weight < 0:
            messagebox.showerror("Error", "Weight cannot be negative!")
            return

        try:
            # Add to database
            self.db.add_grading_component(component_name, weight)

            # Add to UI
            self.create_component_row(component_name, weight)

            # Clear form
            self.new_component_var.set("")
            self.new_weight_var.set(0)

            # Update total
            self.update_total()

            messagebox.showinfo("Success", f"Component '{component_name}' added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add component: {str(e)}")

    def delete_component(self, component):
        """Delete a grading component"""
        # Don't allow deletion of default components
        default_components = ["Attendance", "Quizzes", "Assignments", "Midterm", "Final Exam"]
        if component in default_components:
            messagebox.showwarning(
                "Cannot Delete",
                "Default components cannot be deleted. You can set their weight to 0 if not needed."
            )
            return

        if messagebox.askyesno("Confirm Delete", f"Delete component '{component}'?"):
            try:
                self.db.delete_grading_component(component)
                self.load_config()
                messagebox.showinfo("Success", f"Component '{component}' deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete component: {str(e)}")

    def save_config(self):
        """Save configuration"""
        total_weight = 0
        updates = []

        for component, weight_var in self.weight_entries.items():
            try:
                weight = weight_var.get()
                if weight < 0:
                    messagebox.showerror("Error", f"Weight for {component} cannot be negative")
                    return
                total_weight += weight
                updates.append((component, weight))
            except Exception as e:
                messagebox.showerror("Error", f"Invalid weight value for {component}")
                return

        if abs(total_weight - 100.0) > 0.01:
            messagebox.showwarning(
                "Validation Error",
                f"Total weight must equal 100% (currently {total_weight:.1f}%)"
            )
            return

        try:
            for component, weight in updates:
                self.db.update_grading_config(component, weight)
            messagebox.showinfo("Success", "Grading configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_config(self):
        """Reset to defaults"""
        if messagebox.askyesno("Confirm Reset", "Reset configuration to default values?"):
            try:
                self.db.reset_grading_config()
                self.load_config()
                messagebox.showinfo("Success", "Configuration reset to default!")
            except Exception as e:
                messagebox.showerror("Error", str(e))


class ReportsTab(ttk.Frame):
    """Reports and analytics tab"""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db

        self.create_widgets()

    def create_widgets(self):
        """Create all widgets for the reports tab"""
        # Main container with scrolling
        main_container = ScrolledFrame(self, autohide=True)
        main_container.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Section title
        title_label = ttk.Label(
            main_container,
            text="Grade Reports & Analytics",
            style='SectionTitle.TLabel'
        )
        title_label.pack(anchor=W, pady=(0, 15))

        # Statistics frame
        self.stats_frame = ttk.Labelframe(
            main_container,
            text="Class Statistics",
            padding=20,
            bootstyle="success"
        )
        self.stats_frame.pack(fill=X, pady=(0, 20))

        self.stats_label = ttk.Label(
            self.stats_frame,
            text="Click 'Refresh Report' to generate statistics",
            font=('Segoe UI', 11),
            foreground='gray'
        )
        self.stats_label.pack()

        # Grades table frame
        table_frame = ttk.Labelframe(
            main_container,
            text="Final Grades Summary",
            padding=15,
            bootstyle="info"
        )
        table_frame.pack(fill=BOTH, expand=YES, pady=(0, 20))

        # Define columns
        columns = [
            {"text": "Student ID", "width": 100},
            {"text": "Name", "width": 150},
            {"text": "Attendance", "width": 100},
            {"text": "Quizzes", "width": 90},
            {"text": "Assignments", "width": 110},
            {"text": "Midterm", "width": 90},
            {"text": "Final Exam", "width": 100},
            {"text": "Final Results", "width": 110},
            {"text": "Final Grade", "width": 80}
        ]

        # Create table with empty rowdata
        self.grades_table = Tableview(
            table_frame,
            coldata=columns,
            rowdata=[],
            searchable=True,
            bootstyle="primary",
            height=15,
            autofit=True
        )
        self.grades_table.pack(fill=BOTH, expand=YES)
        
        # Action buttons
        btn_frame = ttk.Frame(main_container)
        btn_frame.pack(fill=X, pady=(0, 10))
        
        refresh_btn = ttk.Button(
            btn_frame,
            text="Refresh Report",
            command=self.generate_report,
            bootstyle="primary",
            width=18
        )
        refresh_btn.pack(side=LEFT, padx=(0, 10))
        
        export_btn = ttk.Button(
            btn_frame,
            text="Export Report",
            command=self.export_report,
            bootstyle="info-outline",
            width=18
        )
        export_btn.pack(side=LEFT)
    
    def generate_report(self):
        """Generate comprehensive report"""
        from attendance_system.utils.calculations import generate_report
        
        report_data = generate_report(self.db)
        
        # Clear existing data
        self.grades_table.delete_rows()
        
        if not report_data:
            self.stats_label.config(text="No student data available")
            return
        
        passing_count = 0
        total_avg = 0
        grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        
        # Add data to table
        for data in report_data:
            row_data = [
                data['student_id'],
                data['name'],
                f"{data['grades'].get('Attendance', 0):.1f}%",
                f"{data['grades'].get('Quizzes', 0):.1f}%",
                f"{data['grades'].get('Assignments', 0):.1f}%",
                f"{data['grades'].get('Midterm', 0):.1f}%",
                f"{data['grades'].get('Final Exam', 0):.1f}%",
                f"{data['final']:.2f}%",
                str(data['letter'])
            ]
            self.grades_table.insert_row(END, row_data)
            
            if data['final'] >= 60:
                passing_count += 1
            total_avg += data['final']
            
            # Count letter grades
            letter = str(data['letter'])
            if letter in grade_counts:
                grade_counts[letter] += 1
        
        self.grades_table.load_table_data()
        
        # Update statistics
        avg_grade = total_avg / len(report_data)
        pass_rate = (passing_count / len(report_data)) * 100
        
        stats_text = (
            f"Total Students: {len(report_data)}  |  "
            f"Average Grade: {avg_grade:.2f}%  |  "
            f"Pass Rate: {pass_rate:.1f}% ({passing_count}/{len(report_data)})\n\n"
            f"Grade Distribution:  "
            f"A's: {grade_counts['A']}  |  "
            f"B's: {grade_counts['B']}  |  "
            f"C's: {grade_counts['C']}  |  "
            f"D's: {grade_counts['D']}  |  "
            f"F's: {grade_counts['F']}"
        )
        
        self.stats_label.config(text=stats_text)
    
    def export_report(self):
        """Export report to Excel"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if filename:
            try:
                from attendance_system.utils.exports import export_report
                export_report(self.db, filename)
                messagebox.showinfo("Success", "Report exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")