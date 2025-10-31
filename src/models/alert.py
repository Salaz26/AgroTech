from pydantic import BaseModel
from datetime import datetime

class Alert(BaseModel):
    id: int
    level: str
    summary: str
    recommendation: str
    timestamp: datetime
