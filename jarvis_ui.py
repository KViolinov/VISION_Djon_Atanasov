# # old design
#
# # import pygame
# # import math
# # import random
# # from enum import Enum
# # import difflib
# #
# #
# # class Color(Enum):
# #     BLACK = (0, 0, 0)
# #     WHITE = (255, 255, 255)
# #     BLUE = (0, 128, 255)
# #     CYAN = (0, 255, 255)
# #     ORANGE1 = (255, 165, 0)
# #     ORANGE2 = (255, 115, 0)
# #     GREEN1 = (0, 219, 0)
# #     GREEN2 = (4, 201, 4)
# #     PINK1 = (255, 182, 193)
# #     PINK2 = (255, 105, 180)
# #     PURPLE1 = (166, 0, 255)
# #     PURPLE2 = (176, 28, 255)
# #
# #
# # class JarvisUI:
# #     def __init__(self, width=1920, height=1080, fullscreen=False):
# #         """Initialize the Jarvis UI."""
# #         pygame.init()
# #         pygame.mixer.init()
# #
# #         self.WIDTH = width
# #         self.HEIGHT = height
# #
# #         if fullscreen:
# #             info = pygame.display.Info()
# #             self.WIDTH, self.HEIGHT = info.current_w, info.current_h
# #             self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
# #         else:
# #             self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
# #
# #         pygame.display.set_caption("Jarvis Interface")
# #
# #         # Fonts
# #         self.font_large = pygame.font.Font(pygame.font.get_default_font(), 36)
# #         self.font_small = pygame.font.Font(pygame.font.get_default_font(), 20)
# #
# #         self.clock = pygame.time.Clock()
# #
# #         # Rotating Circle Parameters
# #         self.center = (self.WIDTH // 2, self.HEIGHT // 2)
# #         self.max_radius = min(self.WIDTH, self.HEIGHT) // 3
# #         self.angle = 0
# #         self.speed = 1
# #
# #         # Particle Parameters
# #         self.num_particles = 100
# #         self.particles = self._initialize_particles()
# #
# #         # Pulse effect variables
# #         self.pulse_factor = 1
# #         self.pulse_speed = 0.05
# #         self.min_size = 3
# #         self.max_size = 3
# #
# #         # Color Transition
# #         self.current_color_1 = list(Color.BLUE.value)
# #         self.current_color_2 = list(Color.CYAN.value)
# #         self.target_color_1 = list(Color.BLUE.value)
# #         self.target_color_2 = list(Color.CYAN.value)
# #         self.color_transition_speed = 10
# #
# #         # State flags
# #         self.model_answering = False
# #         self.is_collided = False
# #         self.is_generating = False
# #
# #         # Jarvis voice and responses
# #         self.jarvis_responses = [
# #             "Тук съм, как мога да помогна?",
# #             "Слушам, как мога да Ви асистирам?",
# #             "Тук съм, как мога да помогна?",
# #             "С какво мога да Ви бъда полезен?"
# #             # "Слушам шефе, как да помогна?"
# #         ]
# #
# #         # Status list
# #         self.status_list = []
# #
# #         # Song information
# #         self.current_song = ""
# #         self.current_artist = ""
# #         self.current_progress = 0
# #         self.song_duration = 0
# #
# #         # Selected model (no dropdown)
# #         self.selected_model = "Gemini"
# #
# #     def _initialize_particles(self):
# #         """Initialize random particles."""
# #         return [
# #             {
# #                 "x": random.randint(0, self.WIDTH),
# #                 "y": random.randint(0, self.HEIGHT),
# #                 "dx": random.uniform(-2, 2),
# #                 "dy": random.uniform(-2, 2)
# #             }
# #             for _ in range(self.num_particles)
# #         ]
# #
# #     def blend_color(self, current, target, speed):
# #         """Gradually transitions the current color toward the target color."""
# #         for i in range(3):
# #             diff = target[i] - current[i]
# #             if abs(diff) > speed:
# #                 current[i] += speed if diff > 0 else -speed
# #             else:
# #                 current[i] = target[i]
# #
# #     def draw_particles(self, target_mode=False):
# #         """Draws particles on the surface."""
# #         for i, particle in enumerate(self.particles):
# #             if target_mode:
# #                 # Calculate target circular positions
# #                 target_x = self.center[0] + math.cos(
# #                     math.radians(self.angle + i * 360 / len(self.particles))) * self.max_radius
# #                 target_y = self.center[1] + math.sin(
# #                     math.radians(self.angle + i * 360 / len(self.particles))) * self.max_radius
# #
# #                 # Smoothly move particles towards their circular positions
# #                 particle["x"] += (target_x - particle["x"]) * 0.05
# #                 particle["y"] += (target_y - particle["y"]) * 0.05
# #
# #                 # Pulse effect
# #                 if self.pulse_factor < self.max_size:
# #                     self.pulse_factor = min(self.max_size, self.pulse_factor + self.pulse_speed)
# #                 else:
# #                     self.pulse_factor = max(self.min_size, self.pulse_factor - self.pulse_speed)
# #             else:
# #                 # Move particles randomly when in default mode
# #                 particle["x"] += particle["dx"]
# #                 particle["y"] += particle["dy"]
# #
# #                 # Keep particles within the screen bounds
# #                 if particle["x"] <= 0 or particle["x"] >= self.WIDTH:
# #                     particle["dx"] *= -1
# #                 if particle["y"] <= 0 or particle["y"] >= self.HEIGHT:
# #                     particle["dy"] *= -1
# #
# #             # Draw the particle
# #             pygame.draw.circle(
# #                 self.screen,
# #                 tuple(self.current_color_2),
# #                 (int(particle["x"]), int(particle["y"])),
# #                 int(self.pulse_factor)
# #             )
# #
# #     def set_response_state(self, model=None):
# #         """Update settings when the model is answering."""
# #         if model == "Gemini":
# #             self.target_color_1 = list(Color.GREEN1.value)
# #             self.target_color_2 = list(Color.GREEN2.value)
# #         elif model == "Llama3":
# #             self.target_color_1 = list(Color.PINK1.value)
# #             self.target_color_2 = list(Color.PINK2.value)
# #         elif model == "Deepseek":
# #             self.target_color_1 = list(Color.PURPLE1.value)
# #             self.target_color_2 = list(Color.PURPLE2.value)
# #
# #         self.speed = 1
# #         self.is_collided = True
# #         self.angle += self.speed
# #
# #     def set_thinking_state(self):
# #         """Update settings when the model is listening."""
# #         self.target_color_1 = list(Color.ORANGE1.value)
# #         self.target_color_2 = list(Color.ORANGE1.value)
# #         self.speed = 0.5
# #         self.is_collided = True
# #         self.angle += self.speed
# #
# #     def set_default_state(self):
# #         """Update settings when the model is not answering."""
# #         self.target_color_1 = list(Color.BLUE.value)
# #         self.target_color_2 = list(Color.CYAN.value)
# #         self.speed = 1
# #         self.is_collided = False
# #
# #     def draw_text(self, text, position, font, color):
# #         """Draws text onto the surface."""
# #         text_surface = font.render(text, True, color)
# #         self.screen.blit(text_surface, position)
# #
# #     def draw_progress_bar(self, x, y, width, height, progress, max_progress):
# #         """Draw a progress bar to represent the song timeline."""
# #         if max_progress > 0:
# #             progress_ratio = progress / max_progress
# #             progress_width = int(width * progress_ratio)
# #         else:
# #             progress_width = 0
# #
# #         # Draw the empty progress bar (background)
# #         pygame.draw.rect(self.screen, (50, 50, 50), (x, y, width, height))
# #
# #         # Draw the filled progress bar (foreground)
# #         pygame.draw.rect(self.screen, Color.GREEN1.value, (x, y, progress_width, height))
# #
# #     def update_status(self, new_status):
# #         """Add new status to the list (max 5 items)."""
# #         self.status_list.append(new_status)
# #         if len(self.status_list) > 5:
# #             self.status_list.pop(0)
# #
# #     def update_song_info(self, song, artist, progress_ms, duration_ms):
# #         """Update the current song information."""
# #         self.current_song = song if song else ""
# #         self.current_artist = artist if artist else ""
# #         self.current_progress = progress_ms
# #         self.song_duration = duration_ms
# #
# #     def fetch_current_track(self, sp):
# #         try:
# #             current_track = sp.currently_playing()
# #             if current_track and current_track['is_playing']:
# #                 song = current_track['item']['name']
# #                 artist = ", ".join([a['name'] for a in current_track['item']['artists']])
# #                 album_cover_url = current_track['item']['album']['images'][0]['url']
# #                 progress_ms = current_track['progress_ms']
# #                 duration_ms = current_track['item']['duration_ms']
# #                 return song, artist, album_cover_url, progress_ms, duration_ms
# #             return None, None, None, 0, 0
# #         except Exception as e:
# #             print(f"Error fetching track: {e}")
# #             return None, None, None, 0, 0
# #
# #
# #     def render(self):
# #         """Main render method - call this every frame."""
# #         # Fill background
# #         self.screen.fill(Color.BLACK.value)
# #
# #         # Toggle behavior based on state
# #         if self.is_generating:
# #             self.set_thinking_state()
# #         elif self.model_answering:
# #             self.set_response_state(self.selected_model)
# #         else:
# #             self.set_default_state()
# #
# #         # Smooth Color Transition
# #         self.blend_color(self.current_color_1, self.target_color_1, self.color_transition_speed)
# #         self.blend_color(self.current_color_2, self.target_color_2, self.color_transition_speed)
# #
# #         # Draw Particles
# #         self.draw_particles(target_mode=self.is_collided)
# #
# #         # Draw Text
# #         self.draw_text("Vision Interface MK4", (10, 10), self.font_large, Color.WHITE.value)
# #         self.draw_text("System Status: All Systems Online", (10, 60), self.font_small, tuple(self.current_color_2))
# #
# #         # Draw the list of statuses
# #         start_y = 90
# #         line_height = 30
# #         for index, status in enumerate(self.status_list):
# #             self.draw_text(status, (10, start_y + index * line_height), self.font_small, Color.WHITE.value)
# #
# #         # Draw the progress bar for the song timeline
# #         progress_bar_x = (self.WIDTH - 700) // 2
# #         progress_bar_y = self.HEIGHT - 30
# #         self.draw_progress_bar(progress_bar_x, progress_bar_y, 700, 10, self.current_progress, self.song_duration)
# #
# #         # Draw song information above the progress bar
# #         if self.current_song:
# #             song_surface = self.font_small.render(self.current_song, True, Color.WHITE.value)
# #             song_text_x = (self.WIDTH - song_surface.get_width()) // 2
# #             song_text_y = progress_bar_y - 30
# #             self.screen.blit(song_surface, (song_text_x, song_text_y))
# #
# #         # Update Display
# #         pygame.display.flip()
# #         self.clock.tick(60)
# #
# #     def quit(self):
# #         """Clean up pygame."""
# #         pygame.quit()
#
#
# # New design
#
# import pygame
# import math
# import random
# from enum import Enum
# import difflib
#
# class Color(Enum):
#     BLACK = (0, 0, 0)
#     WHITE = (255, 255, 255)
#     BLUE = (0, 128, 255)
#     CYAN = (0, 255, 255)
#     ORANGE1 = (255, 165, 0)
#     ORANGE2 = (255, 115, 0)
#     GREEN1 = (0, 219, 0)
#     GREEN2 = (4, 201, 4)
#     PINK1 = (255, 182, 193)
#     PINK2 = (255, 105, 180)
#     PURPLE1 = (166, 0, 255)
#     PURPLE2 = (176, 28, 255)
#     DARK_BG = (5, 5, 8)
#     TEXT_DIM = (100, 105, 120, 180)
#     TEXT_BRIGHT = (220, 225, 235)
#
# class JarvisUI:
#     def __init__(self, width=1920, height=1080, fullscreen=False):
#         pygame.init()
#         pygame.mixer.init()
#
#         self.WIDTH = width
#         self.HEIGHT = height
#
#         if fullscreen:
#             info = pygame.display.Info()
#             self.WIDTH, self.HEIGHT = info.current_w, info.current_h
#             self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
#         else:
#             self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
#
#         pygame.display.set_caption("Jarvis Interface")
#
#         # Minimal, modern fonts
#         self.font_title = pygame.font.Font(pygame.font.get_default_font(), 28)
#         self.font_large = pygame.font.Font(pygame.font.get_default_font(), 24)
#         self.font_medium = pygame.font.Font(pygame.font.get_default_font(), 18)
#         self.font_small = pygame.font.Font(pygame.font.get_default_font(), 14)
#         self.font_micro = pygame.font.Font(pygame.font.get_default_font(), 11)
#
#         self.clock = pygame.time.Clock()
#
#         # Rotating Circle Parameters
#         self.center = (self.WIDTH // 2, self.HEIGHT // 2)
#         self.max_radius = min(self.WIDTH, self.HEIGHT) // 4
#         self.angle = 0
#         self.speed = 1
#
#         # Particle Parameters - fewer, more elegant
#         self.num_particles = 80
#         self.particles = self._initialize_particles()
#
#         # Pulse effect variables
#         self.pulse_factor = 1
#         self.pulse_speed = 0.03
#         self.min_size = 2
#         self.max_size = 2.5
#
#         # Color Transition
#         self.current_color_1 = list(Color.BLUE.value)
#         self.current_color_2 = list(Color.CYAN.value)
#         self.target_color_1 = list(Color.BLUE.value)
#         self.target_color_2 = list(Color.CYAN.value)
#         self.color_transition_speed = 8
#
#         # State flags
#         self.model_answering = False
#         self.is_collided = False
#         self.is_generating = False
#
#         # Jarvis voice and responses
#         self.jarvis_responses = [
#             "Тук съм, как мога да помогна?",
#             "Слушам, как мога да Ви асистирам?",
#             "Тук съм, как мога да помогна?",
#             "С какво мога да Ви бъда полезен?"
#         ]
#
#         # Status list
#         self.status_list = []
#
#         # Song information
#         self.current_song = ""
#         self.current_artist = ""
#         self.current_progress = 0
#         self.song_duration = 0
#
#         # Selected model
#         self.selected_model = "Gemini"
#
#         # Animation for subtle effects
#         self.breath_cycle = 0
#         self.scanline_offset = 0
#
#     def _initialize_particles(self):
#         return [
#             {
#                 "x": random.randint(0, self.WIDTH),
#                 "y": random.randint(0, self.HEIGHT),
#                 "dx": random.uniform(-0.8, 0.8),
#                 "dy": random.uniform(-0.8, 0.8),
#                 "size": random.uniform(1, 2),
#                 "opacity": random.uniform(0.3, 0.8)
#             }
#             for _ in range(self.num_particles)
#         ]
#
#     def blend_color(self, current, target, speed):
#         for i in range(3):
#             diff = target[i] - current[i]
#             if abs(diff) > speed:
#                 current[i] += speed if diff > 0 else -speed
#             else:
#                 current[i] = target[i]
#
#     def draw_subtle_glow(self, center, radius, color, intensity=2):
#         for i in range(intensity):
#             alpha = int(25 / (i + 1))
#             glow_radius = radius + (i * 15)
#             glow_color = (*color, alpha)
#
#             surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
#             pygame.draw.circle(surf, glow_color, (glow_radius, glow_radius), glow_radius)
#             self.screen.blit(surf, (center[0] - glow_radius, center[1] - glow_radius))
#
#     def draw_particles(self, target_mode=False):
#         for i, particle in enumerate(self.particles):
#             if target_mode:
#                 # Calculate target circular positions
#                 target_x = self.center[0] + math.cos(
#                     math.radians(self.angle + i * 360 / len(self.particles))) * self.max_radius
#                 target_y = self.center[1] + math.sin(
#                     math.radians(self.angle + i * 360 / len(self.particles))) * self.max_radius
#
#                 # Smoothly move particles towards their circular positions
#                 particle["x"] += (target_x - particle["x"]) * 0.04
#                 particle["y"] += (target_y - particle["y"]) * 0.04
#
#                 # Pulse effect
#                 if self.pulse_factor < self.max_size:
#                     self.pulse_factor = min(self.max_size, self.pulse_factor + self.pulse_speed)
#                 else:
#                     self.pulse_factor = max(self.min_size, self.pulse_factor - self.pulse_speed)
#
#                 # Draw subtle glow in circle mode
#                 particle_size = int(self.pulse_factor * particle["size"])
#                 opacity = int(particle["opacity"] * 255)
#
#                 # Glow
#                 glow_surf = pygame.Surface((particle_size * 6, particle_size * 6), pygame.SRCALPHA)
#                 glow_color = (*self.current_color_2, opacity // 3)
#                 pygame.draw.circle(glow_surf, glow_color, (particle_size * 3, particle_size * 3), particle_size * 3)
#                 self.screen.blit(glow_surf,
#                                  (int(particle["x"]) - particle_size * 3, int(particle["y"]) - particle_size * 3))
#             else:
#                 # Move particles randomly when in default mode
#                 particle["x"] += particle["dx"]
#                 particle["y"] += particle["dy"]
#
#                 # Keep particles within the screen bounds
#                 if particle["x"] <= 0 or particle["x"] >= self.WIDTH:
#                     particle["dx"] *= -1
#                 if particle["y"] <= 0 or particle["y"] >= self.HEIGHT:
#                     particle["dy"] *= -1
#
#             # Draw the particle core
#             opacity = int(particle["opacity"] * 255)
#             color_with_alpha = (*self.current_color_2, opacity)
#             particle_size = int(self.pulse_factor * particle.get("size", 1))
#
#             surf = pygame.Surface((particle_size * 2, particle_size * 2), pygame.SRCALPHA)
#             pygame.draw.circle(surf, color_with_alpha, (particle_size, particle_size), particle_size)
#             self.screen.blit(surf, (int(particle["x"]) - particle_size, int(particle["y"]) - particle_size))
#
#     def draw_hairline(self, start_pos, end_pos, color, alpha=80):
#         surf = pygame.Surface((abs(end_pos[0] - start_pos[0]) or 1, abs(end_pos[1] - start_pos[1]) or 1),
#                               pygame.SRCALPHA)
#         relative_start = (0, 0) if start_pos[1] == end_pos[1] else (0, 0)
#         relative_end = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
#         pygame.draw.line(surf, (*color, alpha), relative_start, relative_end, 1)
#         self.screen.blit(surf, start_pos)
#
#     def set_response_state(self, model=None):
#         if model == "Gemini":
#             self.target_color_1 = list(Color.GREEN1.value)
#             self.target_color_2 = list(Color.GREEN2.value)
#         elif model == "Llama3":
#             self.target_color_1 = list(Color.PINK1.value)
#             self.target_color_2 = list(Color.PINK2.value)
#         elif model == "Deepseek":
#             self.target_color_1 = list(Color.PURPLE1.value)
#             self.target_color_2 = list(Color.PURPLE2.value)
#
#         self.speed = 1
#         self.is_collided = True
#         self.angle += self.speed
#
#     def set_thinking_state(self):
#         self.target_color_1 = list(Color.ORANGE1.value)
#         self.target_color_2 = list(Color.ORANGE1.value)
#         self.speed = 0.5
#         self.is_collided = True
#         self.angle += self.speed
#
#     def set_default_state(self):
#         self.target_color_1 = list(Color.BLUE.value)
#         self.target_color_2 = list(Color.CYAN.value)
#         self.speed = 1
#         self.is_collided = False
#
#     def draw_text(self, text, position, font, color, alpha=255):
#         if len(color) == 3:
#             color = (*color, alpha)
#         text_surface = font.render(text, True, color)
#         self.screen.blit(text_surface, position)
#
#     def draw_minimal_progress(self, x, y, width, height, progress, max_progress):
#         if max_progress > 0:
#             progress_ratio = progress / max_progress
#             progress_width = int(width * progress_ratio)
#         else:
#             progress_width = 0
#
#         # Background line - very dim
#         bg_surf = pygame.Surface((width, height), pygame.SRCALPHA)
#         pygame.draw.rect(bg_surf, (255, 255, 255, 20), (0, 0, width, height))
#         self.screen.blit(bg_surf, (x, y))
#
#         # Progress line - accent color
#         if progress_width > 0:
#             progress_surf = pygame.Surface((progress_width, height), pygame.SRCALPHA)
#             glow_color = (*self.current_color_1, 200)
#             pygame.draw.rect(progress_surf, glow_color, (0, 0, progress_width, height))
#             self.screen.blit(progress_surf, (x, y))
#
#     def update_status(self, new_status):
#         self.status_list.append(new_status)
#         if len(self.status_list) > 5:
#             self.status_list.pop(0)
#
#     def update_song_info(self, song, artist, progress_ms, duration_ms):
#         self.current_song = song if song else ""
#         self.current_artist = artist if artist else ""
#         self.current_progress = progress_ms
#         self.song_duration = duration_ms
#
#     def fetch_current_track(self, sp):
#         try:
#             current_track = sp.currently_playing()
#             if current_track and current_track['is_playing']:
#                 song = current_track['item']['name']
#                 artist = ", ".join([a['name'] for a in current_track['item']['artists']])
#                 album_cover_url = current_track['item']['album']['images'][0]['url']
#                 progress_ms = current_track['progress_ms']
#                 duration_ms = current_track['item']['duration_ms']
#                 return song, artist, album_cover_url, progress_ms, duration_ms
#             return None, None, None, 0, 0
#         except Exception as e:
#             print(f"Error fetching track: {e}")
#             return None, None, None, 0, 0
#
#     def format_time(self, ms):
#         seconds = ms // 1000
#         minutes = seconds // 60
#         seconds = seconds % 60
#         return f"{minutes}:{seconds:02d}"
#
#     def draw_corner_accent(self, x, y, size, color, corner='tl'):
#         alpha = 120
#         if corner == 'tl':
#             # Top-left
#             pygame.draw.line(self.screen, (*color, alpha), (x, y), (x + size, y), 1)
#             pygame.draw.line(self.screen, (*color, alpha), (x, y), (x, y + size), 1)
#         elif corner == 'tr':
#             # Top-right
#             pygame.draw.line(self.screen, (*color, alpha), (x, y), (x - size, y), 1)
#             pygame.draw.line(self.screen, (*color, alpha), (x, y), (x, y + size), 1)
#
#     def render(self):
#         # Fill with deep black
#         self.screen.fill(Color.DARK_BG.value)
#
#         # Toggle behavior based on state
#         if self.is_generating:
#             self.set_thinking_state()
#         elif self.model_answering:
#             self.set_response_state(self.selected_model)
#         else:
#             self.set_default_state()
#
#         # Smooth Color Transition
#         self.blend_color(self.current_color_1, self.target_color_1, self.color_transition_speed)
#         self.blend_color(self.current_color_2, self.target_color_2, self.color_transition_speed)
#
#         # Update breathing animation
#         self.breath_cycle += 0.02
#         breath_alpha = int(30 + 20 * math.sin(self.breath_cycle))
#
#         # Draw very subtle central glow when active
#         if self.is_collided:
#             for i in range(2):
#                 glow_radius = self.max_radius + 80 + (i * 40)
#                 glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
#                 glow_color = (*self.current_color_1, breath_alpha // (i + 2))
#                 pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), glow_radius)
#                 self.screen.blit(glow_surf, (self.center[0] - glow_radius, self.center[1] - glow_radius))
#
#         # Draw Particles
#         self.draw_particles(target_mode=self.is_collided)
#
#         # Top bar - ultra minimal
#         top_margin = 40
#         left_margin = 50
#
#         # Title - smaller, cleaner
#         self.draw_text("VISION", (left_margin, top_margin), self.font_title, Color.TEXT_BRIGHT.value)
#         title_width = self.font_title.size("VISION")[0]
#         self.draw_text("MK4", (left_margin + title_width + 15, top_margin + 4), self.font_small, self.current_color_1,
#                        alpha=200)
#
#         # Subtle status indicator dot
#         dot_x = left_margin + title_width + 15 + self.font_small.size("MK4")[0] + 20
#         dot_y = top_margin + 8
#         dot_alpha = int(150 + 50 * math.sin(self.breath_cycle))
#         pygame.draw.circle(self.screen, (*self.current_color_2, dot_alpha), (dot_x, dot_y), 3)
#
#         # Status text - minimal
#         if len(self.status_list) > 0:
#             status_y = top_margin + 50
#             for i, status in enumerate(self.status_list[-3:]):  # Show only last 3
#                 opacity = int(100 - (i * 20))
#                 self.draw_text(status, (left_margin, status_y + i * 28), self.font_small, Color.TEXT_DIM.value[:3],
#                                alpha=opacity)
#
#         # Song info - bottom, ultra clean
#         if self.current_song:
#             bottom_margin = 60
#             song_y = self.HEIGHT - bottom_margin
#
#             # Progress bar - just a thin line
#             progress_width = 600
#             progress_x = (self.WIDTH - progress_width) // 2
#             progress_y = song_y
#
#             self.draw_minimal_progress(progress_x, progress_y, progress_width, 2,
#                                        self.current_progress, self.song_duration)
#
#             # Song info above progress
#             song_text_y = progress_y - 40
#
#             # Center-aligned song title
#             song_surface = self.font_medium.render(self.current_song, True, Color.TEXT_BRIGHT.value)
#             song_text_x = (self.WIDTH - song_surface.get_width()) // 2
#             self.screen.blit(song_surface, (song_text_x, song_text_y))
#
#             # Time labels - minimal
#             current_time = self.format_time(self.current_progress)
#             total_time = self.format_time(self.song_duration)
#
#             self.draw_text(current_time, (progress_x, progress_y + 10),
#                            self.font_micro, Color.TEXT_DIM.value[:3], alpha=150)
#
#             total_time_surface = self.font_micro.render(total_time, True, Color.TEXT_DIM.value[:3])
#             self.draw_text(total_time, (progress_x + progress_width - total_time_surface.get_width(),
#                                         progress_y + 10), self.font_micro, Color.TEXT_DIM.value[:3], alpha=150)
#
#         # Corner accents - minimal tech aesthetic
#         accent_size = 20
#         self.draw_corner_accent(left_margin - 10, top_margin - 10, accent_size, self.current_color_1, 'tl')
#         self.draw_corner_accent(self.WIDTH - left_margin + 10, top_margin - 10, accent_size, self.current_color_1, 'tr')
#
#         # Update Display
#         pygame.display.flip()
#         self.clock.tick(60)
#
#     def quit(self):
#         pygame.quit()


import webview
import threading
import time

class VisionAPI:
    def __init__(self):
        self.window = None
        self.state = "idle"

    def set_state(self, new_state):
        self.state = new_state
        print(f"Switching to {new_state} mode")
        if self.window:
            self.window.evaluate_js(f"switchState('{new_state}')")