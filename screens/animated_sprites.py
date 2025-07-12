from PIL import Image as PILImage
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.resources import resource_find
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.resources import resource_find
import random


def get_aspect_ratio(image_path):
    with PILImage.open(image_path) as img:
        width, height = img.size
        return width/height

def get_scaled_position(x_ratio, y_ratio):
    x = Window.width * x_ratio
    y = Window.height * y_ratio
    return (x, y)

def get_ground_level():
    return Window.height * 0.133  # ~100px at 750px height

def get_scaled_value(base_value_ratio):
    return Window.height * base_value_ratio

# PARAMETERS
FRAME_DURATION = 0.2
SPEED = get_scaled_value(0.4) 

class AnimatedSprite(Widget):
    def __init__(self, base_path, frame_count=4, frame_duration=FRAME_DURATION, **kwargs):
        super().__init__(**kwargs)
        
        self.base_path = base_path
        self.frame_count = frame_count
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.animation_time = 0
        
        # Load all frame paths
        self.frame_paths = []
        for i in range(frame_count):
            frame_path = f"{base_path}/{i}.png"
            if resource_find(frame_path):
                self.frame_paths.append(frame_path)
            else:
                print(f"Warning: Frame not found: {frame_path}")
                # Use first frame as fallback
                if i == 0:
                    self.frame_paths.append(f"{base_path}/0.png")
                else:
                    self.frame_paths.append(self.frame_paths[0])
        
        # Create the image widget
        self.image = Image(
            source=resource_find(self.frame_paths[0]) if self.frame_paths else "",
            size=self.size,
            pos=self.pos
        )
        self.add_widget(self.image)
        
        # Start animation
        self.animation_event = Clock.schedule_interval(self.update_animation, 1.0/60.0)
        
        # Bind position and size changes
        self.bind(pos=self.update_graphics, size=self.update_graphics)
    
    def update_graphics(self, *args):
        if hasattr(self, 'image'):
            self.image.pos = self.pos
            self.image.size = self.size
    
    def update_animation(self, dt):
        if not self.frame_paths:
            return
            
        self.animation_time += dt
        
        if self.animation_time >= self.frame_duration:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frame_paths)
            
            # Update image source
            new_source = resource_find(self.frame_paths[self.current_frame])
            if new_source != self.image.source:
                self.image.source = new_source
    
    def stop_animation(self):
        if hasattr(self, 'animation_event'):
            Clock.unschedule(self.animation_event)
    
    def start_animation(self):
        self.stop_animation()
        self.animation_event = Clock.schedule_interval(self.update_animation, 1.0/60.0)
    
    def set_frame(self, frame_index):
        if 0 <= frame_index < len(self.frame_paths):
            self.current_frame = frame_index
            self.image.source = resource_find(self.frame_paths[frame_index])


class AnimatedCow(AnimatedSprite):
    def __init__(self, skin_id="bo", **kwargs):
        cow_pat = f"assets/images/characters/{skin_id}/0.png"
        cow_path = resource_find(cow_pat)
        aspect_ratio = get_aspect_ratio(cow_path)
        self.cow_height = Window.height * 0.183  # ~137px at 750px height
        self.cow_width = self.cow_height * aspect_ratio 

       
        # Apply size before calling super
        kwargs['size'] = (self.cow_width, self.cow_height)
        kwargs['size_hint'] = (None, None)
        
        # Determine base path based on skin_id
        base_path = f"assets/images/characters/{skin_id}"

        
        super().__init__(
            base_path=resource_find(base_path),
            frame_count=4,
            frame_duration=FRAME_DURATION,
            **kwargs
        )
        
        self.skin_id = skin_id
        
        # Cow-specific properties - scaled based on window height
        self.velocity_y = 0
        self.gravity = get_scaled_value(0.8)  
        self.jump_strength = get_scaled_value(0.533)  
        self.ground_level = get_ground_level()
        self.is_falling = False
        self.fall_reason = None
        self.game_started = False
        
        # Store original spawn position for proper reset
        self.original_x = Window.width * 0.5 - self.size[0] * 0.5
        self.original_y = self.ground_level
        
        # Hole-specific tracking
        self.hole_fall_start_x = None
        self.in_hole_phase = False
        self.fell_in_hole = False
        self.hole_respawn_delay = 0
        
        # Flashing effect properties
        self.is_flashing = False
        self.flash_timer = 0
        self.flash_duration = 1.0
        self.flash_interval = 0.1
        # Electric shock effect
        self.is_shocked = False
        self.shock_timer = 0
        self.shock_duration = 0.6  # Giật điện trong 0.6s
        
        self.pos = (self.original_x, self.original_y)
    
    def update(self, dt):
        # Call parent animation update
        super().update_animation(dt)
        
        if not self.game_started:
            return

        # Handle respawn delay after hole fall
        if self.fell_in_hole:
            self.hole_respawn_delay -= dt
            if self.hole_respawn_delay <= 0:
                if self.parent and self.parent.is_spawn_position_safe():
                    self.fell_in_hole = False
                    self.hole_respawn_delay = 0
                    if self.parent:
                        self.parent.lose_life()
                    return
                else:
                    self.hole_respawn_delay = 0.5
            return
        # Handle electric shock effect
        if self.is_shocked:
            self.shock_timer += dt
            if self.shock_timer >= self.shock_duration:
                self.is_shocked = False
                self.shock_timer = 0
                # self.update_graphics()  # Khôi phục lại animation bình thường

        # Handle flashing effect
        if self.is_flashing:
            self.flash_timer += dt
            flash_cycle = int(self.flash_timer / self.flash_interval)
            self.image.opacity = 0.3 if flash_cycle % 2 == 0 else 1.0
            
            if self.flash_timer >= self.flash_duration:
                self.is_flashing = False
                self.flash_timer = 0
                self.image.opacity = 1.0

        # Apply gravity
        self.velocity_y -= self.gravity * dt
        self.y += self.velocity_y * dt

        # Handle falling logic
        if self.is_falling and self.fall_reason == 'hole':
            if self.hole_fall_start_x is None:
                self.hole_fall_start_x = self.x
                self.in_hole_phase = True
            
            if self.in_hole_phase and self.top >= 0:
                self.x -= get_scaled_value(0.267) * dt  # 200 at 750px height
            
            elif self.top < 0 and self.in_hole_phase:
                self.in_hole_phase = False
                self.fell_in_hole = True
                self.hole_respawn_delay = 1.5
                return
        else:
            # Normal ground collision
            if self.y <= self.ground_level:
                self.y = self.ground_level
                self.velocity_y = 0

    def jump(self):
        if self.is_shocked:
            return
        if not self.game_started:
            self.game_started = True

        if not self.is_falling and not self.fell_in_hole:
            self.velocity_y = self.jump_strength
  
    def start_falling(self, reason='hit'):
        self.is_falling = True
        self.fall_reason = reason
        
        if reason == 'hole':
            self.velocity_y = -get_scaled_value(0.4)  # -300 at 750px height
            self.hole_fall_start_x = None
            self.in_hole_phase = False
        
        if reason != 'hole':
            self.start_flashing()

    def start_flashing(self):
        self.is_flashing = True
        self.flash_timer = 0

    def reset_to_ground(self):
        self.pos = (self.original_x, self.original_y)
        self.velocity_y = 0
        self.is_falling = False
        self.fall_reason = None
        self.is_flashing = False
        self.flash_timer = 0
        self.image.opacity = 1.0
        
        # Reset hole-specific tracking
        self.hole_fall_start_x = None
        self.in_hole_phase = False
        self.fell_in_hole = False
        self.hole_respawn_delay = 0
        
        self.update_graphics()

    def start_electric_shock(self):
        self.is_shocked = True
        self.velocity_y = 0
        self.size = (self.cow_width*1.4, self.cow_height*1.4)
        self.shock_timer = 0
        self.image.source = resource_find("assets/images/characters/giatdien.png")
        self.image.opacity = 1.0


class AnimatedKite(AnimatedSprite):    
    def __init__(self, **kwargs):
        kite_path = resource_find("assets/images/obstacles/kite/0.png")
        aspect_ratio = get_aspect_ratio(kite_path)
        kite_height = Window.height * 0.2  # ~137px at 750px height
        kite_width = kite_height * aspect_ratio 
        
        kwargs['size'] = (kite_width, kite_height)
        kwargs['size_hint'] = (None, None)
        
        super().__init__(
            base_path=resource_find("assets/images/obstacles/kite"),
            frame_count=4,
            frame_duration=FRAME_DURATION,
            **kwargs
        )
        
        # Kite-specific properties - scaled based on window height
        
        self.speed = SPEED  # 300 at 750px height
        
        start_x = Window.width * random.uniform(0.4, 0.9)
        start_y = Window.height - random.randint(int(Window.height * 0.067), int(Window.height * 0.133))
        self.pos = (start_x, start_y)
        
        if start_x < 0.6 * Window.width:
            self.gravity = get_scaled_value(1.333) * random.uniform(0.8, 1)  # 1000 at 750px height
        else:
            self.gravity = get_scaled_value(0.8) * random.uniform(0.8, 1)  # 600 at 750px height
            
        self.velocity_y = 0
        self.rotation_speed = random.uniform(180, 360)
        self.horizontal_drift = random.uniform(
            get_scaled_value(0.067), get_scaled_value(0.133)  # 50-100 at 750px height
        )
        self.rotation_angle = 0
    
    def update(self, dt, speed_multiplier=1.0):
        # Call parent animation update
        super().update_animation(dt)
        
        # Update position
        self.x -= self.speed * speed_multiplier * dt
        
        # Apply gravity and drift
        self.velocity_y -= self.gravity * dt
        self.velocity_y = max(self.velocity_y, -get_scaled_value(0.133))  # -100 at 750px height
        self.y += self.velocity_y * dt
        self.rotation_angle += self.rotation_speed * dt
        self.x -= self.horizontal_drift * dt
        
        # Return True if off screen
        return self.x < -self.width


# Helper functions to create animated sprites
def create_animated_cow(skin_id="bo", **kwargs):
    return AnimatedCow(skin_id=skin_id, **kwargs)

def create_animated_kite(**kwargs):
    return AnimatedKite(**kwargs)