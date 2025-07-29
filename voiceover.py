import requests
import os

voiceoverDir = "Voiceovers"

voices = [
 {
      "name": "Rachel",
      "description": "A smooth and natural voice ideal for conversational and professional use cases.",
      "voice_id": "21m00Tcm4TlvDq8ikWAM",
      "voice_settings": {
        "pitch": 1.0,
        "speed": 1.2,
        "intonation": "balanced",
        "clarity": "high",
        "volume": "normal"
  }
},
{
    "name": "Chris",
    "description": "A smooth and natural voice ideal for conversational and professional use cases.",
    "voice_id": "iP95p4xoKVk53GoZ742B",
    "voice_settings": {
        "pitch": 1.0,
        "speed": 1.2,
        "intonation": "balanced",
        "clarity": "high",
        "volume": "normal"
    }
}
]

CHUNK_SIZE = 1024
XI_API_KEY=os.environ['XI_API_KEY']

headers = {
    "Accept": "application/json",
    "xi-api-key": XI_API_KEY
}

# Handle response
def create_voice_over(fileName, text, index):
    VOICE_ID = voices[index]["voice_id"]
    voice_settings = voices[index]["voice_settings"]
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True,
            **voice_settings
        }
    }
    
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    output_path = f"{voiceoverDir}/{fileName}.mp3"
    if response.ok:
        
        with open(output_path, "wb") as audio_file:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                audio_file.write(chunk)
        print(f"Audio stream saved successfully to {output_path}.")
    else:
        print(f"Error {response.status_code}: {response.text}")

    return output_path
