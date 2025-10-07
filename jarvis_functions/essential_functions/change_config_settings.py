import os
import json
import voice_input as sr

from jarvis_functions.essential_functions.enhanced_elevenlabs import generate_audio_from_text

r = sr.Recognizer()

def record_text():
    """Listen for speech and return the recognized text."""
    try:
        with sr.Microphone() as source:
            #print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)

            # Recognize speech using Google API
            MyText = r.recognize_google(audio, language="bg-BG")
            print(f"You said: {MyText}")
            return MyText.lower()

    except sr.RequestError as e:
        print(f"API Request Error: {e}")
        return None
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
        return None


def change_jarvis_voice():
    global new_jarvis_voice

    voices = ["Brian", "Jessica", "Roger", "Samantha"]

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

    def load_config():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    config = load_config()

    jarvis_voice = config.get("jarvis_voice")

    generate_audio_from_text(text="Разбира се, с кой глас бихте желали да говоря? "
                             "Имам следните гласове на разположение: Брайън", voice=jarvis_voice),
    generate_audio_from_text(text="Джесика", voice=voices[1]),
    generate_audio_from_text(text="Роджър", voice=voices[2]),
    generate_audio_from_text(text="и Саманта. Кой глас бихте предпочели?", voice=voices[3])


    print("Listening for voice choice...")
    user_input = record_text()

    if "брайън" in user_input or "brian" in user_input:
        new_jarvis_voice = voices[0]
    elif "джесика" in user_input or "jessica" in user_input:
        new_jarvis_voice = voices[1]
    elif "роджър" in user_input or "roger" in user_input:
        new_jarvis_voice = voices[2]
    elif "саманта" in user_input or "samantha" in user_input:
        new_jarvis_voice = voices[3]

    config["jarvis_name"] = new_jarvis_voice

    with open("../../config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


    generate_audio_from_text(text=f"Супер, смених гласа на {jarvis_voice}", voice=jarvis_voice)


def change_jarvis_name():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

    def load_config():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    config = load_config()

    jarvis_voice = config.get("jarvis_name")

    generate_audio_from_text(text="Разбира се, как бихте желали да се казвам?", voice=jarvis_voice)

    print("Listening for name choice...")
    user_input = record_text()

    if user_input is None:
        generate_audio_from_text(text="Нe можах да разбера. Може ли да повторите?", voice=jarvis_voice)
        user_input = record_text()

    generate_audio_from_text(text=f"Супер, от сега нататък можете да ме наричате {user_input}", voice=jarvis_voice)

    config["jarvis_name"] = user_input

    with open("../../config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


def get_jarvis_name() -> str:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

    def load_config():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    config = load_config()

    jarvis_name = config.get("jarvis_name")
    return jarvis_name


def get_jarvis_voice() -> str:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

    def load_config():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    config = load_config()

    jarvis_voice = config.get("jarvis_voice")
    return jarvis_voice


def get_system_instruction() -> str:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

    def load_config():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    config = load_config()

    system_instructions = config.get("system_instructions", "Default fallback text")
    return system_instructions

# import json
# import os
#
# # Use the base folder (project root) for config.json
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
#
# def load_config():
#     with open(CONFIG_PATH, "r", encoding="utf-8") as f:
#         return json.load(f)
#
# config = load_config()
# print("Config loaded:", config)
#
# # Read
#
# jarvis_voice = config.get("jarvis_voice")
# print(jarvis_voice)
#
#
# # Update
# config["jarvis_name"] = "Vision"
#
# with open("config.json", "w", encoding="utf-8") as f:
#     json.dump(config, f, ensure_ascii=False, indent=4)
#
# print("Config updated:", config)