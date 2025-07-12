from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.metrics import dp
from screens.background import ParallaxWidget
from screens.hover_button import HoverImageButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
import copy

class ImageSwitch(ToggleButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_source()
        self.bind(state=self.on_state_change)

    def on_state_change(self, *args):
        self.update_source()

    def update_source(self):
        self.source = 'assets/images/buttons/on_sound_effect.png' if self.state == 'down' else 'assets/images/buttons/off_sound_effect.png'

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        # Add animated background
        self.bg_parallax = ParallaxWidget()
        self.add_widget(self.bg_parallax)

        # Add semi-transparent overlay
        with self.canvas:
            self.overlay_color = Color(0, 0, 0, 0.2)
            self.overlay_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_overlay, size=self.update_overlay)

        main_layout = FloatLayout()
        self.add_widget(main_layout)

        # Title label
        title_label = Label(
            text='[size=100][color=ffffff]Settings[/color][/size]',
            font_name="assets/fonts/HeehawRegular.ttf",
            markup=True,
            size_hint=(1, None),
            height=Window.height * 0.08,
            halign='center',
            valign='middle',
            pos_hint={'top': 0.92, 'center_x': 0.5}
        )
        main_layout.add_widget(title_label)

        # Main settings layout
        self.settings_layout = BoxLayout(
            orientation='vertical',
            spacing=Window.height * 0.01,
            size_hint=(0.7, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Sound effect toggle row
        sound_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.13,
            padding=(Window.width * 0.05, Window.width * 0.15, 0, 0)
        )

        sound_label = Label(
            text='[size=40][color=ffffff]Sound Effects:[/color][/size]',
            font_name="assets/fonts/HeehawRegular.ttf",
            markup=True,
            size_hint=(0.7, 1),
            halign='left',
            valign='middle'
        )
        sound_label.bind(size=sound_label.setter('text_size'))
        sound_layout.add_widget(sound_label)

        self.sound_switch = ImageSwitch(size_hint=(0.3, 1))
        self.sound_switch.bind(on_press=self.on_sound_toggle)
        sound_layout.add_widget(self.sound_switch)

        self.settings_layout.add_widget(sound_layout)

        # Volume slider row
        volume_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.13,
            padding=(Window.width * 0.05, 0, 0, 0),
            spacing=Window.width * 0.02
        )

        volume_row = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=Window.height * 0.08
        )

        volume_label = Label(
            text='[size=40][color=ffffff]Volume:[/color][/size]',
            font_name="assets/fonts/HeehawRegular.ttf",
            markup=True,
            size_hint=(0.25, 1),
            halign='left',
            valign='middle'
        )
        volume_label.bind(size=volume_label.setter('text_size'))

        self.volume_slider = Slider(
            min=0.0,
            max=1.0,
            value=0.8,
            step=0.1,
            size_hint=(0.6, 1),
            background_horizontal="assets/images/buttons/volume_1.png",
            cursor_image="assets/images/buttons/volume_2.png"
        )
        self.volume_slider.bind(value=self.on_volume_change)

        self.volume_value_label = Label(
            text='80%',
            font_size='20sp',
            size_hint=(0.15, 1),
            halign='center',
            valign='middle'
        )

        volume_row.add_widget(volume_label)
        volume_row.add_widget(self.volume_slider)
        volume_row.add_widget(self.volume_value_label)
        volume_layout.add_widget(volume_row)
        self.settings_layout.add_widget(volume_layout)

        # Buttons for reset and home
        buttons_row = BoxLayout(
            orientation='vertical',
            size_hint_y=0.22,
            spacing=Window.height * 0.015,
            padding=(Window.width * 0.05, Window.height * 0.015, Window.width * 0.05, Window.height * 0.005)
        )

        self.reset_btn = HoverImageButton(
            source="assets/images/buttons/reset.png",
            size_hint=(1, None),
            height=Window.height * 0.09
        )
        self.reset_btn.bind(on_press=self.reset_data)

        self.home_btn = HoverImageButton(
            source="assets/images/buttons/home.png",
            size_hint=(1, None),
            height=Window.height * 0.11
        )
        self.home_btn.bind(on_press=self.go_back)

        buttons_row.add_widget(self.reset_btn)
        buttons_row.add_widget(self.home_btn)

        self.settings_layout.add_widget(buttons_row)
        main_layout.add_widget(self.settings_layout)

    def update_overlay(self, *args):
        self.overlay_rect.pos = self.pos
        self.overlay_rect.size = self.size

    def toggle_music_state(self, instance):
        app = App.get_running_app()
        is_on = instance.state == 'down'
        instance.text = 'Music: ON' if is_on else 'Music: OFF'
        app.data_manager.set_music_enabled(is_on)
        if hasattr(app, 'sound_manager'):
            if is_on:
                app.sound_manager.play_background_music()
            else:
                app.sound_manager.stop_background_music()

    def update_bg(self, *args):
        self.bg_rect.size = Window.size

    def on_enter(self):
        self.load_settings()

    def load_settings(self):
        app = App.get_running_app()
        if app and hasattr(app, 'data_manager'):
            self.sound_switch.active = app.data_manager.get_sound_enabled()
            volume = app.data_manager.get_volume()
            self.volume_slider.value = volume
            self.volume_value_label.text = f'{int(volume * 100)}%'
            self.on_volume_change(self.volume_slider, volume)

    def on_sound_toggle(self, instance):
        """Handle sound effect toggle."""
        app = App.get_running_app()
        if app and hasattr(app, 'data_manager'):
            value = instance.state == 'down'
            app.data_manager.set_sound_enabled(value)
            if value and hasattr(app, 'sound_manager'):
                app.sound_manager.play_sound('button_click')

    def on_volume_change(self, slider, value):
        app = App.get_running_app()
        if app and hasattr(app, 'data_manager'):
            app.data_manager.set_volume(value)
            self.volume_value_label.text = f'{int(value * 100)}%'
            if hasattr(app, 'sound_manager'):
                app.sound_manager.set_volume(value)

    def reset_data(self, button):
        app = App.get_running_app()
        if app and hasattr(app, 'data_manager'):
            if hasattr(app, 'sound_manager'):
                app.sound_manager.play_sound('button_click')
            # Reset data to default and save
            app.data_manager.data = copy.deepcopy(app.data_manager.default_data)
            app.data_manager.save_data()
            self.load_settings()  
            # Update sound settings after reset
            if hasattr(app, 'sound_manager'):
                app.sound_manager.set_volume(app.data_manager.get_volume())
                if app.data_manager.get_music_enabled():
                    app.sound_manager.play_background_music()
                else:
                    app.sound_manager.stop_background_music()
            # Show reset confirmation
            button.text = 'DATA RESET!'
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: setattr(button, 'text', 'RESET ALL DATA'), 2.0)

    def go_back(self, button):
        app = App.get_running_app()
        if app and hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')
        self.manager.current = 'main_menu'
