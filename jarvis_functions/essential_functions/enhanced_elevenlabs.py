from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVEN_LABS_API"),
)

def generate_audio_from_text(text: str, voice: str):
    voice_id = ""

    if(voice == "Brian"):
        voice_id= "nPczCjzI2devNBz1zQrb"
    elif(voice == "Samantha"):
        voice_id= "gu1puNDpHxzdmn6ZDDcv"
    elif(voice == "Roger"):
        voice_id = "CwhRBWXzGAHq8TQ4Fs17"
    elif(voice == "Jessica"):
        voice_id = "cgSgspJ2msm6clMCkdW9"

    audio = elevenlabs.text_to_speech.convert(
        text=(text),
        voice_id=voice_id,
        # model_id="eleven_v3",
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
    )

    play(audio)

