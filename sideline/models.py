"""
Request model for the /analyze endpoint.
"""

from typing import Optional

from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    match_id: int
    mode:     str
    template: Optional[str] = "The Game Flow"
