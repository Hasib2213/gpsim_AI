from fastapi import APIRouter
from services.gemini_service import (
    generate_pdf_content,
    generate_video_suggestions,
    generate_audio_suggestions
)
from models import FieldModeResponse, TechniqueContent
import asyncio

router = APIRouter(prefix="/field-mode", tags=["Field Mode"])

TECHNIQUES = [
    "1 Minute Reset (use this between calls)",
    "Box Breathing (use this in the vehicle)",
    "Body Scan Meditation",
    "Grounding Exercise (use this after a tough run)",
    "5-4-3-2-1 Technique (use this before going home)",
    "Pattern Interrupt (use this to break the stress cycle)",
    "Quick Body Scan (use this during downtime)"
]

@router.post("/full-content", response_model=FieldModeResponse)
async def get_full_field_mode_content():
    """
    Field Mode এ কল করলেই 
    সব technique এর audio, video এবং pdf (JSON) dynamically generate হয়ে আসবে
    """
    all_techniques_content = []

    # Parallel processing (fast performance)
    tasks = []
    for tech_name in TECHNIQUES:
        tasks.append(process_single_technique(tech_name))

    results = await asyncio.gather(*tasks)

    for result in results:
        all_techniques_content.append(result)

    return FieldModeResponse(
        mode="Field Mode",
        techniques=all_techniques_content
    )

async def process_single_technique(technique_name: str) -> TechniqueContent:
    """একটা technique এর জন্য audio, video, pdf generate করে"""
    
    # Gemini দিয়ে 3টা জিনিস simultaneously generate করা হচ্ছে
    audio_task = generate_audio_suggestions(technique_name)
    video_task = generate_video_suggestions(technique_name)
    pdf_task = generate_pdf_content(technique_name, "Field Mode")

    audio_list, video_list, pdf_content = await asyncio.gather(
        audio_task, video_task, pdf_task
    )

    return TechniqueContent(
        technique_name=technique_name,
        audio=audio_list,
        video=video_list,
        pdf=pdf_content
    )

@router.get("/techniques")
async def get_techniques():
    return {"techniques": TECHNIQUES}
