from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TechniqueContent(BaseModel):
    technique_name: str
    audio: List[Dict[str, Any]]
    video: List[Dict[str, Any]]
    pdf: Dict[str, Any]

class CalmMyBodyResponse(BaseModel):
    mode: str
    techniques: List[TechniqueContent]

class ResetOption(BaseModel):
    option_name: str
    techniques: List[TechniqueContent]

class ResetAfterStressResponse(BaseModel):
    mode: str
    options: List[ResetOption]

class FieldModeResponse(BaseModel):
    mode: str
    techniques: List[TechniqueContent]

class WeekContent(BaseModel):
    week_number: int
    week_name: str
    audio: List[Dict[str, Any]]
    video: List[Dict[str, Any]]
    pdf: Dict[str, Any]

class DailyRegulationResponse(BaseModel):
    mode: str
    weeks: List[WeekContent]
