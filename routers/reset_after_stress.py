from fastapi import APIRouter
from services.gemini_service import (
    generate_pdf_content,
    generate_video_suggestions,
    generate_audio_suggestions
)
from models import ResetAfterStressResponse, ResetOption, TechniqueContent
import asyncio

router = APIRouter(prefix="/reset-after-stress", tags=["Reset After Stress"])

OPTIONS_DATA = [
    {
        "name": "After a Single Incident",
        "techniques": ["Understanding What Just Happened", "Grounding Exercise", "Quick Reset Card"]
    },
    {
        "name": "After a Long Day",
        "techniques": ["Extended Body Scan", "Understanding What Just Happened", "Grounding Exercise"]
    },
    {
        "name": "After Multiple Tough Calls",
        "techniques": ["Understanding What Just Happened", "Grounding Exercise"]
    }
]

@router.post("/full-content", response_model=ResetAfterStressResponse)
async def get_full_reset_after_stress_content():
    """
    Reset After Stress mode এ কল করলেই 
    3 টা অপশনের অধীনে থাকা সব technique এর audio, video এবং pdf (JSON) dynamically generate হয়ে আসবে
    """
    options_content = []

    for option in OPTIONS_DATA:
        option_name = option["name"]
        techniques = option["techniques"]
        
        # Parallel processing for techniques in this option
        tasks = []
        for tech_name in techniques:
            tasks.append(process_single_technique(tech_name))
            
        results = await asyncio.gather(*tasks)
        
        options_content.append(
            ResetOption(
                option_name=option_name,
                techniques=list(results)
            )
        )

    return ResetAfterStressResponse(
        mode="Reset After Stress",
        options=options_content
    )

async def process_single_technique(technique_name: str) -> TechniqueContent:
    """একটা technique এর জন্য audio, video, pdf generate করে"""
    
    # Gemini দিয়ে 3টা জিনিস simultaneously generate করা হচ্ছে
    audio_task = generate_audio_suggestions(technique_name)
    video_task = generate_video_suggestions(technique_name)
    pdf_task = generate_pdf_content(technique_name, "Reset After Stress")

    audio_list, video_list, pdf_content = await asyncio.gather(
        audio_task, video_task, pdf_task
    )

    return TechniqueContent(
        technique_name=technique_name,
        audio=audio_list,
        video=video_list,
        pdf=pdf_content
    )

@router.get("/options")
async def get_options():
    return {"options": OPTIONS_DATA}
