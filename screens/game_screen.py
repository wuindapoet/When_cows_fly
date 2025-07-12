import random
from kivy.resources import resource_find
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.app import App
from kivy.resources import resource_find
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from screens.background import ParallaxWidget, get_objects_background_speed
from kivy.uix.behaviors import ButtonBehavior

from screens.animated_sprites import AnimatedCow, AnimatedKite, get_ground_level, get_scaled_value, get_aspect_ratio

def get_gravity():
    return get_scaled_value(0.8)  # ADJUST GRAVITY

def get_jump_strength():
    return get_scaled_value(0.533)  # ADJUST JUMP STRENGTH

class ImageButton(ButtonBehavior, Image):
    pass

class Obstacle(Widget):
    def __init__(self, obstacle_type, **kwargs):
        super().__init__(**kwargs)
        self.obstacle_type = obstacle_type
        self.speed = get_objects_background_speed()
        self.size_hint = (None, None)
        
        # Special physics for different obstacles
        self.velocity_y = 0
        self.gravity = 0
        self.rotation_speed = 0

        # Set size and position based on obstacle type - all scaled to window height
        if self.obstacle_type == 'electric_wire':
            self.path = resource_find("assets/images/obstacles/wire_1.png")
            aspect_ratio = get_aspect_ratio(self.path)

            # Set size based on aspect ratio
            aspect_ratio = get_aspect_ratio(self.path)  
            
            wire_width = Window.width
            wire_height = wire_width / aspect_ratio  

            self.size = (wire_width, wire_height)
            margin_from_top = Window.height * 0.04  
            self.pos = (Window.width, Window.height - wire_height - margin_from_top)

            self.image = Image(source=self.path, size=self.size, pos=self.pos)
            self.add_widget(self.image)
  
            self.sparks = []
            num_sparks = random.randint(2, 4)  

            for _ in range(num_sparks):
                offset_x = random.uniform(0.1, 0.9) * self.width
                spark_y = self.y + self.height * 0.5  
                spark_pos = (self.x + offset_x, spark_y)

                spark = SparkEffect(
                    parent_widget=self,
                    image_pos=spark_pos,
                    scale_x=2.0,         # bigger
                    scale_y=0.12,        # higher
                    y_offset_ratio=0.12  # deeper
                )

            self.sparks.append((spark, offset_x, 0))
            self.bind(pos=self.update_graphics)

        elif self.obstacle_type == 'hole':
            self.path = resource_find("assets/images/obstacles/hole.png")
            aspect_ratio = get_aspect_ratio(self.path)
            hole_height = get_ground_level() + Window.height*0.02
            hole_width = hole_height*aspect_ratio  # ~300px at 750px height

            self.size = (hole_width, hole_height)
            self.pos = (Window.width, 0)
            
        elif self.obstacle_type == 'barrier':
            self.path = resource_find("assets/images/obstacles/barrier.png")
            aspect_ratio = get_aspect_ratio(self.path)           
            barrier_height = Window.height * 0.307  # ~230px at 750px height
            barrier_width = barrier_height * aspect_ratio  # ~200px at 750px height

            self.size = (barrier_width, barrier_height)
            self.pos = (Window.width, get_ground_level())
            
        elif self.obstacle_type == 'kite':
            return

        elif self.obstacle_type == 'bird':
            self.speed = get_scaled_value(1.3)  # 1200 at 750px height
            self.path = resource_find("assets/images/obstacles/bird.png")
            aspect_ratio =  get_aspect_ratio(self.path)
            
            bird_height = Window.height * 0.07  
            bird_width = bird_height * aspect_ratio  # ~70px at 750px height
            self.size = (bird_width, bird_height)
            
            # Bird position range scaled to window height
            min_y = int(get_ground_level() + Window.height * 0.053)  # 40px above ground at 750px
            max_y = int(Window.height - Window.height * 0.107)  # 80px from top at 750px
            
            self.pos = (Window.width, random.randint(min_y, max_y))


        self.initial_y = self.y
        self.rotation_angle = 0
        
        if self.obstacle_type not in ['electric_wire', 'kite']:  # Đã tạo image ở trên rồi
            self.image = Image(source=resource_find(self.path), size=self.size, pos=self.pos)
            self.add_widget(self.image)

        self.bind(pos=self.update_graphics)
        
    def update_graphics(self, *args):
        if hasattr(self, 'image'):
            self.image.pos = self.pos

        if hasattr(self, 'sparks'):
            for spark, offset_x, offset_y in self.sparks:
                new_x = self.x + offset_x
                new_y = self.y + offset_y
                spark.update_position((new_x, new_y))

    def update(self, dt, speed_multiplier=1.0):
        self.x -= self.speed * speed_multiplier * dt

        if self.obstacle_type == 'bird':
            self.rotation_angle += 120 * dt

        if self.obstacle_type == 'electric_wire':
            if self.right < 0:
                self.x += self.width * (int(Window.width // self.width) + 2)
            return False

        return self.x < -self.width

    def toggle_spark_effect(self, dt):
        if hasattr(self, 'spark_instruction') and self.spark_images:
            new_source = random.choice(self.spark_images)
            self.spark_instruction.source = new_source
            if self.spark_instruction.a == 0:
                self.spark_instruction.a = 1  # show
            else:
                self.spark_instruction.a = 0  # hide


class Collectible(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = get_objects_background_speed()  
        
        # Size scaled to window height
        collectible_size = Window.height * 0.067  # ~50px at 750px height
        self.size = (collectible_size, collectible_size)
        self.size_hint = (None, None)
        
        # Position range scaled to window height
        min_y = int(Window.height * 0.107)  # 80px from bottom at 750px
        max_y = int(Window.height - Window.height * 0.107)  # 80px from top at 750px
        
        self.pos = (Window.width, random.randint(min_y, max_y))

        self.image = Image(
            source=resource_find("assets/images/obstacles/collectible.png"),
            size=self.size,
            size_hint=(None, None),
            pos=self.pos
        )
        self.add_widget(self.image)
        self.bind(pos=self.update_graphics)

    def update_graphics(self, *args):
        
        if hasattr(self, 'image'):
            self.image.pos = self.pos
        if hasattr(self, 'spark_image'):
            self.spark_image.pos = self.pos

        
    def update(self, dt, speed_multiplier=1.0):
        self.x -= self.speed * speed_multiplier * dt
        return self.x < -self.width

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_running = False
        self.score = 0
        self.lives = 3
        self.speed_multiplier = 1.0
        self.obstacles = []
        self.collectibles = []
        self.spawn_timer = 0
        self.collectible_spawn_timer = 0

        self.cow = None
        self.parallax = None
        self.build_ui()
        self.is_paused = False

    def build_ui(self):
        # UI Layout
        ui_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            pos_hint={'top': 1.05},
            padding=[Window.width * 0.02, Window.height * 0.013],  # Scaled padding
            spacing=Window.width * 0.01  # Scaled spacing
        )
        
        # Score display
        font_size = Window.height * 0.05  # Scale font size to window height
        self.score_label = Label(
            text='Score: 0',
            font_size=font_size,
            color=(0.345, 0.192, 0.004, 1),  # #583101
            font_name=resource_find('assets/fonts/HeehawRegular.ttf'),
            markup=True,
            size_hint=(0.7, 1),
            halign='left',
            valign='middle',
            pos_hint={'top': 0.65}
        )
        self.score_label.bind(size=self._update_label_text_align)

        # Lives UI - scaled to window height
        self.hearts = []
        heart_size = Window.height * 0.053  # ~40px at 750px height
        hearts_layout_width = heart_size * 3 + Window.width * 0.01  # 3 hearts + spacing
        
        self.hearts_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(hearts_layout_width, heart_size),
            spacing=Window.width * 0.005,  # Scaled spacing
            pos_hint={'x': 0.01, 'top': 0.45}
        )

        for _ in range(3):
            heart = Image(
                source=resource_find('assets/images/icons/live.png'),
                size_hint=(None, None),
                size=(heart_size, heart_size)
            )
            self.hearts.append(heart)
            self.hearts_layout.add_widget(heart)

        ui_layout.add_widget(self.score_label)
        ui_layout.add_widget(self.hearts_layout)
        self.add_widget(ui_layout)
        
        # Settings icon - scaled to window height
        settings_size = Window.height * 0.107  # ~80px at 750px height
        self.game_settings_btn = ImageButton(
            source=resource_find('assets/images/buttons/setting.png'),
            size_hint=(None, None),
            size=(settings_size, settings_size),
            pos_hint={'right': 0.98, 'y': 0.02}
        )
        self.game_settings_btn.bind(on_press=self.show_settings)
        self.add_widget(self.game_settings_btn, index=0)

    def _update_label_text_align(self, instance, value):
        instance.text_size = instance.size

    def on_enter(self):
        if self.is_paused:
            self.resume_game()
        else:
            self.start_game()
            App.get_running_app().sound_manager.play_background_music()
    
    def on_leave(self):
        self.stop_game()
    
    def start_game(self):
        self.game_running = True
        self.score = 0
        self.lives = 3
        self.speed_multiplier = 1.0
        self.spawn_timer = 0
        self.collectible_spawn_timer = 0

        # Get skin and background
        app = App.get_running_app()
        skin_id = app.data_manager.get_equipped_skin()
        print("Equipped skin_id:", skin_id)
        
        # Create new AnimatedCow with skin
        if hasattr(self, 'cow') and self.cow:
            self.cow.stop_animation()  # Stop animation before removing
            self.remove_widget(self.cow)

        # Create animated cow with the selected skin - positioned relative to window
        self.cow = AnimatedCow(skin_id=skin_id or "bo")
        cow_x = Window.width * 0.1  # Position cow at 10% from left edge
        self.cow.pos = (cow_x, self.cow.ground_level)
        self.cow.game_started = False
        self.add_widget(self.cow)
        print("Added animated cow with skin:", skin_id)

        # Create parallax background
        if hasattr(self, 'parallax') and self.parallax:
            self.remove_widget(self.parallax)
        
        self.parallax = ParallaxWidget(cow=self.cow)
        self.add_widget(self.parallax, index=len(self.children))  # Add to back

        # Clear old obstacles and collectibles
        for obstacle in self.obstacles:
            if hasattr(obstacle, 'stop_animation'):
                obstacle.stop_animation()
            self.remove_widget(obstacle)
        for collectible in self.collectibles:
            self.remove_widget(collectible)
        self.obstacles.clear()
        self.collectibles.clear()

        sample_wire = Obstacle(obstacle_type='electric_wire')
        wire_width = sample_wire.width
        num_wires = int(Window.width // wire_width) + 2  # ensure full coverage

        for i in range(num_wires):
            wire = Obstacle(obstacle_type='electric_wire')
            wire.x = i * wire.width  
            self.obstacles.append(wire)
            cow_index = self.children.index(self.cow)
            self.add_widget(wire, index=cow_index + 1)

        # UI
        self.update_ui()

        # Game loop
        Clock.schedule_interval(self.update_game, 1.0 / 60.0)

    def stop_game(self):
        self.game_running = False
        Clock.unschedule(self.update_game)
        
        # Stop all animations
        if self.cow:
            self.cow.stop_animation()
        for obstacle in self.obstacles:
            if hasattr(obstacle, 'stop_animation'):
                obstacle.stop_animation()
    
    def pause_game(self):
        if self.game_running and not self.is_paused:  
            Clock.unschedule(self.update_game)
            self.game_running = False
            self.is_paused = True
            # Pause animations
            if self.cow:
                self.cow.stop_animation()
            for obstacle in self.obstacles:
                if hasattr(obstacle, 'stop_animation'):
                    obstacle.stop_animation()
            
    def resume_game(self):
        if not self.game_running and self.is_paused:
            Clock.schedule_interval(self.update_game, 1.0 / 60.0)
            self.game_running = True
            self.is_paused = False
            # Resume animations
            if self.cow:
                self.cow.start_animation()
            for obstacle in self.obstacles:
                if hasattr(obstacle, 'start_animation'):
                    obstacle.start_animation()

    def update_game(self, dt):
        if not self.game_running:
            return

        # Update cow
        if self.cow:
            self.cow.update(dt)

        # Update speed based on score
        self.speed_multiplier = 1.0 + (self.score // 10) * 0.2

        # Update ground speed multiplier
        if self.parallax and hasattr(self.parallax, 'ground') and self.parallax.ground:
            self.parallax.ground.set_speed_multiplier(self.speed_multiplier)

        # Spawn obstacles
        self.spawn_timer += dt
        if self.spawn_timer >= 5.0 / self.speed_multiplier:
            self.spawn_obstacle()
            self.spawn_timer = 0

        # Spawn collectibles
        self.collectible_spawn_timer += dt
        if self.collectible_spawn_timer >= 3.0:
            self.spawn_collectible()
            self.collectible_spawn_timer = 0

        # Update obstacles
        for obstacle in self.obstacles[:]:
            if obstacle.update(dt, self.speed_multiplier):
                if hasattr(obstacle, 'stop_animation'):
                    obstacle.stop_animation()
                self.remove_widget(obstacle)
                self.obstacles.remove(obstacle)
            else:
                self.check_collision(obstacle)

        # Update collectibles
        for collectible in self.collectibles[:]:
            if collectible.update(dt, self.speed_multiplier):
                self.remove_widget(collectible)
                self.collectibles.remove(collectible)
            else:
                self.check_collectible_collision(collectible)
    
    def spawn_obstacle(self, obstacle_type=None):
        if obstacle_type is None:
            obstacle_types = ['hole', 'kite', 'bird', 'barrier']
            obstacle_type = random.choice(obstacle_types)
        
        if obstacle_type == 'kite':
            # Create animated kite
            obstacle = AnimatedKite()
            obstacle.obstacle_type = 'kite'  # Set type for collision detection
        else:
            obstacle = Obstacle(obstacle_type=obstacle_type)
        
        self.obstacles.append(obstacle)
        try:
            cow_index = self.children.index(self.cow)
            if obstacle.obstacle_type == 'hole':
                self.add_widget(obstacle, index=cow_index + 1)
            else:
                self.add_widget(obstacle, index=cow_index)
        except ValueError:
            self.add_widget(obstacle)    
            
    def spawn_collectible(self):
        collectible = Collectible()
        self.collectibles.append(collectible)
        try:
            cow_index = self.children.index(self.cow)
            self.add_widget(collectible, index=cow_index + 1)
        except ValueError:
            self.add_widget(collectible)    
    
    def is_spawn_position_safe(self):
        if not self.cow:
            return True
            
        cow_spawn_center_x = self.cow.original_x + self.cow.width / 2
        
        for obstacle in self.obstacles:
            if hasattr(obstacle, 'obstacle_type') and obstacle.obstacle_type == 'hole':
                hole_left = obstacle.x
                hole_right = obstacle.right
                
                # Check if spawn position overlaps with hole        
                if hole_left <= cow_spawn_center_x <= hole_right:
                    return False
        return True
            
    def check_collision(self, obstacle):
        if not self.cow or not self.cow.collide_widget(obstacle):
            return
            
        print('o no, cow hit an obstacle!')
        app = App.get_running_app()
        
        obstacle_type = getattr(obstacle, 'obstacle_type', 'unknown')
        
        if obstacle_type == 'electric_wire':
            # self.cow.start_falling(obstacle_type)
            self.cow.start_electric_shock()
            self.cow.start_flashing()  # nếu muốn nháy nháy thêm
            self.cow.start_falling('hit')
            self.play_sound_async('hit')

            Clock.schedule_once(lambda dt: self.game_over(), 0.4)
            self.play_sound_async('game_over')

            return
        elif obstacle_type == 'hole':
            # When cow collides with hole, move it to center first, then fall
            hole_center_x = obstacle.x + obstacle.width / 2
            cow_center_offset = self.cow.width / 2
            
            # Move cow to center of hole before falling
            self.cow.x = hole_center_x - cow_center_offset
            self.cow.start_falling('hole')
            print('Cow hit hole! Moving to center and falling.')
            return
        
        else:
            self.play_sound_async('hit')
            # Make cow fall
            self.cow.start_falling('hit')
            
            # Remove obstacle
            if hasattr(obstacle, 'stop_animation'):
                obstacle.stop_animation()
            self.remove_widget(obstacle)
            self.obstacles.remove(obstacle)
            
            # Lose life after a short delay
            Clock.schedule_once(lambda dt: self.lose_life(), 0.5)

    def lose_life(self):
        self.lives -= 1
        self.update_ui()
        
        # Reset cow to ground
        if self.cow:
            self.cow.reset_to_ground()
            self.cow.pos = (Window.height * 0.133, self.cow.ground_level)
        
        if self.lives <= 0:
            self.game_over()
    
    def check_collectible_collision(self, collectible):
        if self.cow and self.cow.collide_widget(collectible):
            self.score += 1
            self.update_ui()
            self.remove_widget(collectible)
            self.collectibles.remove(collectible)
    
    def play_sound_async(self, sound_name):
        try:
            app = App.get_running_app()
            if app and hasattr(app, 'sound_manager'):
                app.sound_manager.play_sound(sound_name)
        except Exception:
            # Silently ignore sound errors to prevent game crashes
            pass
    
    def game_over(self):
        self.stop_game()
        
        # Save score data
        app = App.get_running_app()
        if app and hasattr(app, 'data_manager'):
            app.data_manager.add_points(self.score)
            is_new_high_score = self.score > app.data_manager.get_best_score()
            app.data_manager.set_best_score(self.score)
            
            # Pass data to game over screen
            game_over_screen = self.manager.get_screen('game_over')
            game_over_screen.set_score_data(self.score, is_new_high_score)
        
        self.manager.current = 'game_over'
    
    def update_ui(self):
        # Update lives display
        for i in range(3):
            if i < self.lives:
                self.hearts[i].source = resource_find('assets/images/icons/live.png')
            else:
                self.hearts[i].source = resource_find('assets/images/icons/die.png')

        # Update score
        self.score_label.text = f'Score: {self.score}'

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True

        if self.game_running and self.cow:
            self.cow.jump()
            return True  

        return False
    
    def on_space_press(self):
        if self.game_running and self.cow:
            self.cow.jump()

    def show_settings(self, *args):
        self.pause_game()
        self.manager.current = 'game_settings'

    def reset_game(self):
        self.stop_game()  
        self.score = 0
        self.lives = 3
        self.is_paused = False
        self.game_running = False

        self.obstacles.clear()
        self.collectibles.clear()

        self.canvas.clear()
        self.clear_widgets()
        self.build_ui()

        if self.cow:
            self.cow.reset_to_ground()

import random
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.resources import resource_find

class SparkEffect:
    def __init__(self, parent_widget, image_pos, scale_x=3.0, scale_y=0.1, y_offset_ratio=0.25):
        self.spark_images = [
            resource_find("assets/images/obstacles/light_1.png"),
            resource_find("assets/images/obstacles/light_2.png"),
            resource_find("assets/images/obstacles/light_3.png"),
        ]

        spark_width =  200
        spark_height = 100

        self.image = Image(
            source=random.choice(self.spark_images),
            size_hint=(None, None),
            size=(spark_width, spark_height),
            pos= image_pos,
            opacity=1
        )

        parent_widget.add_widget(self.image, index=0)
        self._clock_event = Clock.schedule_interval(self.toggle_spark, 0.5)

    def toggle_spark(self, dt):
        self.image.source = random.choice(self.spark_images)
        self.image.opacity = 1 if self.image.opacity == 0 else 0

    def update_position(self, pos):
        self.image.pos = pos

    def stop(self):
        if self._clock_event:
            self._clock_event.cancel()
        if self.image.parent:
            self.image.parent.remove_widget(self.image)
