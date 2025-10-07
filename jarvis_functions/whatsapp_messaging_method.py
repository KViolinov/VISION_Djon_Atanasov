import pywhatkit as kit
import pyautogui
import time
from jarvis_functions.essential_functions.enhanced_elevenlabs import generate_audio_from_text
from jarvis_functions.essential_functions.voice_input import record_text

def whatsapp_send_message():
    generate_audio_from_text(text="На кого искате да пратя съобшение?", voice="Brian")

    print("Listening for camera info...")
    contact_info = record_text()

    if "тати" in contact_info or "баща ми" in contact_info:
        generate_audio_from_text(text="Добре, съобщението ще бъде към баща ви. А какво ще искате да бъде съобщението?",
                                voice="Brian")

        print("Listening for message info...")
        message_info = record_text()

        #subprocess.run(["powershell", "Start-Process firefox.exe"])
        # Send the message (it types but does not send)
        kit.sendwhatmsg_instantly("+359888503801", message_info)

        # Wait for WhatsApp Web to load and type the message
        time.sleep(2)  # Adjust this if needed

        # Press "Enter" to send the message
        pyautogui.press("enter")

        generate_audio_from_text(text="Съобщението е изпратено", voice="Brian")

    # elif "мама" in contact_info or "майка ми" in contact_info:
    #     audio = client.generate(text="Добре, съобщението ще бъде към мама. А какво ще искате да бъде съобщението?",
    #                             voice="Brian")
    #     play(audio)
    #
    #     print("Listening for message info...")
    #     message_info = record_text()
    #
    #     #subprocess.run(["powershell", "Start-Process firefox.exe"])
    #
    #     # Send the message (it types but does not send)
    #     kit.sendwhatmsg_instantly("+359888503801", message_info)
    #
    #     # Wait for WhatsApp Web to load and type the message
    #     time.sleep(2)  # Adjust this if needed
    #
    #     # Press "Enter" to send the message
    #     pyautogui.press("enter")
