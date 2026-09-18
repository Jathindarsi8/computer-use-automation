from google import genai
import PIL.Image
import base64
import io
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def test_gemini_vision():
    # Read and encode image
    with open("evidence/step_001_homepage.png", "rb") as f:
        image_bytes = f.read()
    
    image_base64 = base64.b64encode(image_bytes).decode()
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": image_base64
                        }
                    },
                    {
                        "text": "What do you see on this webpage? List 3 actions an AI agent could take here."
                    }
                ]
            }
        ]
    )
    
    print("✅ Gemini Vision works!")
    print(response.text)

if __name__ == "__main__":
    test_gemini_vision()