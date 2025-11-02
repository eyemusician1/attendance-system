"""
Config Screen - Kivy Version
Configuration interface for grading weights
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle


class ConfigScreen(BoxLayout):
    """Configuration screen for grading weights"""
    
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 20
        
        self.create_widgets()
        self.load_config()
    
    def create_widgets(self):
        """Create all widgets"""
        # Title
        title = Label(
            text='Grading Configuration',
            font_size='22sp',
            bold=True,
            color=(0.06, 0.09, 0.16, 1),
            size_hint_y=None,
            height=40,
            halign='left'
        )
        title.bind(size=title.setter('text_size'))
        self.add_widget(title)
        
        # Subtitle
        subtitle = Label(
            text='Configure grading weights for each component. Total must equal 100%',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=30,
            halign='left'
        )
        subtitle.bind(size=subtitle.setter('text_size'))
        self.add_widget(subtitle)
        
        # Config table
        self.create_config_table()
        
        # Action buttons
        self.create_action_buttons()
        
        # Grade scale info
        self.create_grade_scale()
        
        # Spacer
        self.add_widget(BoxLayout())
    
    def create_config_table(self):
        """Create configuration table"""
        table_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=320,
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
            text='Component Weights',
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
        header = GridLayout(cols=2, size_hint_y=None, height=40, spacing=10)
        header.add_widget(Label(
            text='Component',
            bold=True,
            color=(0.4, 0.47, 0.55, 1),
            font_size='13sp'
        ))
        header.add_widget(Label(
            text='Weight (%)',
            bold=True,
            color=(0.4, 0.47, 0.55, 1),
            font_size='13sp'
        ))
        table_container.add_widget(header)
        
        # Config inputs grid
        self.config_inputs = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None,
            height=220,
            padding=[0, 10, 0, 10]
        )
        table_container.add_widget(self.config_inputs)
        
        self.add_widget(table_container)
    
    def _update_table(self, instance, value):
        """Update table background"""
        self.table_rect.pos = instance.pos
        self.table_rect.size = instance.size
    
    def create_action_buttons(self):
        """Create action buttons"""
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        # Save Configuration
        save_btn = Button(
            text='Save Configuration',
            size_hint_x=None,
            width=200,
            background_color=(0.02, 0.71, 0.41, 1),
            color=(1, 1, 1, 1)
        )
        save_btn.bind(on_press=self.save_config)
        btn_layout.add_widget(save_btn)
        
        # Reset to Default
        reset_btn = Button(
            text='Reset to Default',
            size_hint_x=None,
            width=180,
            background_color=(0.94, 0.96, 0.98, 1),
            color=(0.28, 0.34, 0.41, 1)
        )
        reset_btn.bind(on_press=self.reset_config)
        btn_layout.add_widget(reset_btn)
        
        # Spacer
        btn_layout.add_widget(BoxLayout())
        
        self.add_widget(btn_layout)
    
    def create_grade_scale(self):
        """Create grade scale information"""
        scale_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=200,
            padding=20,
            spacing=10
        )
        
        # Background
        with scale_container.canvas.before:
            Color(0.94, 0.97, 1, 1)  # Light blue background
            self.scale_rect = RoundedRectangle(
                size=scale_container.size,
                pos=scale_container.pos,
                radius=[12]
            )
        scale_container.bind(
            size=self._update_scale,
            pos=self._update_scale
        )
        
        # Scale title
        scale_title = Label(
            text='Grade Point Scale',
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=30,
            color=(0.06, 0.09, 0.16, 1),
            halign='left'
        )
        scale_title.bind(size=scale_title.setter('text_size'))
        scale_container.add_widget(scale_title)
        
        # Scale information
        scale_text = Label(
            text=(
                'Grading Scale:\n\n'
                '100% = 1.00  |  90% = 1.25  |  85% = 1.75  |  80% = 2.00\n'
                '75% = 2.25   |  70% = 2.50  |  65% = 2.75  |  60% = 3.00\n\n'
                'Below 60% = 5.00 (Failed)'
            ),
            color=(0.28, 0.34, 0.41, 1),
            font_size='13sp',
            halign='center',
            valign='middle'
        )
        scale_text.bind(size=scale_text.setter('text_size'))
        scale_container.add_widget(scale_text)
        
        self.add_widget(scale_container)
    
    def _update_scale(self, instance, value):
        """Update scale background"""
        self.scale_rect.pos = instance.pos
        self.scale_rect.size = instance.size
    
    def load_config(self):
        """Load configuration from database"""
        self.config_inputs.clear_widgets()
        config = self.db.get_grading_config()
        self.weight_inputs = {}
        
        for component, weight in config:
            # Component label
            component_label = Label(
                text=component,
                color=(0.28, 0.34, 0.41, 1),
                halign='left',
                valign='middle'
            )
            component_label.bind(size=component_label.setter('text_size'))
            self.config_inputs.add_widget(component_label)
            
            # Weight input
            weight_input = TextInput(
                text=str(weight),
                multiline=False,
                input_filter='float',
                size_hint_x=0.6
            )
            self.weight_inputs[component] = weight_input
            self.config_inputs.add_widget(weight_input)
    
    def save_config(self, instance):
        """Save configuration to database"""
        total = 0
        updates = []
        
        # Validate all inputs
        for component, input_widget in self.weight_inputs.items():
            try:
                weight = float(input_widget.text)
                total += weight
                updates.append((component, weight))
            except ValueError:
                self.show_popup('Error', f'Invalid weight value for {component}')
                return
        
        # Check if total equals 100
        if abs(total - 100.0) > 0.01:
            self.show_popup(
                'Validation Error',
                f'Total weight must equal 100%\nCurrently: {total:.1f}%'
            )
            return
        
        # Save to database
        try:
            for component, weight in updates:
                self.db.update_grading_config(component, weight)
            self.show_popup('Success', 'Grading configuration saved successfully!')
        except Exception as e:
            self.show_popup('Error', f'Failed to save configuration: {str(e)}')
    
    def reset_config(self, instance):
        """Reset configuration to default values"""
        # Create confirmation popup
        content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        content.add_widget(Label(
            text='Are you sure you want to reset\nthe configuration to default values?'
        ))
        
        btn_layout = BoxLayout(size_hint_y=None, height=44, spacing=10)
        
        def confirm_reset(btn_instance):
            try:
                self.db.reset_grading_config()
                self.load_config()
                popup.dismiss()
                self.show_popup('Success', 'Configuration reset to default values!')
            except Exception as e:
                popup.dismiss()
                self.show_popup('Error', f'Failed to reset configuration: {str(e)}')
        
        yes_btn = Button(
            text='Yes, Reset',
            background_color=(0.93, 0.26, 0.26, 1),
            color=(1, 1, 1, 1)
        )
        yes_btn.bind(on_press=confirm_reset)
        
        no_btn = Button(
            text='Cancel',
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Confirm Reset',
            content=content,
            size_hint=(0.6, 0.4)
        )
        no_btn.bind(on_press=popup.dismiss)
        popup.open()
    
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