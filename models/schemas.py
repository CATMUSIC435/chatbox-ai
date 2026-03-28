from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    question: str
    domain: Optional[str] = "default"

class LearnRequest(BaseModel):
    text: str
    domain: Optional[str] = "default"
