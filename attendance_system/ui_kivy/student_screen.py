"""
Student Screen - Kivy Version (Redesigned)
Modern, spacious interface with card-based design
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
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


class StudentScreen(BoxLayout):
    """Student management screen with modern card layout"""

    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.orientation = 'vertical'
        self.padding = [0, dp(10), 0, dp(10)]
        self.spacing = dp(24)

        self.create_widgets()
        self.refresh_students()

    def create_widgets(self):
        """Create all widgets with modern spacing"""
        # Section title with subtitle
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(70),
            spacing=dp(4)
        )

        title = Label(
            text='Student Management',
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
            text='Add new students and manage attendance records',
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

        # Add student form
        self.create_add_form()

        # Student list
        self.create_student_list()

        # Action buttons
        self.create_action_buttons()

    def create_add_form(self):
        """Create modern add student form"""
        form_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(220),
            padding=dp(28),
            spacing=dp(20)
        )

        # Modern card background with shadow effect
        with form_container.canvas.before:
            Color(1, 1, 1, 1)
            self.form_rect = RoundedRectangle(
                size=form_container.size,
                pos=form_container.pos,
                radius=[dp(16)]
            )
        form_container.bind(
            size=self._update_form_rect,
            pos=self._update_form_rect
        )

        # Form title
        form_title = Label(
            text='Add New Student',
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=dp(30),
            color=(0.09, 0.11, 0.18, 1),
            halign='left',
            valign='middle'
        )
        form_title.bind(size=form_title.setter('text_size'))
        form_container.add_widget(form_title)

        # Input grid with better spacing
        input_grid = GridLayout(
            cols=2,
            spacing=dp(16),
            size_hint_y=None,
            height=dp(120),
            row_force_default=True,
            row_default_height=dp(52)
        )

        # Row 1
        self.student_id_input = ModernTextInput(hint_text='Student ID *')
        self.student_name_input = ModernTextInput(hint_text='Full Name *')

        input_grid.add_widget(self.student_id_input)
        input_grid.add_widget(self.student_name_input)

        # Row 2
        self.course_input = ModernTextInput(hint_text='Course')
        self.email_input = ModernTextInput(hint_text='Email Address')

        input_grid.add_widget(self.course_input)
        input_grid.add_widget(self.email_input)

        form_container.add_widget(input_grid)

        # Add button - modern style
        btn_layout = BoxLayout(size_hint_y=None, height=dp(52))
        add_btn = Button(
            text='Add Student',
            size_hint=(None, None),
            size=(dp(160), dp(48)),
            background_color=(0.02, 0.71, 0.41, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        add_btn.bind(on_press=self.add_student)
        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(BoxLayout())
        form_container.add_widget(btn_layout)

        self.add_widget(form_container)

    def _update_form_rect(self, instance, value):
        """Update form background"""
        self.form_rect.pos = instance.pos
        self.form_rect.size = instance.size

    def create_student_list(self):
        """Create modern student list with cards"""
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
        list_container.bind(
            size=self._update_list_rect,
            pos=self._update_list_rect
        )

        # List title
        list_header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40)
        )

        list_title = Label(
            text='Student List',
            font_size='18sp',
            bold=True,
            color=(0.09, 0.11, 0.18, 1),
            halign='left',
            valign='middle'
        )
        list_title.bind(size=list_title.setter('text_size'))
        list_header.add_widget(list_title)

        # Student count badge
        self.count_label = Label(
            text='0 students',
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

        # Column headers with better styling
        header = GridLayout(
            cols=5,
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8),
            padding=[dp(16), dp(12)]
        )

        # Header background
        with header.canvas.before:
            Color(0.96, 0.97, 0.98, 1)
            self.header_rect = RoundedRectangle(
                size=header.size,
                pos=header.pos,
                radius=[dp(8)]
            )
        header.bind(size=self._update_header_rect, pos=self._update_header_rect)

        headers = ['Student ID', 'Name', 'Course', 'Email', 'Attendance']
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
        self.student_list_layout = GridLayout(
            cols=5,
            spacing=dp(8),
            size_hint_y=None,
            padding=[dp(16), dp(12), dp(16), dp(12)]
        )
        self.student_list_layout.bind(
            minimum_height=self.student_list_layout.setter('height')
        )
        scroll.add_widget(self.student_list_layout)
        list_container.add_widget(scroll)

        self.add_widget(list_container)

    def _update_list_rect(self, instance, value):
        """Update list background"""
        self.list_rect.pos = instance.pos
        self.list_rect.size = instance.size

    def _update_header_rect(self, instance, value):
        """Update header background"""
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size

    def create_action_buttons(self):
        """Create modern action buttons"""
        btn_layout = BoxLayout(
            size_hint_y=None,
            height=dp(56),
            spacing=dp(12)
        )

        # Mark Attendance - Primary action
        mark_btn = Button(
            text='Mark Attendance',
            size_hint_x=None,
            width=dp(180),
            background_color=(0.15, 0.44, 0.92, 1),
            color=(1, 1, 1, 1),
            font_size='15sp',
            bold=True
        )
        mark_btn.bind(on_press=self.mark_attendance)
        btn_layout.add_widget(mark_btn)

        # Refresh
        refresh_btn = Button(
            text='Refresh',
            size_hint_x=None,
            width=dp(120),
            background_color=(0.94, 0.96, 0.98, 1),
            color=(0.28, 0.34, 0.41, 1),
            font_size='15sp'
        )
        refresh_btn.bind(on_press=lambda x: self.refresh_students())
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
        export_btn.bind(on_press=self.export_students)
        btn_layout.add_widget(export_btn)

        self.add_widget(btn_layout)

    def add_student(self, instance):
        """Add a new student"""
        student_id = self.student_id_input.text.strip()
        name = self.student_name_input.text.strip()
        course = self.course_input.text.strip()
        email = self.email_input.text.strip()

        if not student_id or not name:
            self.show_popup('Validation Error', 'Student ID and Name are required!')
            return

        success = self.db.add_student(student_id, name, course, email)
        if success:
            self.show_popup('Success', 'Student added successfully!')
            # Clear inputs
            self.student_id_input.text = ''
            self.student_name_input.text = ''
            self.course_input.text = ''
            self.email_input.text = ''
            self.refresh_students()
        else:
            self.show_popup('Error', 'Student ID already exists!')

    def refresh_students(self):
        """Refresh student list"""
        self.student_list_layout.clear_widgets()

        students = self.db.get_students_with_attendance()

        # Update count
        self.count_label.text = f'{len(students)} student{"s" if len(students) != 1 else ""}'

        for student in students:
            attendance_pct = 0
            if student[4] > 0:
                attendance_pct = (student[5] / student[4]) * 100

            # Add row with better styling
            for i, text in enumerate([
                student[0],
                student[1],
                student[2] or '-',
                student[3] or '-',
                f"{attendance_pct:.1f}%"
            ]):
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
                self.student_list_layout.add_widget(lbl)

    def mark_attendance(self, instance):
        """Mark attendance with modern dialog"""
        students = self.db.get_all_students()

        if not students:
            self.show_popup('Error', 'No students found!')
            return

        # Create modern popup
        content = BoxLayout(orientation='vertical', padding=dp(28), spacing=dp(20))

        # Title
        title = Label(
            text=f"Mark Attendance",
            font_size='22sp',
            bold=True,
            size_hint_y=None,
            height=dp(36),
            color=(0.09, 0.11, 0.18, 1)
        )
        content.add_widget(title)

        # Date
        date_label = Label(
            text=datetime.now().strftime('%B %d, %Y'),
            size_hint_y=None,
            height=dp(28),
            font_size='15sp',
            color=(0.5, 0.55, 0.6, 1)
        )
        content.add_widget(date_label)

        # Subtitle
        subtitle = Label(
            text='Check students who are present',
            size_hint_y=None,
            height=dp(32),
            color=(0.5, 0.5, 0.5, 1),
            font_size='14sp'
        )
        content.add_widget(subtitle)

        # Scrollable student list
        scroll = ScrollView()
        student_layout = GridLayout(
            cols=1,
            spacing=dp(12),
            size_hint_y=None,
            padding=dp(12)
        )
        student_layout.bind(minimum_height=student_layout.setter('height'))

        checkboxes = {}
        for student_id, name, course, email in students:
            row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(12))

            # Modern rounded background
            with row.canvas.before:
                Color(0.97, 0.98, 0.99, 1)
                rect = RoundedRectangle(size=row.size, pos=row.pos, radius=[dp(8)])
            row.bind(size=lambda inst, val, r=rect: setattr(r, 'size', val),
                    pos=lambda inst, val, r=rect: setattr(r, 'pos', val))

            cb = CheckBox(active=True, size_hint_x=None, width=dp(56))
            checkboxes[student_id] = cb

            lbl = Label(
                text=f"{name} ({student_id})",
                halign='left',
                valign='middle',
                font_size='15sp',
                padding=[dp(12), 0]
            )
            lbl.bind(size=lbl.setter('text_size'))

            row.add_widget(cb)
            row.add_widget(lbl)
            student_layout.add_widget(row)

        scroll.add_widget(student_layout)
        content.add_widget(scroll)

        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(12))

        def save_attendance(instance):
            today = datetime.now().strftime("%Y-%m-%d")
            for student_id, cb in checkboxes.items():
                status = "Present" if cb.active else "Absent"
                self.db.mark_attendance(student_id, today, status)
            popup.dismiss()
            self.show_popup('Success', 'Attendance saved successfully!')
            self.refresh_students()

        save_btn = Button(
            text='Save Attendance',
            background_color=(0.02, 0.71, 0.41, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        save_btn.bind(on_press=save_attendance)

        cancel_btn = Button(
            text='Cancel',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
            font_size='16sp'
        )

        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)

        # Create popup
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.7, 0.85),
            separator_height=0
        )
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    def export_students(self, instance):
        """Export students to Excel"""
        try:
            from attendance_system.utils.exports import export_students
            filename = 'students_export.xlsx'
            export_students(self.db, filename)
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