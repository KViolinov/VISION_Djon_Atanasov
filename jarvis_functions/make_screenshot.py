import google.generativeai as genai
from PIL import ImageGrab
import os
import io

from api_keys.api_keys import GEMINI_KEY

# Configure Gemini API
os.environ["GEMINI_API_KEY"] = GEMINI_KEY
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

def make_screenshot():
    screenshot = ImageGrab.grab()

    # Save to memory buffer as PNG
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    response = model.generate_content(
        [
            "Опиши този скрийншот подробно:",
            {"mime_type": "image/png", "data": image_bytes},
        ]
    )

    return response.text