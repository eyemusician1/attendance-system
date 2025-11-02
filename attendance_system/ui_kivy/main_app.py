"""
Main Application - Kivy Version (Redesigned)
Ultra-modern, spacious Material Design interface
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from attendance_system.database.db_manager import DBManager
from attendance_system.ui_kivy.student_screen import StudentScreen
from attendance_system.ui_kivy.grades_screen import GradesScreen
from attendance_system.ui_kivy.config_screen import ConfigScreen
from attendance_system.ui_kivy.reports_screen import ReportsScreen

# Set window properties - larger for better spacing
Window.clearcolor = (0.97, 0.97, 0.98, 1)  # Light background
Window.size = (1600, 950)
Window.minimum_width = 1400
Window.minimum_height = 900


class ModernTabbedPanel(TabbedPanel):
    """Modern tabbed panel with spacious design"""

    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db

        # Configure tabbed panel with better spacing
        self.do_default_tab = False
        self.tab_pos = 'top_left'
        self.tab_width = dp(180)
        self.tab_height = dp(56)
        self.background_color = (1, 1, 1, 0)

        # Create tabs
        self.create_tabs()

    def create_tabs(self):
        """Create all tabs with icons"""
        # Students Tab
        student_tab = TabbedPanelItem(text='Students')
        student_tab.add_widget(StudentScreen(self.db))
        self.add_widget(student_tab)

        # Grades Tab
        grades_tab = TabbedPanelItem(text='Grades')
        self.grades_screen = GradesScreen(self.db, self.calculate_final_grades)
        grades_tab.add_widget(self.grades_screen)
        self.add_widget(grades_tab)

        # Settings Tab
        config_tab = TabbedPanelItem(text='Settings')
        config_tab.add_widget(ConfigScreen(self.db))
        self.add_widget(config_tab)

        # Reports Tab
        reports_tab = TabbedPanelItem(text='Reports')
        self.reports_screen = ReportsScreen(self.db)
        reports_tab.add_widget(self.reports_screen)
        self.add_widget(reports_tab)

    def calculate_final_grades(self):
        """Calculate final grades and switch to reports"""
        self.reports_screen.generate_report()
        self.switch_to(self.tab_list[-1])


class MainScreen(BoxLayout):
    """Main screen with modern, spacious layout"""

    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.orientation = 'vertical'
        self.padding = 0
        self.spacing = 0

        # Create header
        self.create_header()

        # Create main content
        self.create_content()

    def create_header(self):
        """Create modern, spacious header"""
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(100),
            padding=[dp(40), dp(24), dp(40), dp(24)],
            spacing=dp(24)
        )

        # Background with gradient effect
        with header.canvas.before:
            Color(1, 1, 1, 1)
            self.header_rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self._update_header_rect, pos=self._update_header_rect)

        # Left side - Title with better typography
        title_layout = BoxLayout(orientation='vertical', spacing=dp(2))

        title_label = Label(
            text='Student Management System',
            font_size='32sp',
            bold=True,
            color=(0.09, 0.11, 0.18, 1),
            size_hint_x=None,
            width=dp(600),
            halign='left',
            valign='bottom'
        )
        title_label.bind(size=title_label.setter('text_size'))

        subtitle_label = Label(
            text='Professional attendance and grade management',
            font_size='16sp',
            color=(0.5, 0.55, 0.6, 1),
            size_hint_x=None,
            width=dp(600),
            halign='left',
            valign='top'
        )
        subtitle_label.bind(size=subtitle_label.setter('text_size'))

        title_layout.add_widget(title_label)
        title_layout.add_widget(subtitle_label)
        header.add_widget(title_layout)

        # Spacer
        header.add_widget(BoxLayout())

        # Right side - Theme button with modern styling
        self.theme_btn = Button(
            text='Toggle Theme',
            size_hint=(None, None),
            size=(dp(140), dp(48)),
            background_color=(0.15, 0.44, 0.92, 1),
            color=(1, 1, 1, 1),
            font_size='15sp',
            bold=True
        )
        self.theme_btn.bind(on_press=self.toggle_theme)
        header.add_widget(self.theme_btn)

        self.add_widget(header)

    def _update_header_rect(self, instance, value):
        """Update header background rectangle"""
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size

    def create_content(self):
        """Create main content area with better spacing"""
        # Container with generous padding
        container = BoxLayout(
            orientation='vertical',
            padding=[dp(40), dp(20), dp(40), dp(40)],
            spacing=0
        )

        # Subtle separator
        separator = BoxLayout(size_hint_y=None, height=dp(2))
        with separator.canvas.before:
            Color(0.89, 0.91, 0.93, 1)
            self.sep_rect = Rectangle(size=separator.size, pos=separator.pos)
        separator.bind(size=self._update_sep_rect, pos=self._update_sep_rect)
        container.add_widget(separator)

        # Add spacing before tabs
        container.add_widget(BoxLayout(size_hint_y=None, height=dp(24)))

        # Tabbed panel with modern styling
        self.tabbed_panel = ModernTabbedPanel(self.db)
        container.add_widget(self.tabbed_panel)

        self.add_widget(container)

    def _update_sep_rect(self, instance, value):
        """Update separator rectangle"""
        self.sep_rect.pos = instance.pos
        self.sep_rect.size = instance.size

    def toggle_theme(self, instance):
        """Toggle between light and dark theme"""
        if Window.clearcolor[0] > 0.5:
            # Switch to dark
            Window.clearcolor = (0.09, 0.11, 0.18, 1)
            instance.text = 'Light Theme'
            instance.background_color = (0.94, 0.96, 0.98, 1)
            instance.color = (0.09, 0.11, 0.18, 1)
        else:
            # Switch to light
            Window.clearcolor = (0.97, 0.97, 0.98, 1)
            instance.text = 'Toggle Theme'
            instance.background_color = (0.15, 0.44, 0.92, 1)
            instance.color = (1, 1, 1, 1)


class StudentManagementApp(App):
    """Main Kivy Application"""

    def build(self):
        """Build the application"""
        self.title = 'Student Management System'
        self.icon = None  # Add your icon path here
        
        # Initialize database
        self.db = DBManager()
        
        # Create and return main screen
        return MainScreen(self.db)
    
    def on_stop(self):
        """Clean up when app closes"""
        self.db.close()


if __name__ == '__main__':
    StudentManagementApp().run()