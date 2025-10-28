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

    match voice:
        case "Brian":
            voice_id= "nPczCjzI2devNBz1zQrb"
        case "Samantha":
            voice_id= "gu1puNDpHxzdmn6ZDDcv"
        case "Roger":
            voice_id = "CwhRBWXzGAHq8TQ4Fs17"
        case "Jessica":
            voice_id = "cgSgspJ2msm6clMCkdW9"

    audio = elevenlabs.text_to_speech.convert(
        text=(text),
        voice_id=voice_id,
        model_id="eleven_flash_v2_5", # more sophisticated model - eleven_v3
        output_format="mp3_44100_128",
    )

    play(audio)

