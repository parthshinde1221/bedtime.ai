import base64
import requests
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TTS_API_URL = os.getenv("TTS_API_URL")
AUDIO_FILE_PATH = os.getenv("AUDIO_FILE_PATH")
def generate_story(sketch_classify_result: dict) -> str:
    try:
        # Access prediction directly from the dictionary
        prediction = sketch_classify_result.get("prediction", "unknown")
        confidence = sketch_classify_result.get("confidence", "unknown")

        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Call the ChatGPT API to expand on this story
        response = client.chat.completions.create(            
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative storyteller."},
                {"role": "user", "content": f"Tell a bedtime story about: '{prediction}'. Keep it very short under 100 words for kids."}
            ]
        )

        # Extract the generated story from the API response
        generated_story = response.choices[0].message.content  
        print(f"Generated Story: {generated_story}")

        # Read audio file as Base64
        base64_voice = read_audio_file_as_base64(AUDIO_FILE_PATH)
        # Use the narration function to generate narrated audio
        narrated_audio_base64 = narrate_story(generated_story, base64_voice)
        print("Narration completed successfully.")
        return narrated_audio_base64

    except Exception as e:
        print(f"Error while generating story or narration: {e}")
        return ""


def narrate_story(story: str, base64_voice: str) -> str:
    payload = {
        "input_audio": base64_voice,
        "text": story,
    }
    response = requests.post(TTS_API_URL, json=payload)
    if response.status_code == 200:
        return response.json()["output_audio"]
    else:
        raise Exception(f"Failed to generate audio. Status code: {response.status_code}, Response: {response.text}")

def read_audio_file_as_base64(file_path: str) -> str:
    with open(file_path, "rb") as audio_file:
        encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")
    return encoded_audio
