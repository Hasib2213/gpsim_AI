from fastapi import APIRouter
from services.gemini_service import (
    generate_pdf_content,
    generate_video_suggestions,
    generate_audio_suggestions
)
from models import CalmMyBodyResponse, TechniqueContent
import asyncio

router = APIRouter(prefix="/calm-my-body", tags=["Calm My Body"])

TECHNIQUES = [
    "1 Minute Reset",
    "Box Breathing",
    "Body Scan Meditation",
    "Grounding Exercise",
    "5-4-3-2-1 Technique",
    "Progressive Muscle Relaxation"
]

@router.get("/full-content", response_model=CalmMyBodyResponse)
async def get_full_calm_my_body_content():
    """
    Calm My Body mode এ কল করলেই 
    সব 6টা technique এর audio, video এবং pdf (JSON) dynamically generate হয়ে আসবে
    """
    all_techniques_content = []

    # Parallel processing (fast performance)
    tasks = []
    for tech_name in TECHNIQUES:
        tasks.append(process_single_technique(tech_name))

    results = await asyncio.gather(*tasks)

    for result in results:
        all_techniques_content.append(result)

    return CalmMyBodyResponse(
        mode="Calm My Body",
        techniques=all_techniques_content
    )

async def process_single_technique(technique_name: str) -> TechniqueContent:
    """একটা technique এর জন্য audio, video, pdf generate করে"""
    
    # Gemini দিয়ে 3টা জিনিস simultaneously generate করা হচ্ছে
    audio_task = generate_audio_suggestions(technique_name)
    video_task = generate_video_suggestions(technique_name)
    pdf_task = generate_pdf_content(technique_name, "Calm My Body")

    audio_list, video_list, pdf_content = await asyncio.gather(
        audio_task, video_task, pdf_task
    )

    return TechniqueContent(
        technique_name=technique_name,
        audio=audio_list,
        video=video_list,
        pdf=pdf_content
    )

# Bonus: শুধু technique list চাইলে
@router.get("/techniques")
async def get_techniques():
    return {"techniques": TECHNIQUES}
