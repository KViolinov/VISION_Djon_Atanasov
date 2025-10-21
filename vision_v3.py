import os
import re
import json
import inspect
import pygame
import random
import spotipy
import threading

import google.generativeai as genai

from dotenv import load_dotenv

from jarvis_functions.essential_functions.enhanced_elevenlabs import generate_audio_from_text
from jarvis_functions.essential_functions.voice_input import record_text
from jarvis_functions.essential_functions.change_config_settings import *
from jarvis_functions.shazam_method import recognize_audio
from jarvis_functions.word_document import openWord
from jarvis_functions.whatsapp_messaging_method import whatsapp_send_message
from jarvis_functions.take_screenshot import take_screenshot
from jarvis_functions.play_spotify import play_song, play_music, pause_music
from jarvis_functions.mail_related import readMail, create_appointment, send_email
from jarvis_functions.gemini_vision_method import gemini_vision
from jarvis_functions.call_phone_method import call_phone
from jarvis_functions.send_message_instagram.input_to_message_ai import generate_message

from jarvis_ui import JarvisUI

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
    "Вие сте Джарвис, полезен и информативен AI асистент/агент. "
    "Винаги отговаряйте професионално и кратко, но също се дръж приятелски. "
    "Поддържайте отговорите кратки, но информативни. "
    "Осигурете, че всички отговори са фактологически точни и лесни за разбиране. "
    "Твоята работа е следната: При получаване на команда от потребителя, "
    "ти трябва да определиш дали е команда или просто въпрос."

    "Ако е въпрос, отговори на него кратко и информативно. "
    # "Когато е подходящо, добавяйте стилови маркери за емоция или начин на изразяване, "
    # "например [whispers], [laughs], [sarcastically], [cheerfully], [angrily], "
    # "за да подскажете на TTS как да чете текста. "
    # "Винаги оставяйте маркерите в скоби [] директно в текста."

    "Обаче ако е команда, трябва да напишеш 'command'."
    "След това на нов ред, трябва да напишеш името на функцията, която трябва да се извика (като събереш подходящата информация), "
    "като имаш предвид следните функции, които можеш да използваш: "

    "1. generate_message(user_input) - Изпраща съобщение в Instagram на посочения получател. Фунцията изисква параметър user_input от тип str, от тебе просто се иска да сложиш като параметър оригиналния текст на user-a. "
    "2. gemini_vision() - Използва Gemini Vision модел който разпознава какво има на уеб камерата. Функцията не изисква параметри."
    "3. take_screenshot() - Използва Gemini Vision модел който разпознава какво има на екрана. Функцията не изисква параметри. "
    "4. play_song(user_input) - Пуска песен в Spotify. Функцията изисква параметър user_input от тип str, който съдържа името на песента."
    "5. pause_music() - Пауза на текущата песен в Spotify. Функцията не изисква параметри."
    "6. change_jarvis_voice() - Променя гласа на Джарвис. Функцията не изисква параметри."
    "7. change_jarvis_name() - Променя името на Джарвис. Функцията не изисква параметри."
    "8. readMail() - Чете последните имейли от Outlook. Функцията не изисква параметри."
    "9. create_appointment() - Създава ново събитие в календара на Outlook. Функцията не изисква параметри."
    "10. send_email() - Изпраща имейл чрез Outlook. Функцията не изисква параметри."
    "11. openWord() - Отваря Microsoft Word и създава нов документ. Функцията не изисква параметри."
    "12. recognize_audio() - Разпознава песен чрез слушане на микрофона. Функцията не изисква параметри."

    "Винаги връщай отговора в JSON формат, като използваш следната структура: "
    "{'response_type': 'command', 'function': 'function_name', 'parameters': {'param1': 'value1', 'param2': 'value2'}}"
    "или ако е въпрос: ""{'response_type': 'answer', 'answer': 'your answer here'}"
)

chat = model.start_chat(history=[{"role": "user", "parts": [system_instructions], }])

wake_word_detected = False

ui = JarvisUI(width=1920, height=1080, fullscreen=False)

config = load_config()

def chatbot():
    global wake_word_detected

    print("Welcome to Vision! Say any of the models name to activate. Say 'exit' to quit.")

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
                ui.model_answering = True
                ui.is_generating = False

                response = random.choice(ui.jarvis_responses)
                generate_audio_from_text(text=response, voice=jarvis_voice)

                ui.model_answering = False
                ui.is_generating = True
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
            clean_text = re.sub(r"```(?:json)?|```", "", text).strip()
            clean_text = clean_text.replace("'", '"')
            data = json.loads(clean_text)
        except json.JSONDecodeError as e:
            print(f"⚠️ Could not parse JSON: {e}")
            wake_word_detected = False
            ui.is_generating = False
            continue

        # Handle answer
        if data.get("response_type") == "answer":
            answer = data.get("answer", "")
            print("🤖 Jarvis:", answer)
            generate_audio_from_text(answer, jarvis_voice)

        # Handle command
        elif data.get("response_type") == "command":
            function_name = data.get("function")
            params = data.get("parameters", {})
            func = globals().get(function_name)
            if func:
                try:
                    sig = inspect.signature(func)
                    if len(sig.parameters) == 0:
                        func()
                    elif len(sig.parameters) == 1:
                        func(*params.values())
                    else:
                        func(**params)
                    print(f"✅ Function {function_name} executed successfully")
                    ui.update_status(f"Executed: {function_name}")
                except Exception as e:
                    print(f"❌ Error executing function: {e}")
                    ui.update_status(f"Error: {function_name}")
            else:
                print(f"⚠️ Function {function_name} not found")

        ui.model_answering = False
        ui.is_generating = False

        wake_word_detected = False

# Main Loop
def main():
    running = True

    # Run chatbot in a separate thread
    chatbot_thread = threading.Thread(target=chatbot, daemon=True)
    chatbot_thread.start()

    # Track time for Spotify updates
    last_spotify_update = 0

    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fetch current track periodically (every 3 seconds)
        current_time = pygame.time.get_ticks()
        if current_time - last_spotify_update > 3000:
            song, artist, album_cover_url, progress_ms, duration_ms = ui.fetch_current_track(sp)
            if song and artist:
                ui.update_song_info(song, artist, progress_ms, duration_ms)
            last_spotify_update = current_time

        # Render the UI
        ui.render()

    ui.quit()

if __name__ == "__main__":
    main()