"""
Reports Screen - Kivy Version
Reports and analytics interface
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle


class ReportsScreen(BoxLayout):
    """Reports and analytics screen"""
    
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 20
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets"""
        # Title
        title = Label(
            text='Grade Reports & Analytics',
            font_size='22sp',
            bold=True,
            color=(0.06, 0.09, 0.16, 1),
            size_hint_y=None,
            height=40,
            halign='left'
        )
        title.bind(size=title.setter('text_size'))
        self.add_widget(title)
        
        # Statistics section
        self.create_statistics()
        
        # Grades table
        self.create_grades_table()
        
        # Action buttons
        self.create_action_buttons()
    
    def create_statistics(self):
        """Create statistics display"""
        stats_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=140,
            padding=20,
            spacing=10
        )
        
        # Background
        with stats_container.canvas.before:
            Color(0.02, 0.71, 0.41, 0.1)  # Light green background
            self.stats_rect = RoundedRectangle(
                size=stats_container.size,
                pos=stats_container.pos,
                radius=[12]
            )
        stats_container.bind(
            size=self._update_stats,
            pos=self._update_stats
        )
        
        # Stats title
        stats_title = Label(
            text='Class Statistics',
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=30,
            color=(0.06, 0.09, 0.16, 1),
            halign='left'
        )
        stats_title.bind(size=stats_title.setter('text_size'))
        stats_container.add_widget(stats_title)
        
        # Stats content
        self.stats_label = Label(
            text='Click "Refresh Report" to generate statistics',
            color=(0.5, 0.5, 0.5, 1),
            font_size='14sp',
            halign='center',
            valign='middle'
        )
        self.stats_label.bind(size=self.stats_label.setter('text_size'))
        stats_container.add_widget(self.stats_label)
        
        self.add_widget(stats_container)
    
    def _update_stats(self, instance, value):
        """Update statistics background"""
        self.stats_rect.pos = instance.pos
        self.stats_rect.size = instance.size
    
    def create_grades_table(self):
        """Create final grades table"""
        table_container = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10
        )
        
        # Background
        with table_container.canvas.before:
            Color(1, 1, 1, 1)
            self.table_rect = RoundedRectangle(
                size=table_container.size,
                pos=table_container.pos,
                radius=[12]
            )
        table_container.bind(
            size=self._update_table,
            pos=self._update_table
        )
        
        # Table title
        table_title = Label(
            text='Final Grades Summary',
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=30,
            color=(0.06, 0.09, 0.16, 1),
            halign='left'
        )
        table_title.bind(size=table_title.setter('text_size'))
        table_container.add_widget(table_title)
        
        # Headers
        header = GridLayout(cols=9, size_hint_y=None, height=40, spacing=5)
        headers = [
            'ID', 'Name', 'Attend', 'Quiz', 'Assign',
            'Mid', 'Final', 'Grade', 'Letter'
        ]
        for h in headers:
            lbl = Label(
                text=h,
                bold=True,
                color=(0.4, 0.47, 0.55, 1),
                font_size='12sp'
            )
            header.add_widget(lbl)
        table_container.add_widget(header)
        
        # Scrollable content
        scroll = ScrollView()
        self.report_list = GridLayout(
            cols=9,
            spacing=5,
            size_hint_y=None,
            padding=[0, 10, 0, 10]
        )
        self.report_list.bind(minimum_height=self.report_list.setter('height'))
        scroll.add_widget(self.report_list)
        table_container.add_widget(scroll)
        
        self.add_widget(table_container)
    
    def _update_table(self, instance, value):
        """Update table background"""
        self.table_rect.pos = instance.pos
        self.table_rect.size = instance.size
    
    def create_action_buttons(self):
        """Create action buttons"""
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        # Refresh Report
        refresh_btn = Button(
            text='Refresh Report',
            size_hint_x=None,
            width=180,
            background_color=(0.15, 0.44, 0.92, 1),
            color=(1, 1, 1, 1)
        )
        refresh_btn.bind(on_press=lambda x: self.generate_report())
        btn_layout.add_widget(refresh_btn)
        
        # Export Report
        export_btn = Button(
            text='Export Report',
            size_hint_x=None,
            width=150,
            background_color=(0.94, 0.96, 0.98, 1),
            color=(0.28, 0.34, 0.41, 1)
        )
        export_btn.bind(on_press=self.export_report)
        btn_layout.add_widget(export_btn)
        
        # Spacer
        btn_layout.add_widget(BoxLayout())
        
        self.add_widget(btn_layout)
    
    def generate_report(self):
        """Generate comprehensive report"""
        from attendance_system.utils.calculations import generate_report
        
        report_data = generate_report(self.db)
        
        # Clear existing data
        self.report_list.clear_widgets()
        
        if not report_data:
            self.stats_label.text = 'No student data available'
            return
        
        # Calculate statistics
        passing_count = sum(1 for d in report_data if d['final'] >= 60)
        total_avg = sum(d['final'] for d in report_data) / len(report_data)
        pass_rate = (passing_count / len(report_data)) * 100
        
        # Count letter grades
        grade_counts = {
            'A': sum(1 for d in report_data if str(d['letter']) == 'A'),
            'B': sum(1 for d in report_data if str(d['letter']) == 'B'),
            'C': sum(1 for d in report_data if str(d['letter']) == 'C'),
            'D': sum(1 for d in report_data if str(d['letter']) == 'D'),
            'F': sum(1 for d in report_data if str(d['letter']) == 'F')
        }
        
        # Update statistics
        stats_text = (
            f"Total Students: {len(report_data)}  |  "
            f"Average Grade: {total_avg:.2f}%  |  "
            f"Pass Rate: {pass_rate:.1f}% ({passing_count}/{len(report_data)})\n\n"
            f"Grade Distribution:  "
            f"A's: {grade_counts['A']}  |  "
            f"B's: {grade_counts['B']}  |  "
            f"C's: {grade_counts['C']}  |  "
            f"D's: {grade_counts['D']}  |  "
            f"F's: {grade_counts['F']}"
        )
        
        self.stats_label.text = stats_text
        
        # Populate table
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
            
            for text in row_data:
                lbl = Label(
                    text=str(text),
                    color=(0.28, 0.34, 0.41, 1),
                    size_hint_y=None,
                    height=35
                )
                self.report_list.add_widget(lbl)
    
    def export_report(self, instance):
        """Export report to Excel"""
        try:
            from attendance_system.utils.exports import export_report
            filename = 'final_report.xlsx'
            export_report(self.db, filename)
            self.show_popup('Success', f'Report exported to {filename}')
        except Exception as e:
            self.show_popup('Error', f'Export failed: {str(e)}')
    
    def show_popup(self, title, message):
        """Show popup message"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        content.add_widget(Label(text=message))
        
        btn = Button(
            text='OK',
            size_hint=(None, None),
            size=(100, 44),
            background_color=(0.15, 0.44, 0.92, 1),
            color=(1, 1, 1, 1)
        )
        
        btn_layout = BoxLayout(size_hint_y=None, height=44)
        btn_layout.add_widget(BoxLayout())
        btn_layout.add_widget(btn)
        btn_layout.add_widget(BoxLayout())
        content.add_widget(btn_layout)
        
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup.open()