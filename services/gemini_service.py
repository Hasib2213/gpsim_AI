import json
import os
from google import genai
from google.genai import types

# Initialize client. It will automatically use the GEMINI_API_KEY from environment variables.
client = genai.Client()

async def generate_pdf_content(technique_name: str, mode: str) -> dict:
    prompt = f"Generate an educational PDF content outline as JSON for the technique '{technique_name}' in '{mode}'. Schema: {{'title': 'str', 'description': 'str', 'steps': ['str'], 'benefits': 'str'}}."
    
    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"[Gemini API Error] PDF Content generation failed for {technique_name}: {e}")
        # Fallback dictionary if Gemini call fails
        return {
            "title": technique_name, 
            "description": f"Here is a default guide for {technique_name} while offline.", 
            "steps": ["Find a comfortable position.", "Take a slow, deep breath in.", "Exhale gently.", "Repeat for 1 minute."], 
            "benefits": "Provides immediate relaxation and nervous system regulation."
        }

async def generate_video_suggestions(technique_name: str) -> list:
    prompt = f"Suggest 2 instructional videos for '{technique_name}'. Output strictly as a JSON list of objects with keys: 'title', 'duration', 'url_placeholder'."
    
    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        data = json.loads(response.text)
        return data if isinstance(data, list) else data.get("videos", [data])
    except Exception as e:
        print(f"[Gemini API Error] Video suggestions failed for {technique_name}: {e}")
        return [{"title": f"Demo Video for {technique_name}", "duration": "5 mins", "url_placeholder": "https://youtube.com/something"}]

async def generate_audio_suggestions(technique_name: str) -> list:
    prompt = f"Suggest 2 guided audio sessions for '{technique_name}'. Output strictly as a JSON list of objects with keys: 'title', 'duration', 'theme'."
    
    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        data = json.loads(response.text)
        return data if isinstance(data, list) else data.get("audios", [data])
    except Exception as e:
        print(f"[Gemini API Error] Audio suggestions failed for {technique_name}: {e}")
        return [{"title": f"Demo Audio for {technique_name}", "duration": "3 mins", "theme": "Calm"}]
