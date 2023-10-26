from pydantic import BaseModel
from typing import Optional

class UniversalyModel(BaseModel):
    name: str | None = None
    login: str
    password: str
