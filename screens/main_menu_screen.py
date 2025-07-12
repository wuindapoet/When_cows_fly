import os
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.resources import resource_find
from kivy.uix.behaviors import ButtonBehavior
from screens.hover_button import HoverImageButton 
from screens.background import ParallaxWidget  

class ImageButton(ButtonBehavior, Image):
    pass

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        self.music_tracks = [f'background_{i}.mp3' for i in range(1, 7)]
        self.current_music = None

    def build_ui(self):
        self.bg_parallax = ParallaxWidget()
        self.add_widget(self.bg_parallax)
        # Root layout
        main_layout = FloatLayout()
        self.add_widget(main_layout)

        # Main vertical layout
        vertical_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20,
            size_hint=(1, 1)
        )

        # Cow preview
        self.cow_preview = Image(source="assets/images/characters/logo.png",size_hint=(None, None), size=(500, 400), allow_stretch=True, keep_ratio=True)
        self.preview_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=20, padding=[0, 20])
        self.preview_layout.add_widget(Widget(size_hint=(0.5, 1)))  # left spacer
        self.preview_layout.add_widget(self.cow_preview)
        self.preview_layout.add_widget(Widget(size_hint=(0.5, 1)))  # right spacer

        # Score label
        self.score_label = Label(
            text='',
            markup=True,
            size_hint=(1, 0.15),
            halign='center'
        )

        # Buttons
        button_layout = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.45))

        play_btn = ImageButton(source='assets/images/buttons/play_button.png', size_hint=(None, None), size=(200, 100), allow_stretch=True)
        shop_btn = ImageButton(source='assets/images/buttons/shop_button.png', size_hint=(None, None), size=(200, 100), allow_stretch=True)
        tutorial_btn = ImageButton(source='assets/images/buttons/tutorial_button.png', size_hint=(None, None), size=(200, 100), allow_stretch=True)

        for btn in [play_btn, shop_btn, tutorial_btn]:
            btn.pos_hint = {'center_x': 0.5, 'center_y': 0.4}

        play_btn.bind(on_press=self.start_game)
        shop_btn.bind(on_press=self.open_shop)
        tutorial_btn.bind(on_press=self.show_tutorial)

        button_layout.add_widget(play_btn)
        button_layout.add_widget(shop_btn)
        button_layout.add_widget(tutorial_btn)

        # Add all widgets to vertical_layout
        vertical_layout.add_widget(self.preview_layout)
        vertical_layout.add_widget(self.score_label)
        vertical_layout.add_widget(button_layout)

        # Add vertical_layout to main layout
        main_layout.add_widget(vertical_layout)

        # Settings icon
        settings_size = Window.height * 0.107 
        settings_btn = ImageButton(
            source=resource_find('assets/images/buttons/setting.png'),
            size_hint=(None, None),
            size=(settings_size, settings_size),
            pos_hint={'right': 0.98, 'y': 0.02}
        )
        settings_btn.bind(on_press=self.show_settings)
        main_layout.add_widget(settings_btn)

        # Auto resize background
        Window.bind(size=self.update_bg_image)

    def on_enter(self):
        self.update_score_display()
        self.update_preview()
        
    from kivy.core.window import Window

    def update_score_display(self):
        app = App.get_running_app()
        if app and hasattr(app, 'data_manager'):
            best = app.data_manager.get_best_score()
            pts = app.data_manager.get_total_points()
            self.score_label.font_name = "assets/fonts/HeehawRegular.ttf"

            # Responsive font size
            best_font_size = int(Window.height * 0.07)
            total_font_size = int(Window.height * 0.05)

            self.score_label.text = (
                f'[size={best_font_size}][color=ffffff]Best Score: {best}[/color][/size]\n'
                f'[size={total_font_size}][color=ffffaa]Total Points: {pts}[/color][/size]'
            )

            # Center align
            self.score_label.halign = 'center'
            self.score_label.valign = 'middle'
            self.score_label.bind(size=self._update_label_text_size)

    def _update_label_text_size(self, instance, size):
        instance.text_size = size

    def update_preview(self):
        app = App.get_running_app()
        dm = app.data_manager

        skin_id = dm.get_equipped_skin()
        # Load cow skin preview image
        skin_path = f"assets/images/characters/{skin_id}.png" if skin_id else "assets/images/characters/bo.gif"
        
    def start_game(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')
        self.manager.current = 'game'

    def open_shop(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')
        self.manager.current = 'shop'

    def show_tutorial(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')
        self.manager.current = 'tutorial'

    def show_settings(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')
        self.manager.current = 'settings'

    def update_bg_image(self, *args):
        if hasattr(self, 'bg_parallax'):
            self.bg_parallax.on_resize()
        Window.bind(size=lambda *args: self.update_score_display())