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
