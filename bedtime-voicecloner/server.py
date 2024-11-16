from flask import Flask, request, jsonify
import base64
import os
import torch
from TTS.api import TTS

app = Flask(__name__)

# Set environment variable to confirm Coqui TOS agreement
os.environ["COQUI_TOS_AGREED"] = "1"

# Initialize TTS model and log device info
try:
    print("Initializing TTS model...")
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=torch.cuda.is_available())
    device = "GPU" if torch.cuda.is_available() else "CPU"
    print(f"TTS model initialized. Processing will occur on: {device}")
except Exception as e:
    print(f"Failed to initialize TTS model: {e}")
    raise

@app.route('/tts', methods=['POST'])
def text_to_speech():
    print("Received a request for text-to-speech conversion.")
    data = request.json
    input_audio = data.get('input_audio')
    text = data.get('text')

    if not input_audio or not text:
        print("Missing input_audio or text in the request.")
        return jsonify({'error': 'Missing input_audio or text'}), 400

    try:
        # Decode the input audio from Base64
        input_audio_path = "/tmp/input_audio.wav"
        print("Decoding input_audio from Base64.")
        with open(input_audio_path, "wb") as f:
            f.write(base64.b64decode(input_audio))
        print(f"Input audio saved at: {input_audio_path}")

        # Generate speech using the input voice as `speaker_wav`
        output_path = "/tmp/output_audio.wav"
        print("Generating speech from text using the TTS model.")
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=input_audio_path,
            language="en"
        )
        print(f"Output audio generated and saved at: {output_path}")

        # Encode the output audio to Base64 for the response
        print("Encoding output audio to Base64.")
        with open(output_path, "rb") as f:
            output_audio = base64.b64encode(f.read()).decode('utf-8')

        print("Request processed successfully.")
        return jsonify({'output_audio': output_audio})
    except Exception as e:
        print(f"Error during text-to-speech processing: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000)
