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








# import pyautogui
# import time
# import webbrowser
#
# # The URL you want to open
# url_to_open = "https://www.instagram.com/direct/t/106491827536886/"  # Replace with your specific Instagram URL
#
# print(f"Opening {url_to_open} in your default web browser...")
#
# webbrowser.open(url_to_open, new=2)
#
# print("Browser opened. Giving it some time to load.")
# time.sleep(15)  # Give the browser time to open and load the page
#
# pyautogui.typewrite("mlukni be turchin takuv! - izprateno ot Jarvis")
#
# # Press "Enter" to send the message
# pyautogui.press("enter")
#
# # Wait briefly to ensure the message is sent
# time.sleep(2)
#
# # Close the browser tab (Ctrl + W or Cmd + W)
# pyautogui.hotkey("ctrl", "w")  # Use "cmd" instead of "ctrl" if on macOS
#
# print("Browser tab closed.")





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


from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id="dacc19ea9cc44decbdcb2959cd6eb74a",
    client_secret="11e970f059dc4265a8fe64aaa80a82bf",
    redirect_uri="http://localhost:8888/callback",
    scope="user-read-playback-state,user-modify-playback-state"
))

devices = sp.devices()
print(devices)
