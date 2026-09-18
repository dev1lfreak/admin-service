from pydantic import BaseModel
from pydantic import Field


class ErrorResponse(BaseModel):
    detail: str = Field(title='Detail')
