import pyautogui
import time

from jarvis_functions.essential_functions.voice_input import record_text
from jarvis_functions.essential_functions.enhanced_elevenlabs import generate_audio_from_text

def call_phone():
    # Press the 'Win' key to open the Start menu
    pyautogui.press('winleft')
    time.sleep(1)

    # Type 'Phone Link' in the Start menu search bar
    pyautogui.write('Phone Link')
    time.sleep(1)

    # Press 'Enter' to launch the app
    pyautogui.press('enter')
    time.sleep(5)  # Wait for the app to open

    # Open the webcam
    generate_audio_from_text(text="На кого искате да звънна?", voice="Brian")

    print("Listening for contact info...")
    contact_info = record_text()

    if "тати" in contact_info or "баща ми" in contact_info:
        generate_audio_from_text(text="Добре, звъня на баща ви", voice="Brian")

        # Example: Let's assume you are typing the number into the first text field
        pyautogui.write('+359888503801')  # Type the number into the active input field
        pyautogui.press('enter')  # Press Enter to submit if needed

    elif "мама" in contact_info or "майка ми" in contact_info:
        generate_audio_from_text(text="Добре, звъня на мама",
                                voice="Brian")

        # Example: Let's assume you are typing the number into the first text field
        pyautogui.write('+359888433144')  # Type the number into the active input field
        pyautogui.press('enter')  # Press Enter to submit if needed


    time.sleep(2)  # Allow time for the app to process

