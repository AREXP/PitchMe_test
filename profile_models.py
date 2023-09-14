from pydantic import BaseModel
from typing import List


class PythonDeveloperCriteriaModel(BaseModel):
    BACKEND_TITLES_REQUIRED: int = 3
    MIN_TOTAL_EXPERIENCE: int = 8
    POSITIONS_REQUIRED: List[str] = ["Backend developer", "Software engineer"]
    SKILLS_REQUIRED: List[str] = ["Python", "C++"]
    FAANG_COMPANY: str = "FAANG"


class MiddleUXDesignerCriteria(BaseModel):
    POSITIONS_REQUIRED: List[str] = ["Product designer", "UX-designer"]
    DESIGN_TOOLS_REQUIRED: List[str] = ["Figma", "Sketch", "UX-research", "Miro"]  # any two elements from the list
    JOB_PATTERN: str = "design"
    DESIGN_TOOLS_COUNT_REQUIRED: int = 2
    EU_COUNTRIES: List[str] = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT",
                               "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"]
    MIN_LAST_JOB_EXPERIENCE: int = 2
    MAX_TOTAL_EXPERIENCE: int = 5
