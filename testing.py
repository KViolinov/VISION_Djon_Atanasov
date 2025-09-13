# import spotipy
# import requests
# from PIL import Image
# from io import BytesIO
# import numpy as np
# import time
#
# from api_keys.api_keys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
#
# client_id = SPOTIFY_CLIENT_ID
# client_secret = SPOTIFY_CLIENT_SECRET
#
# sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(
#     client_id=client_id,
#     client_secret=client_secret,
#     redirect_uri='http://localhost:8888/callback',
#     scope="user-read-playback-state user-read-currently-playing"))  # Necessary permissions
#
#
# def get_current_song():
#     """Fetches the currently playing song and album cover URL."""
#     track = sp.current_playback()
#     if track and track.get('item'):
#         song_name = track['item']['name']
#         artist_name = track['item']['artists'][0]['name']
#         album_cover_url = track['item']['album']['images'][0]['url']  # Get the largest image
#         return song_name, artist_name, album_cover_url
#     return None, None, None
#
#
# def get_average_color(image_url):
#     """Downloads the image and calculates the average color."""
#     response = requests.get(image_url)
#     image = Image.open(BytesIO(response.content))
#     image = image.resize((50, 50))  # Reduce resolution for faster processing
#     np_image = np.array(image)
#
#     avg_color = np_image.mean(axis=(0, 1))  # Compute mean RGB values
#     return tuple(map(int, avg_color[:3]))  # Convert to integer RGB format
#
#
# def set_color(red, green, blue):
#     """Set the color using RGB values."""
#     url = "http://192.168.10.211/json/state"
#     data = {
#         "on": True,
#         "bri": 255,  # Optional: brightness
#         "seg": [{
#             "col": [[red, green, blue]]
#         }]
#     }
#     response = requests.post(url, json=data)
#     if response.status_code == 200:
#         print(f"✅ LED Color Set: RGB({red}, {green}, {blue})")
#     else:
#         print("⚠️ Failed to update LED color!")
#
#
# last_song = None
#
# while True:
#     song_name, artist_name, cover_url = get_current_song()
#
#     if song_name and song_name != last_song:  # Check if the song has changed
#         last_song = song_name
#         avg_color = get_average_color(cover_url)
#
#         print(f"🎵 Now Playing: {song_name} - {artist_name}")
#         print(f"🎨 Average Album Cover Color (RGB): {avg_color}")
#
#         # Set the LED color to match the album cover
#         set_color(*avg_color)
#
#     time.sleep(5)  # Wait for 5 seconds before checking again
#



# from jarvis_functions.send_message_instagram.input_to_message_ai import *
#
# text = "Искам да пратиш съобщение на Мерт, че е тъп турчин и ще му избием зъбите"
# #text = "Искам да пратиш съобщение към Вероника, и я питай какво прави"
#
# generate_message(text)




# import pyautogui
# import time
# import webbrowser
# import pyperclip
# import google.generativeai as genai
# from elevenlabs import play
# from elevenlabs.client import ElevenLabs
# 
# from api_keys.api_keys import GEMINI_KEY, ELEVEN_LABS_API
# 
# client = ElevenLabs(api_key=ELEVEN_LABS_API)
# 
# def get_address_from_google_maps() -> str:
#     url_to_open = "https://www.google.com/maps"
# 
#     print(f"Opening {url_to_open}...")
#     webbrowser.open(url_to_open, new=2)
#     time.sleep(8)  # Wait for Google Maps to load
# 
#     print("Typing 'Home' and pressing Enter...")
#     pyautogui.typewrite("Home", interval=0.1)
#     pyautogui.press("enter")
# 
#     print("Waiting for Home location to load...")
#     time.sleep(4)
# 
#     print("Pressing Tab 7 times and Enter...")
#     for _ in range(7):
#         pyautogui.press("tab")
#         time.sleep(0.2)
# 
#     pyautogui.press("enter")
# 
#     print("Waiting for address info to appear...")
#     time.sleep(2)
# 
#     print("Copying address...")
#     pyautogui.hotkey("ctrl", "c")
#     time.sleep(0.5)
# 
#     address = pyperclip.paste()
#     print("Address:", address)
# 
#     pyautogui.hotkey("ctrl", "w")
# 
#     return address or "No address found"
# 
# def generate_message_from_address(address: str) -> str:
#     genai.configure(api_key=GEMINI_KEY)
#     model = genai.GenerativeModel("gemini-1.5-flash")
# 
#     prompt = (
#         "Ше ти дам адрес, и от теб искам да съставиш събщение, нещо като разговор"
#         "все едно ми поръваш такси на този адрес. Адресът е: " + address
#     )
# 
#     response = model.generate_content(prompt)
# 
#     full_text = response.candidates[0].content.parts[0].text.strip()
#     return(full_text)
# 
# def generate_audio_from_message(message: str):
#     audio = client.generate(text=message, voice="Brian")
#     play(audio)
# 
# 
# # Run it
# address = get_address_from_google_maps()
# message = generate_message_from_address(address)
# generate_audio_from_message(message)



# import serial
# import time
#
# PORT = 'COM4'       # Смени с твоя сериен порт
# BAUD_RATE = 115200
#
# try:
#     ser = serial.Serial(PORT, BAUD_RATE, timeout=5)
#     time.sleep(2)  # Изчаква ESP-то да стартира
#     print(f"Connected to the {PORT}")
# except serial.SerialException as e:
#     print("Error in opening the serial port:", e)
#     exit(1)
#
# # Изпращаме командата "get"
# ser.write(b'get 80:7D:3A:DD:B3:A4\n')
# print("🔁 Sent: get")
#
# # Четем отговора на ESP-то
# while True:
#     if ser.in_waiting > 0:
#         line = ser.readline().decode('utf-8', errors='ignore').strip()
#         if line:
#             print("📥 Received:", line)
#             # Спиране, ако сме получили очаквания отговор
#             if "Temperature:" in line or "Humidity:" in line:
#                 break
#
# ser.close()
# print("Connection is ended.")

import pygame
import sys
import importlib
import api_keys

pygame.init()

# === Window setup ===
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jarvis with Settings")

# === Fonts ===
font_small = pygame.font.Font(None, 28)
font_large = pygame.font.Font(None, 40)

# === Colors ===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
ORANGE = (255, 165, 0)

# === Settings UI State ===
settings_open = False
settings_rect = pygame.Rect(WIDTH - 120, HEIGHT - 50, 100, 40)
active_input = None
input_boxes = {}
inputs = {}

# === Load API keys dynamically ===
def load_api_keys():
    importlib.reload(api_keys)
    return {
        "ELEVEN_LABS_API": api_keys.ELEVEN_LABS_API,
        "GEMINI_KEY": api_keys.GEMINI_KEY,
        "SPOTIFY_CLIENT_ID": api_keys.SPOTIFY_CLIENT_ID,
        "SPOTIFY_CLIENT_SECRET": api_keys.SPOTIFY_CLIENT_SECRET
    }

# === Save API keys to file ===
def save_api_keys(updated):
    with open("api_keys/api_keys.py", "w") as f:
        for key, value in updated.items():
            f.write(f'{key} = "{value}"\n')

# === Setup input fields ===
def setup_inputs():
    global input_boxes, inputs
    keys = load_api_keys()
    inputs = keys.copy()
    input_boxes = {}
    start_y = 100
    for i, (k, v) in enumerate(keys.items()):
        rect = pygame.Rect(200, start_y + i * 60, 400, 35)
        input_boxes[k] = rect

setup_inputs()

# === Draw text helper ===
def draw_text(surface, text, pos, font, color):
    txt = font.render(text, True, color)
    surface.blit(txt, pos)

# === Main loop ===
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(GRAY)
    mouse_pos = pygame.mouse.get_pos()

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if settings_rect.collidepoint(mouse_pos):
                settings_open = not settings_open
                if settings_open:
                    setup_inputs()
            if settings_open:
                for key, rect in input_boxes.items():
                    if rect.collidepoint(mouse_pos):
                        active_input = key
                        break
                else:
                    active_input = None

            # Close button
            if settings_open:
                close_rect = pygame.Rect(WIDTH//2 + 200 - 40, HEIGHT//2 - 200 + 10, 30, 30)
                if close_rect.collidepoint(mouse_pos):
                    settings_open = False

            # Save button
            if settings_open:
                save_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 150, 100, 40)
                if save_rect.collidepoint(mouse_pos):
                    save_api_keys(inputs)
                    settings_open = False

        elif event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_BACKSPACE:
                inputs[active_input] = inputs[active_input][:-1]
            elif event.key == pygame.K_RETURN:
                active_input = None
            else:
                inputs[active_input] += event.unicode

    # --- Draw settings button ---
    pygame.draw.rect(screen, WHITE, settings_rect, border_radius=10)
    draw_text(screen, "⚙ Settings", (settings_rect.x + 5, settings_rect.y + 10), font_small, BLACK)

    # --- Draw popup ---
    if settings_open:
        popup_width, popup_height = 500, 400
        popup_x = (WIDTH - popup_width) // 2
        popup_y = (HEIGHT - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

        pygame.draw.rect(screen, (30, 30, 30), popup_rect, border_radius=15)
        pygame.draw.rect(screen, WHITE, popup_rect, 2, border_radius=15)

        draw_text(screen, "Settings", (popup_x + 20, popup_y + 20), font_large, WHITE)

        # Draw inputs
        for i, (key, rect) in enumerate(input_boxes.items()):
            pygame.draw.rect(screen, WHITE if active_input == key else BLACK, rect, 2)
            text_surface = font_small.render(inputs[key], True, WHITE)
            screen.blit(text_surface, (rect.x + 5, rect.y + 5))
            draw_text(screen, key, (rect.x - 180, rect.y + 5), font_small, WHITE)

        # Close button
        close_rect = pygame.Rect(popup_x + popup_width - 40, popup_y + 10, 30, 30)
        pygame.draw.rect(screen, ORANGE, close_rect, border_radius=5)
        draw_text(screen, "X", (close_rect.x + 8, close_rect.y + 5), font_small, BLACK)

        # Save button
        save_rect = pygame.Rect(popup_x + popup_width//2 - 50, popup_y + popup_height - 60, 100, 40)
        pygame.draw.rect(screen, ORANGE, save_rect, border_radius=10)
        draw_text(screen, "Save", (save_rect.x + 20, save_rect.y + 8), font_small, BLACK)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
