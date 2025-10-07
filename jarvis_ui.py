import pygame
import math
import random
from enum import Enum


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 128, 255)
    CYAN = (0, 255, 255)
    ORANGE1 = (255, 165, 0)
    ORANGE2 = (255, 115, 0)
    GREEN1 = (0, 219, 0)
    GREEN2 = (4, 201, 4)
    PINK1 = (255, 182, 193)
    PINK2 = (255, 105, 180)
    PURPLE1 = (166, 0, 255)
    PURPLE2 = (176, 28, 255)


class JarvisUI:
    def __init__(self, width=1920, height=1080, fullscreen=False):
        """Initialize the Jarvis UI."""
        pygame.init()
        pygame.mixer.init()

        self.WIDTH = width
        self.HEIGHT = height

        if fullscreen:
            info = pygame.display.Info()
            self.WIDTH, self.HEIGHT = info.current_w, info.current_h
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption("Jarvis Interface")

        # Fonts
        self.font_large = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.font_small = pygame.font.Font(pygame.font.get_default_font(), 20)

        self.clock = pygame.time.Clock()

        # Rotating Circle Parameters
        self.center = (self.WIDTH // 2, self.HEIGHT // 2)
        self.max_radius = min(self.WIDTH, self.HEIGHT) // 3
        self.angle = 0
        self.speed = 1

        # Particle Parameters
        self.num_particles = 100
        self.particles = self._initialize_particles()

        # Pulse effect variables
        self.pulse_factor = 1
        self.pulse_speed = 0.05
        self.min_size = 3
        self.max_size = 3

        # Color Transition
        self.current_color_1 = list(Color.BLUE.value)
        self.current_color_2 = list(Color.CYAN.value)
        self.target_color_1 = list(Color.BLUE.value)
        self.target_color_2 = list(Color.CYAN.value)
        self.color_transition_speed = 10

        # State flags
        self.model_answering = False
        self.is_collided = False
        self.is_generating = False

        # Jarvis voice and responses
        self.jarvis_responses = [
            "Тук съм, как мога да помогна?",
            "Слушам, как мога да Ви асистирам?",
            "Тук съм, как мога да помогна?",
            "С какво мога да Ви бъда полезен?"
            # "Слушам шефе, как да помогна?"
        ]
        self.jarvis_voice = "Brian"

        # Status list
        self.status_list = []

        # Song information
        self.current_song = ""
        self.current_artist = ""
        self.current_progress = 0
        self.song_duration = 0

        # Selected model (no dropdown)
        self.selected_model = "Gemini"

    def _initialize_particles(self):
        """Initialize random particles."""
        return [
            {
                "x": random.randint(0, self.WIDTH),
                "y": random.randint(0, self.HEIGHT),
                "dx": random.uniform(-2, 2),
                "dy": random.uniform(-2, 2)
            }
            for _ in range(self.num_particles)
        ]

    def blend_color(self, current, target, speed):
        """Gradually transitions the current color toward the target color."""
        for i in range(3):
            diff = target[i] - current[i]
            if abs(diff) > speed:
                current[i] += speed if diff > 0 else -speed
            else:
                current[i] = target[i]

    def draw_particles(self, target_mode=False):
        """Draws particles on the surface."""
        for i, particle in enumerate(self.particles):
            if target_mode:
                # Calculate target circular positions
                target_x = self.center[0] + math.cos(
                    math.radians(self.angle + i * 360 / len(self.particles))) * self.max_radius
                target_y = self.center[1] + math.sin(
                    math.radians(self.angle + i * 360 / len(self.particles))) * self.max_radius

                # Smoothly move particles towards their circular positions
                particle["x"] += (target_x - particle["x"]) * 0.05
                particle["y"] += (target_y - particle["y"]) * 0.05

                # Pulse effect
                if self.pulse_factor < self.max_size:
                    self.pulse_factor = min(self.max_size, self.pulse_factor + self.pulse_speed)
                else:
                    self.pulse_factor = max(self.min_size, self.pulse_factor - self.pulse_speed)
            else:
                # Move particles randomly when in default mode
                particle["x"] += particle["dx"]
                particle["y"] += particle["dy"]

                # Keep particles within the screen bounds
                if particle["x"] <= 0 or particle["x"] >= self.WIDTH:
                    particle["dx"] *= -1
                if particle["y"] <= 0 or particle["y"] >= self.HEIGHT:
                    particle["dy"] *= -1

            # Draw the particle
            pygame.draw.circle(
                self.screen,
                tuple(self.current_color_2),
                (int(particle["x"]), int(particle["y"])),
                int(self.pulse_factor)
            )

    def set_response_state(self, model=None):
        """Update settings when the model is answering."""
        if model == "Gemini":
            self.target_color_1 = list(Color.GREEN1.value)
            self.target_color_2 = list(Color.GREEN2.value)
        elif model == "Llama3":
            self.target_color_1 = list(Color.PINK1.value)
            self.target_color_2 = list(Color.PINK2.value)
        elif model == "Deepseek":
            self.target_color_1 = list(Color.PURPLE1.value)
            self.target_color_2 = list(Color.PURPLE2.value)

        self.speed = 1
        self.is_collided = True
        self.angle += self.speed

    def set_thinking_state(self):
        """Update settings when the model is listening."""
        self.target_color_1 = list(Color.ORANGE1.value)
        self.target_color_2 = list(Color.ORANGE1.value)
        self.speed = 0.5
        self.is_collided = True
        self.angle += self.speed

    def set_default_state(self):
        """Update settings when the model is not answering."""
        self.target_color_1 = list(Color.BLUE.value)
        self.target_color_2 = list(Color.CYAN.value)
        self.speed = 1
        self.is_collided = False

    def draw_text(self, text, position, font, color):
        """Draws text onto the surface."""
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_progress_bar(self, x, y, width, height, progress, max_progress):
        """Draw a progress bar to represent the song timeline."""
        if max_progress > 0:
            progress_ratio = progress / max_progress
            progress_width = int(width * progress_ratio)
        else:
            progress_width = 0

        # Draw the empty progress bar (background)
        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, width, height))

        # Draw the filled progress bar (foreground)
        pygame.draw.rect(self.screen, Color.GREEN1.value, (x, y, progress_width, height))

    def update_status(self, new_status):
        """Add new status to the list (max 5 items)."""
        self.status_list.append(new_status)
        if len(self.status_list) > 5:
            self.status_list.pop(0)

    def update_song_info(self, song, artist, progress_ms, duration_ms):
        """Update the current song information."""
        self.current_song = song if song else ""
        self.current_artist = artist if artist else ""
        self.current_progress = progress_ms
        self.song_duration = duration_ms

    def render(self):
        """Main render method - call this every frame."""
        # Fill background
        self.screen.fill(Color.BLACK.value)

        # Toggle behavior based on state
        if self.is_generating:
            self.set_thinking_state()
        elif self.model_answering:
            self.set_response_state(self.selected_model)
        else:
            self.set_default_state()

        # Smooth Color Transition
        self.blend_color(self.current_color_1, self.target_color_1, self.color_transition_speed)
        self.blend_color(self.current_color_2, self.target_color_2, self.color_transition_speed)

        # Draw Particles
        self.draw_particles(target_mode=self.is_collided)

        # Draw Text
        self.draw_text("Vision Interface MK4", (10, 10), self.font_large, Color.WHITE.value)
        self.draw_text("System Status: All Systems Online", (10, 60), self.font_small, tuple(self.current_color_2))

        # Draw the list of statuses
        start_y = 90
        line_height = 30
        for index, status in enumerate(self.status_list):
            self.draw_text(status, (10, start_y + index * line_height), self.font_small, Color.WHITE.value)

        # Draw the progress bar for the song timeline
        progress_bar_x = (self.WIDTH - 700) // 2
        progress_bar_y = self.HEIGHT - 30
        self.draw_progress_bar(progress_bar_x, progress_bar_y, 700, 10, self.current_progress, self.song_duration)

        # Draw song information above the progress bar
        if self.current_song:
            song_surface = self.font_small.render(self.current_song, True, Color.WHITE.value)
            song_text_x = (self.WIDTH - song_surface.get_width()) // 2
            song_text_y = progress_bar_y - 30
            self.screen.blit(song_surface, (song_text_x, song_text_y))

        # Update Display
        pygame.display.flip()
        self.clock.tick(60)

    def quit(self):
        """Clean up pygame."""
        pygame.quit()