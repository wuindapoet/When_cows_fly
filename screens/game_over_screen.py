from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.animation import Animation
from screens.background import ParallaxWidget
from kivy.core.window import Window


class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_score = 0
        self.is_new_high_score = False
        self.build_ui()
 
    def build_ui(self):
        # Parallax background
        self.bg_parallax = ParallaxWidget()
        self.add_widget(self.bg_parallax)

        # Overlay
        with self.canvas:
            self.overlay_color = Color(0, 0, 0, 0.2)
            self.overlay_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_overlay, size=self.update_overlay)

        # Layout chính
        main_layout = FloatLayout()
        self.add_widget(main_layout)

        frame_layout = FloatLayout(
            size_hint=(0.5, 0.6),  
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
    )
        main_layout.add_widget(frame_layout)

        frame_img = Image(
            source='assets/images/backgrounds/gameover_background.png',
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,           
            keep_ratio= False  
        )
        frame_layout.add_widget(frame_img)
      

        # Font auto-scale
        font_size = min(Window.width, Window.height) * 0.4

        # Score box
        score_box = BoxLayout(
            orientation='vertical',
            size_hint=(0.6, 0.4),
            pos_hint={'center_x': 0.55, 'center_y': 0.5},
            spacing=Window.height * 0.0005
        )

        # Your Score
        your_score_row = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 1),
            spacing=Window.width * 0.005
        )
        self.your_score_icon = Image(
            source='assets/images/buttons/total_score.png',
            size_hint=(None, 1),
            width=Window.width * 0.045
        )
        self.your_score_label = Label(
            text='',
            markup=True,
            font_name='assets/fonts/HeehawRegular.ttf',
            font_size=font_size,
            halign='left',
            valign='middle',
            size_hint=(1, 1),
            # text_size=(1, 1)  # set cứng vùng hiển thị chữ
        )

        self.your_score_label.bind(size=self._update_text_align)
        your_score_row.add_widget(self.your_score_icon)
        your_score_row.add_widget(self.your_score_label)

        # Best Score
        best_score_row = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 1),
            spacing=Window.width * 0.005
        )
        self.best_score_icon = Image(
            source='assets/images/buttons/best_score.png',
            size_hint=(None, 1),
            width=Window.width * 0.045
        )
        self.best_score_label = Label(
            text='',
            markup=True,
            font_name='assets/fonts/HeehawRegular.ttf',
            font_size=font_size,
            halign='left',
            valign='middle',
            size_hint=(1, 1),
            # text_size=(1,1)  # set cứng vùng hiển thị chữ
        )
        self.best_score_label.bind(size=self._update_text_align)
        best_score_row.add_widget(self.best_score_icon)
        best_score_row.add_widget(self.best_score_label)

        score_box.add_widget(your_score_row)
        score_box.add_widget(best_score_row)
        frame_layout.add_widget(score_box)


        # Play Again, Main Menu, Shop buttons
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(0.7, 0.3 ), 
            pos_hint={'center_x': 0.5, 'y': 0.055},  # Sát đáy frame_layout
            spacing=10 
        )

        play_btn = Button(
            size_hint=(0.4, 1), 
            pos_hint={'center_x': 0.25, 'center_y': 0.36},
            background_normal='assets/images/buttons/return.png',
            background_color=(1, 1, 1, 1),
            text=''
        )
        play_btn.bind(on_press=self.play_again)

        home_btn = Button(
            size_hint=(0.4,1), 
            pos_hint={'center_x': 0.5, 'center_y': 0.36},
            background_normal='assets/images/buttons/home.png',
            background_color=(1, 1, 1, 1),
            text=''
        )
        home_btn.bind(on_press=self.go_to_main_menu)

        shop_btn = Button(
            size_hint=(0.4, 1),
            pos_hint={'center_x': 0.75, 'center_y': 0.36},
            background_normal='assets/images/buttons/shop.png',
            background_color=(1, 1, 1, 1),
            text=''
        )
        shop_btn.bind(on_press=self.go_to_shop)

        buttons_layout.add_widget(play_btn)
        buttons_layout.add_widget(home_btn)
        buttons_layout.add_widget(shop_btn)

        frame_layout.add_widget(buttons_layout)

        self.update_font_size()  
        Window.bind(on_resize=self.update_font_size)

    def update_font_size(self, *args):
        scale = min(Window.width, Window.height)
        new_font_size = scale * 0.045 
        self.your_score_label.font_size = new_font_size
        self.best_score_label.font_size = new_font_size

    def _update_text_align(self, instance, value):
        instance.text_size = instance.size
        instance.texture_update()


    def update_overlay(self, *args):
        self.overlay_rect.pos = self.pos
        self.overlay_rect.size = self.size

    def set_score_data(self, current_score, is_new_high_score):
        self.current_score = current_score
        self.is_new_high_score = is_new_high_score

    def on_enter(self):
        self.update_score_display()
        if self.is_new_high_score:
            self.animate_high_score()

    def update_score_display(self):
        app = App.get_running_app()
        best_score = 0
        if app and hasattr(app, 'data_manager'):
            best_score = app.data_manager.get_best_score()

        self.your_score_label.text = f'[color=ffffff]Your Score: {self.current_score}[/color]'
        self.best_score_label.text = f'[color=cccccc]Best Score: {best_score}[/color]'

    def animate_high_score(self):
        anim = Animation(opacity=0.3, duration=0.5) + Animation(opacity=1, duration=0.5)
        anim.repeat = True
        anim.start(self.best_score_icon)

    def play_again(self, button):
        app = App.get_running_app()
        if app and hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')
        Animation.stop_all(self.best_score_icon)
        self.manager.current = 'game'

    def go_to_main_menu(self, button):
        app = App.get_running_app()
        if app and hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')
        Animation.stop_all(self.best_score_icon)
        self.manager.current = 'main_menu'

    def go_to_shop(self, button):
        app = App.get_running_app()
        if app and hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')
        Animation.stop_all(self.best_score_icon)
        self.manager.current = 'shop'