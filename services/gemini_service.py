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

import urllib.request
import urllib.parse
import asyncio
import re


def _format_youtube_duration(duration_iso: str) -> str:
    """Convert YouTube ISO-8601 duration like PT1H2M9S into a human-friendly string."""
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_iso or "")
    if not match:
        return "N/A"

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)

    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")
    return " ".join(parts)

def search_youtube_videos_sync(technique_name: str) -> list:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        return [{"title": f"Demo Video for {technique_name}", "duration": "5 mins", "url_placeholder": "https://youtube.com/something"}]
    
    query = urllib.parse.quote(f"{technique_name} technique relaxation")
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=2&key={api_key}"
    
    try:
        req = urllib.request.Request(search_url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            items = data.get("items", [])
            video_ids = [item.get("id", {}).get("videoId", "") for item in items if item.get("id", {}).get("videoId")]

            duration_by_id = {}
            if video_ids:
                ids_param = urllib.parse.quote(",".join(video_ids))
                details_url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={ids_param}&key={api_key}"
                details_req = urllib.request.Request(details_url)
                with urllib.request.urlopen(details_req) as details_response:
                    details_data = json.loads(details_response.read().decode())
                    for video_item in details_data.get("items", []):
                        vid = video_item.get("id")
                        iso_duration = video_item.get("contentDetails", {}).get("duration", "")
                        duration_by_id[vid] = _format_youtube_duration(iso_duration)

            results = []
            for item in items:
                snippet = item.get("snippet", {})
                video_id = item.get("id", {}).get("videoId", "")
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                results.append({
                    "title": snippet.get("title", ""),
                    "duration": duration_by_id.get(video_id, "N/A"),
                    "url_placeholder": video_url
                })
            
            if not results:
                return [{"title": f"Demo Video for {technique_name}", "duration": "5 mins", "url_placeholder": "https://youtube.com/something"}]
            return results
    except Exception as e:
        print(f"[YouTube API Error] failed for {technique_name}: {e}")
        return [{"title": f"Demo Video for {technique_name}", "duration": "5 mins", "url_placeholder": "https://youtube.com/something"}]

async def generate_video_suggestions(technique_name: str) -> list:
    return await asyncio.to_thread(search_youtube_videos_sync, technique_name)


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
