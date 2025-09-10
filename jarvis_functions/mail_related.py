from docx import Document
import win32com.client as win32
import time
import dateparser

from datetime import datetime, timedelta

from elevenlabs import play
from elevenlabs.client import ElevenLabs
import speech_recognition as sr

import os

from api_keys.api_keys import ELEVEN_LABS_API

client = ElevenLabs(api_key=ELEVEN_LABS_API)
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

def send_email_function(subject, body, to_email):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = subject
    mail.Body = body
    mail.To = to_email
    mail.Send()

def parse_natural_time(natural_time):
    """
    Parses a natural language time expression (e.g., '3 часа следобяд днес', 'tomorrow', 'next Wednesday')
    into a datetime object.
    """

    # Manually handle 'днес' and 'утре' since dateparser fails sometimes
    now = datetime.now()

    # Replace Bulgarian words with English for better parsing
    normalized_time = (
        natural_time.replace("днес", "today")
        .replace("утре", "tomorrow")
        .replace("следобяд", "PM")
        .replace("сутринта", "AM")
    )

    # Try parsing with dateparser
    event_time = dateparser.parse(
        normalized_time,
        languages=['bg', 'en'],  # Use both Bulgarian and English
        settings={'PREFER_DATES_FROM': 'future'}
    )

    # If dateparser fails, manually handle simple cases
    if event_time is None:
        if "днес" in natural_time:
            event_time = now.replace(hour=15, minute=0, second=0, microsecond=0)
        elif "утре" in natural_time:
            event_time = (now + timedelta(days=1)).replace(hour=15, minute=0, second=0, microsecond=0)
        else:
            raise ValueError(f"Could not parse the given time expression: {natural_time}")

    return event_time

def create_outlook_appointment(subject, start_time, duration):
    outlook = win32.Dispatch("Outlook.Application")
    appointment = outlook.CreateItem(1)  # 1 = olAppointmentItem

    appointment.Subject = subject
    appointment.Start = start_time
    appointment.Duration = duration
    appointment.ReminderMinutesBeforeStart = 15
    appointment.Save()

    print(f"✅ Appointment '{subject}' scheduled for {start_time}")


def send_email(jarvis_voice: str) -> str:
    audio = client.generate(text="Разбира се, към кого бихте желали да пратите имейла?", voice=jarvis_voice)
    play(audio)

    print("Listening for email info...")
    user_input = record_text()

    if "тати" in user_input or "баща ми" in user_input:
        to_email = "bojidarbojinov@outlook.com"
    elif "мама" in user_input or "майка ми" in user_input:
        to_email = "kameliqbojinova@outlook.com"

    audio = client.generate(text="Каква ще е темата на вашето писмо?", voice=jarvis_voice)
    play(audio)

    print("Listening for email info...")
    subject = record_text()

    audio = client.generate(text="Какво искате да изпратите?", voice=jarvis_voice)
    play(audio)

    print("Listening for email info...")
    body = record_text()

    audio = client.generate(text="Супер, преди да изпратя имейла, ще ви кажа какво съм си записал",
                            voice=jarvis_voice)
    play(audio)

    if to_email == "bojidarbojinov@outlook.com":
        audio = client.generate(text="Имейла е към Божидар Божинов (баща ви)", voice=jarvis_voice)
        play(audio)
    elif to_email == "kameliqbojinova@outlook.com":
        audio = client.generate(text="Имейла е към Камелия Божинова (майка ви)", voice=jarvis_voice)
        play(audio)
    audio = client.generate(text="Темата на писмото е " + subject + "И съдържанието на писмото е " + body,
                            voice=jarvis_voice)
    play(audio)

    audio = client.generate(text="Всичко наред ли е с информацията в писмото?", voice=jarvis_voice)
    play(audio)

    print("Listening for approval...")
    user_input = record_text()

    if "да" in user_input:
        audio = client.generate(text="✅ Супер, пращам имейла", voice=jarvis_voice)
        play(audio)
        send_email(subject, body, to_email)

        return to_email

    elif "не" in user_input:
        audio = client.generate(text="Сорка", voice=jarvis_voice)
        play(audio)

        return "Имаше проблем с информацията в имейла"

def create_appointment(jarvis_voice: str):
    # subject of event
    audio = client.generate(text="Разбира се, как искате да се казва събитието?", voice=jarvis_voice)
    play(audio)

    print("Listening for apointment info...")
    subject = record_text()

    # time of event
    audio = client.generate(text="За кога да бъде това събитие?", voice=jarvis_voice)
    play(audio)

    print("Listening for apointment info...")
    user_input = record_text()

    # duration of event
    audio = client.generate(text="Колко време ще продължи това събитие?", voice=jarvis_voice)
    play(audio)

    print("Listening for apointment info...")
    duration = record_text()


    event_time = parse_natural_time(user_input)
    print(f"Parsed event time: {event_time}")  # Debug output
    audio = client.generate(
        text=f"Супер, запазвам събитие {subject}, в {event_time.strftime('%H:%M %d-%m-%Y')}, и ще трае 1 час",
        voice=jarvis_voice)
    play(audio)

    create_outlook_appointment(subject, event_time, duration=60)

def readMail(jarvis_voice: str):
    # Initialize Outlook
    outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 = Inbox

    # Get all messages sorted by received time (newest first)
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)  # Sort descending (newest first)

    # Retrieve the last 5 emails
    num_emails = 3  # Change this number if you need more
    latest_messages = [messages.GetNext() for _ in range(num_emails)]

    audio = client.generate(text="Ето последните 3 имейла в пощата ви: ", voice=jarvis_voice)
    play(audio)
    # Print email details
    for i, email in enumerate(latest_messages, start=1):
        print(f"\n📧 Email {i}:")
        print(f"Subject: {email.Subject}")
        print(f"From: {email.SenderName}")
        print(f"Received: {email.ReceivedTime}")
        print("\n--- Email Body ---\n")
        print(email.Body)  # Full email body
        print("\n--- End of Email ---\n")
        audio = client.generate(text=f"Имейл номер {i}, изпратено е от {email.SenderName}, "
                                     f"темата е {email.Subject}, а съдържанието на писмото е {email.Body}",
                                voice=jarvis_voice)
        play(audio)
