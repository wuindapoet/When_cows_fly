# game_settings_screen.py
from screens.settings_screen import SettingsScreen
from kivy.metrics import dp
from screens.hover_button import HoverImageButton
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.window import Window


class GameSettingsScreen(SettingsScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build_ui(self):
        super().build_ui()

        if hasattr(self, 'home_btn'):
            # Hide old home button in buttons_row
            self.home_btn.opacity = 0
            self.home_btn.disabled = True
            self.home_btn.size_hint_y = None
            self.home_btn.height = 0

        return_btn = HoverImageButton(
            source="assets/images/buttons/return.png",
            size_hint=(1, None),
            height=Window.height * 0.11
        )
        return_btn.bind(on_press=self.go_back_to_game)

        # Create new home button
        custom_home_btn = HoverImageButton(
            source="assets/images/buttons/home.png",
            size_hint=(1, None),
            height=Window.height * 0.11
        )
        custom_home_btn.bind(on_press=self.go_home)

        # Horizontal layout
        bottom_buttons = BoxLayout(
            orientation='horizontal',
            spacing=dp(15),
            size_hint=(1, None),
            height=Window.height * 0.11,
            padding=(dp(20), 0, dp(20), 0)
        )
        bottom_buttons.add_widget(return_btn)
        bottom_buttons.add_widget(custom_home_btn)

        if hasattr(self, 'settings_layout'):
            self.settings_layout.add_widget(bottom_buttons)

    def go_back_to_game(self, button):
        app = App.get_running_app()
        if app and hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')

        if 'game' in self.manager.screen_names:
            game_screen = self.manager.get_screen('game')

            if hasattr(self, 'saved_score'):
                game_screen.score = self.saved_score
            if hasattr(self, 'saved_lives'):
                game_screen.lives = self.saved_lives

            game_screen.is_paused = True
            self.manager.current = 'game'

    def go_home(self, button):
        app = App.get_running_app()
        if app and hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')

        if 'game' in self.manager.screen_names:
            game_screen = self.manager.get_screen('game')
            game_screen.reset_game()


        self.manager.current = 'main_menu'

    def on_enter(self):
        super().on_enter()
        app = App.get_running_app()
        if 'game' in self.manager.screen_names:
            game_screen = self.manager.get_screen('game')
            self.saved_score = game_screen.score
            self.saved_lives = game_screen.lives