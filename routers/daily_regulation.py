from fastapi import APIRouter
from services.gemini_service import (
    generate_pdf_content,
    generate_video_suggestions,
    generate_audio_suggestions
)
from models import DailyRegulationResponse, WeekContent
import asyncio

router = APIRouter(prefix="/daily-regulation", tags=["Build Daily Regulation"])

WEEKS = [
    {"week_number": 1, "week_name": "Understanding Stress"},
    {"week_number": 2, "week_name": "Regulation Basics"},
    {"week_number": 3, "week_name": "Building Consistency"},
    {"week_number": 4, "week_name": "Applying Under Stress"},
]

@router.post("/full-content", response_model=DailyRegulationResponse)
async def get_full_daily_regulation_content():
    """
    Build Daily Regulation mode এ কল করলেই
    4 সপ্তাহের প্রতিটি week এর audio, video এবং pdf (JSON) dynamically generate হয়ে আসবে
    """
    # Parallel processing for all 4 weeks
    tasks = [process_single_week(w["week_number"], w["week_name"]) for w in WEEKS]
    weeks_content = await asyncio.gather(*tasks)

    return DailyRegulationResponse(
        mode="Build Daily Regulation",
        weeks=list(weeks_content)
    )

async def process_single_week(week_number: int, week_name: str) -> WeekContent:
    """একটা week এর জন্য audio, video, pdf generate করে"""

    topic = f"Week {week_number}: {week_name}"

    # Gemini + YouTube দিয়ে 3টা জিনিস simultaneously generate
    audio_task = generate_audio_suggestions(topic)
    video_task = generate_video_suggestions(topic)
    pdf_task = generate_pdf_content(topic, "Build Daily Regulation")

    audio_list, video_list, pdf_content = await asyncio.gather(
        audio_task, video_task, pdf_task
    )

    return WeekContent(
        week_number=week_number,
        week_name=week_name,
        audio=audio_list,
        video=video_list,
        pdf=pdf_content
    )

@router.get("/weeks")
async def get_weeks():
    return {"weeks": WEEKS}
