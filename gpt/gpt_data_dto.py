
from pydantic import BaseModel


class GptData(BaseModel):
    content: str
