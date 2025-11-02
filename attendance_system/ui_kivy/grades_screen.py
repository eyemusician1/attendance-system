"""
Grades Screen - Kivy Version (Redesigned)
Modern, spacious interface with card-based design
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from datetime import datetime


class ModernTextInput(TextInput):
    """Custom text input with better styling"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1, 1, 1, 1)
        self.foreground_color = (0.2, 0.2, 0.2, 1)
        self.cursor_color = (0.15, 0.44, 0.92, 1)
        self.padding = [dp(16), dp(12)]
        self.font_size = '15sp'
        self.multiline = False


class GradesScreen(BoxLayout):
    """Grades management screen with modern card layout"""

    def __init__(self, db, calculate_callback, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.calculate_callback = calculate_callback
        self.orientation = 'vertical'
        self.padding = [0, dp(10), 0, dp(10)]
        self.spacing = dp(24)

        self.create_widgets()
        self.refresh_grades()

    def create_widgets(self):
        """Create all widgets with modern spacing"""
        # Section header
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(70),
            spacing=dp(4)
        )

        title = Label(
            text='Grade Management',
            font_size='26sp',
            bold=True,
            color=(0.09, 0.11, 0.18, 1),
            size_hint_y=None,
            height=dp(40),
            halign='left',
            valign='bottom'
        )
        title.bind(size=title.setter('text_size'))

        subtitle = Label(
            text='Record and manage student grades and assessments',
            font_size='15sp',
            color=(0.5, 0.55, 0.6, 1),
            size_hint_y=None,
            height=dp(26),
            halign='left',
            valign='top'
        )
        subtitle.bind(size=subtitle.setter('text_size'))

        header_layout.add_widget(title)
        header_layout.add_widget(subtitle)
        self.add_widget(header_layout)

        # Add grade form
        self.create_add_form()

        # Grades list
        self.create_grades_list()

        # Action buttons
        self.create_action_buttons()

    def create_add_form(self):
        """Create modern add grade form"""
        form = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(240),
            padding=dp(28),
            spacing=dp(20)
        )

        # Modern card background
        with form.canvas.before:
            Color(1, 1, 1, 1)
            self.form_rect = RoundedRectangle(
                size=form.size,
                pos=form.pos,
                radius=[dp(16)]
            )
        form.bind(size=self._update_form, pos=self._update_form)

        # Form title
        form_title = Label(
            text='Add New Grade',
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=dp(30),
            color=(0.09, 0.11, 0.18, 1),
            halign='left',
            valign='middle'
        )
        form_title.bind(size=form_title.setter('text_size'))
        form.add_widget(form_title)

        # Input grid - better layout
        grid = GridLayout(
            cols=3,
            spacing=dp(16),
            size_hint_y=None,
            height=dp(120),
            row_force_default=True,
            row_default_height=dp(52)
        )

        # Row 1
        self.grade_student_id = ModernTextInput(hint_text='Student ID *')

        self.assessment_type = Spinner(
            text='Select Type',
            values=['Attendance', 'Quizzes', 'Assignments', 'Midterm', 'Final Exam'],
            background_color=(1, 1, 1, 1),
            color=(0.2, 0.2, 0.2, 1),
            font_size='15sp',
            size_hint_y=None,
            height=dp(52)
        )

        self.assessment_name = ModernTextInput(hint_text='Assessment Name *')

        grid.add_widget(self.grade_student_id)
        grid.add_widget(self.assessment_type)
        grid.add_widget(self.assessment_name)

        # Row 2
        self.score_input = ModernTextInput(hint_text='Score', input_filter='float')
        self.max_score_input = ModernTextInput(hint_text='Max Score', input_filter='float')
        self.max_score_input.text = '100'

        grid.add_widget(self.score_input)
        grid.add_widget(self.max_score_input)
        grid.add_widget(BoxLayout())  # Empty cell

        form.add_widget(grid)

        # Add button
        btn_layout = BoxLayout(size_hint_y=None, height=dp(52))
        add_btn = Button(
            text='Add Grade',
            size_hint=(None, None),
            size=(dp(160), dp(48)),
            background_color=(0.02, 0.71, 0.41, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        add_btn.bind(on_press=self.add_grade)
        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(BoxLayout())
        form.add_widget(btn_layout)

        self.add_widget(form)

    def _update_form(self, instance, value):
        self.form_rect.pos = instance.pos
        self.form_rect.size = instance.size

    def create_grades_list(self):
        """Create modern grades list"""
        list_container = BoxLayout(
            orientation='vertical',
            padding=dp(28),
            spacing=dp(16)
        )

        # Card background
        with list_container.canvas.before:
            Color(1, 1, 1, 1)
            self.list_rect = RoundedRectangle(
                size=list_container.size,
                pos=list_container.pos,
                radius=[dp(16)]
            )
        list_container.bind(size=self._update_list, pos=self._update_list)

        # List header
        list_header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40)
        )

        list_title = Label(
            text='Grade Records',
            font_size='18sp',
            bold=True,
            color=(0.09, 0.11, 0.18, 1),
            halign='left',
            valign='middle'
        )
        list_title.bind(size=list_title.setter('text_size'))
        list_header.add_widget(list_title)

        # Record count
        self.count_label = Label(
            text='0 records',
            font_size='14sp',
            color=(0.5, 0.55, 0.6, 1),
            size_hint_x=None,
            width=dp(120),
            halign='right',
            valign='middle'
        )
        self.count_label.bind(size=self.count_label.setter('text_size'))
        list_header.add_widget(self.count_label)

        list_container.add_widget(list_header)

        # Column headers
        header = GridLayout(
            cols=8,
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8),
            padding=[dp(16), dp(12)]
        )

        with header.canvas.before:
            Color(0.96, 0.97, 0.98, 1)
            self.header_rect = RoundedRectangle(
                size=header.size,
                pos=header.pos,
                radius=[dp(8)]
            )
        header.bind(size=self._update_header, pos=self._update_header)

        headers = ['Student ID', 'Name', 'Type', 'Assessment', 'Score', 'Max', '%', 'Date']
        for h in headers:
            lbl = Label(
                text=h,
                bold=True,
                color=(0.4, 0.47, 0.55, 1),
                font_size='13sp',
                halign='left',
                valign='middle'
            )
            lbl.bind(size=lbl.setter('text_size'))
            header.add_widget(lbl)

        list_container.add_widget(header)

        # Scrollable content
        scroll = ScrollView()
        self.grades_list = GridLayout(
            cols=8,
            spacing=dp(8),
            size_hint_y=None,
            padding=[dp(16), dp(12)]
        )
        self.grades_list.bind(minimum_height=self.grades_list.setter('height'))
        scroll.add_widget(self.grades_list)
        list_container.add_widget(scroll)

        self.add_widget(list_container)

    def _update_list(self, instance, value):
        self.list_rect.pos = instance.pos
        self.list_rect.size = instance.size

    def _update_header(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size

    def create_action_buttons(self):
        """Create modern action buttons"""
        btn_layout = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(12))

        # Calculate button - primary action
        calc_btn = Button(
            text='Calculate Final Grades',
            size_hint_x=None,
            width=dp(220),
            background_color=(0.15, 0.44, 0.92, 1),
            color=(1, 1, 1, 1),
            font_size='15sp',
            bold=True
        )
        calc_btn.bind(on_press=lambda x: self.calculate_callback())
        btn_layout.add_widget(calc_btn)

        # Refresh
        refresh_btn = Button(
            text='Refresh',
            size_hint_x=None,
            width=dp(120),
            background_color=(0.94, 0.96, 0.98, 1),
            color=(0.28, 0.34, 0.41, 1),
            font_size='15sp'
        )
        refresh_btn.bind(on_press=lambda x: self.refresh_grades())
        btn_layout.add_widget(refresh_btn)

        # Spacer
        btn_layout.add_widget(BoxLayout())

        # Export
        export_btn = Button(
            text='Export to Excel',
            size_hint_x=None,
            width=dp(160),
            background_color=(0.94, 0.96, 0.98, 1),
            color=(0.28, 0.34, 0.41, 1),
            font_size='15sp'
        )
        export_btn.bind(on_press=self.export_grades)
        btn_layout.add_widget(export_btn)

        self.add_widget(btn_layout)

    def add_grade(self, instance):
        """Add a new grade"""
        student_id = self.grade_student_id.text.strip()
        assessment_type = self.assessment_type.text
        assessment_name = self.assessment_name.text.strip()

        if assessment_type == 'Select Type':
            self.show_popup('Validation Error', 'Please select an assessment type!')
            return

        try:
            score = float(self.score_input.text or 0)
            max_score = float(self.max_score_input.text or 100)
        except ValueError:
            self.show_popup('Validation Error', 'Invalid score values!')
            return

        if not student_id or not assessment_name:
            self.show_popup('Validation Error', 'Student ID and Assessment Name are required!')
            return

        if max_score == 0:
            self.show_popup('Validation Error', 'Max score cannot be zero!')
            return

        if not self.db.get_student(student_id):
            self.show_popup('Error', 'Student ID not found!')
            return

        try:
            date = datetime.now().strftime("%Y-%m-%d")
            self.db.add_grade(student_id, assessment_type, assessment_name, score, max_score, date)
            self.show_popup('Success', 'Grade added successfully!')

            # Clear inputs
            self.grade_student_id.text = ''
            self.assessment_name.text = ''
            self.score_input.text = ''
            self.max_score_input.text = '100'
            self.assessment_type.text = 'Select Type'

            self.refresh_grades()
        except Exception as e:
            self.show_popup('Error', str(e))

    def refresh_grades(self):
        """Refresh grades list"""
        self.grades_list.clear_widgets()
        grades = self.db.get_all_grades()

        # Update count
        self.count_label.text = f'{len(grades)} record{"s" if len(grades) != 1 else ""}'

        for grade in grades:
            percentage = (grade[4] / grade[5]) * 100 if grade[5] > 0 else 0

            for text in [
                grade[0], grade[1], grade[2], grade[3],
                f"{grade[4]:.1f}", f"{grade[5]:.1f}",
                f"{percentage:.1f}%", grade[6]
            ]:
                lbl = Label(
                    text=str(text),
                    color=(0.28, 0.34, 0.41, 1),
                    size_hint_y=None,
                    height=dp(44),
                    font_size='14sp',
                    halign='left',
                    valign='middle'
                )
                lbl.bind(size=lbl.setter('text_size'))
                self.grades_list.add_widget(lbl)

    def export_grades(self, instance):
        """Export grades to Excel"""
        try:
            from attendance_system.utils.exports import export_grades
            filename = 'grades_export.xlsx'
            export_grades(self.db, filename)
            self.show_popup('Success', f'Exported to {filename}')
        except Exception as e:
            self.show_popup('Error', f'Export failed: {str(e)}')

    def show_popup(self, title, message):
        """Show modern popup message"""
        content = BoxLayout(orientation='vertical', padding=dp(28), spacing=dp(24))

        msg_label = Label(
            text=message,
            font_size='16sp',
            color=(0.28, 0.34, 0.41, 1)
        )
        content.add_widget(msg_label)

        btn = Button(
            text='OK',
            size_hint=(None, None),
            size=(dp(120), dp(48)),
            background_color=(0.15, 0.44, 0.92, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        btn_layout = BoxLayout(size_hint_y=None, height=dp(48))
        btn_layout.add_widget(BoxLayout())
        btn_layout.add_widget(btn)
        btn_layout.add_widget(BoxLayout())
        content.add_widget(btn_layout)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.5, 0.35),
            title_size='18sp'
        )
        btn.bind(on_press=popup.dismiss)
        popup.open()