import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window

from kivy.logger import Logger
from kivy.clock import Clock

from screens.main_menu_screen import MainMenuScreen
from screens.game_screen import GameScreen
from screens.shop_screen import ShopScreen
from screens.game_over_screen import GameOverScreen
from screens.tutorial_screen import TutorialScreen  
from screens.settings_screen import SettingsScreen
from screens.game_settings_screen import GameSettingsScreen
from screens.background import ParallaxWidget
from kivy.uix.floatlayout import FloatLayout

from utils.data_manager import DataManager
from utils.sound_manager import SoundManager
Window.size = (800,600)

class WhenCowsFlyApp(App):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = DataManager()
        self.sound_manager = SoundManager()
        
    def build(self):
        root = FloatLayout()
        
        self.parallax_bg = ParallaxWidget()
        root.add_widget(self.parallax_bg)

        self.screen_manager = ScreenManager(transition=FadeTransition())

        self.screen_manager.add_widget(MainMenuScreen(name='main_menu'))
        self.screen_manager.add_widget(GameScreen(name='game'))
        self.screen_manager.add_widget(ShopScreen(name='shop'))
        self.screen_manager.add_widget(GameOverScreen(name='game_over'))
        self.screen_manager.add_widget(TutorialScreen(name='tutorial'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        self.screen_manager.add_widget(GameSettingsScreen(name='game_settings'))
         
        self.screen_manager.current = 'main_menu'

        root.add_widget(self.screen_manager)

        Window.bind(on_key_down=self.on_key_down)

        Logger.info("WhenCowsFly: Application built successfully")
        return root
    
    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 32:
            current_screen = self.screen_manager.get_screen(self.screen_manager.current)
            if hasattr(current_screen, 'on_space_press'):
                current_screen.on_space_press()
        
        elif key == 27:
            return self.on_back_button()
        
        return False

    def on_back_button(self):
        current = self.screen_manager.current

        if current == 'main_menu':
            return False
        elif current == 'game':
            game_screen = self.screen_manager.get_screen('game')
            if hasattr(game_screen, 'restart_game'):
                game_screen.restart_game()
            self.screen_manager.current = 'main_menu'
            return True
        else:
            self.screen_manager.current = 'main_menu'
            return True
    
    def on_start(self):
        Logger.info("WhenCowsFly: App started")
        self.data_manager.load_data()
        self.sound_manager.load_sounds()
        self.sound_manager.play_background_music()
    
    def on_stop(self):
        Logger.info("WhenCowsFly: App stopping")
        self.data_manager.save_data()
    
    def on_pause(self):
        if self.screen_manager.current == 'game':
            game_screen = self.screen_manager.get_screen('game')
            if hasattr(game_screen, 'pause_game'):
                game_screen.pause_game()
        return True
    
    def on_resume(self):
        if self.screen_manager.current == 'game':
            game_screen = self.screen_manager.get_screen('game')
            if hasattr(game_screen, 'resume_game'):
                game_screen.resume_game()
print("window.width", Window.width, "window.height", Window.height)
if __name__ == '__main__':
    WhenCowsFlyApp().run()