from pydantic import BaseModel, Field


class ConvertRequest(BaseModel):
    markdown: str = Field(..., min_length=1)
