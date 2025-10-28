import os
import re
import json
import inspect
import pygame
import random
import spotipy
import threading
import webview

import google.generativeai as genai

from dotenv import load_dotenv

from jarvis_functions.essential_functions.enhanced_elevenlabs import generate_audio_from_text
from jarvis_functions.essential_functions.voice_input import record_text
from jarvis_functions.essential_functions.change_config_settings import get_jarvis_voice, get_jarvis_name, change_jarvis_name, change_jarvis_voice
from jarvis_functions.shazam_method import recognize_audio
from jarvis_functions.word_document import openWord
from jarvis_functions.whatsapp_messaging_method import whatsapp_send_message
from jarvis_functions.take_screenshot import take_screenshot
from jarvis_functions.play_spotify import play_song, play_music, pause_music
#from jarvis_functions.mail_related import readMail, create_appointment, send_email
from jarvis_functions.gemini_vision_method import gemini_vision
from jarvis_functions.call_phone_method import call_phone
from jarvis_functions.send_message_instagram.input_to_message_ai import generate_message
from jarvis_functions.record_video import record_video

from jarvis_ui import VisionAPI

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri='http://localhost:8888/callback',
    scope='user-library-read user-read-playback-state user-modify-playback-state'))

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_KEY")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel(model_name="gemini-2.5-flash")

system_instructions = (
    "Ти си Джарвис – интелигентен, приятелски и полезен AI асистент. "
    "Отговаряй професионално и кратко, на български език. "
    "Винаги връщай отговора САМО във валиден JSON формат, без обяснения, без Markdown, без ```json```. "
    "Допустими са два типа отговори:\n\n"
    "1️⃣ Ако потребителят задава въпрос:\n"
    "{"
    "\"response_type\": \"answer\", "
    "\"answer\": \"тук е отговорът ти\""
    "}\n\n"
    "2️⃣ Ако потребителят иска действие (команда):\n"
    "{"
    "\"response_type\": \"command\", "
    "\"function\": \"името_на_функцията\", "
    "\"parameters\": {\"параметър1\": \"стойност1\", \"параметър2\": \"стойност2\"}"
    "}\n\n"
    "Функции, които можеш да извикваш:\n"
    "- generate_message(user_input)\n"
    "- gemini_vision()\n"
    "- take_screenshot()\n"
    "- record_video()\n"
    "- play_song(user_input)\n"
    "- pause_music()\n"
    "- change_jarvis_voice()\n"
    "- change_jarvis_name()\n"
    "- openWord()\n"
    "- recognize_audio()\n\n"
    "Никога не добавяй нищо извън JSON формата. "
    "Ако не си сигурен, върни {\"response_type\": \"answer\", \"answer\": \"Не съм сигурен, но мога да проверя.\"}"
)


chat = model.start_chat(history=[{"role": "user", "parts": [system_instructions], }])

wake_word_detected = False

api = None
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

jarvis_responses = [
    "Тук съм, как мога да помогна?",
    "Слушам, как мога да Ви асистирам?",
    "Тук съм, как мога да помогна?",
    "С какво мога да Ви бъда полезен?"
]

def update_spotify_status(api):
    import time
    while True:
        try:
            playback = sp.current_playback()
            if playback and playback["is_playing"]:
                track = playback["item"]
                song = track["name"]
                artist = ", ".join([a["name"] for a in track["artists"]])
                api.window.evaluate_js(f"updateSpotify('{song}', '{artist}', true)")
            else:
                api.window.evaluate_js("updateSpotify('', '', false)")
        except Exception as e:
            print("⚠️ Spotify update error:", e)

        time.sleep(10)  # update every 10 seconds

def chatbot():
    global wake_word_detected

    print("Welcome to Vision! Say any of the models name to activate. Say 'exit' to quit.")
    generate_audio_from_text("На линия съм, извикайте ме когато имате нужда.", get_jarvis_voice())

    while True:
        if not wake_word_detected:
            print("Waiting for wake word...")
            user_input = record_text()

            if not user_input:
                print("Sorry, I didn't catch that. Please try again.")
                continue

            user_input_lower = user_input.lower()

            jarvis_name = get_jarvis_name().lower()
            jarvis_voice = get_jarvis_voice()

            if jarvis_name == user_input_lower:
                wake_word_detected = True
                pygame.mixer.music.load("sound_files/beep.flac")
                pygame.mixer.music.play()

                print("✅ Wake word detected!")
                api.set_state("answering")

                response = random.choice(jarvis_responses)
                generate_audio_from_text(text=response, voice=jarvis_voice)

                api.set_state("thinking")
            else:
                continue

        print("Listening for commands...")
        user_input = record_text()

        if not user_input:
            print("Error: No input detected.")
            wake_word_detected = False
            continue

        response = chat.send_message(user_input)
        text = response.text.strip()

        # Clean and parse JSON
        try:
            # Try to clean and parse JSON
            clean_text = re.sub(r"```(?:json)?|```", "", text).strip()
            clean_text = clean_text.replace("'", '"')
            data = json.loads(clean_text)
        except json.JSONDecodeError as e:
            print(f"⚠️ Could not parse JSON: {e}")
            print("Raw response:", text)  # Show what was actually returned
            generate_audio_from_text(text, jarvis_voice)  # still speak the message

            api.set_state("idle")
            continue

        # Handle answer
        if data.get("response_type") == "answer":
            answer = data.get("answer", "")
            print("🤖 Jarvis:", answer)
            api.set_state("answering")
            generate_audio_from_text(answer, jarvis_voice)

        # Handle command
        elif data.get("response_type") == "command":
            function_name = data.get("function")
            params = data.get("parameters", {})
            func = globals().get(function_name)

            if func:
                try:
                    sig = inspect.signature(func)

                    # --- Special handling for camera ---
                    if function_name == "gemini_vision":
                        api.set_state("camera")  # Orb shows 📸 animation
                        func(api.set_state)  # Pass the UI callback to gemini_vision()
                        api.set_state("idle")  # Go back to idle after completion

                    elif function_name == "record_video":
                        api.set_state("recording")
                        func(api.set_state)
                        api.set_state("idle")

                    # --- All other functions ---
                    else:
                        if len(sig.parameters) == 0:
                            func()
                        elif len(sig.parameters) == 1:
                            func(*params.values())
                        else:
                            func(**params)

                    print(f"✅ Function {function_name} executed successfully")

                except Exception as e:
                    print(f"❌ Error executing function: {e}")
            else:
                print(f"⚠️ Function {function_name} not found")

        api.set_state("idle")
        wake_word_detected = False

# Main Loop
def main():
    global api

    api = VisionAPI()
    window = webview.create_window("Vision Interface MK4", "ui/index.html", js_api=api, width=1200, height=800)
    api.window = window

    threading.Thread(target=chatbot, daemon=True).start()
    threading.Thread(target=update_spotify_status, args=(api,), daemon=True).start()

    webview.start()

if __name__ == "__main__":
    main()