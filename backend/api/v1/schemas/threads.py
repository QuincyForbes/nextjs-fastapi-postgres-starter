from pydantic import BaseModel


class ThreadCreate(BaseModel):
    name: str


class ThreadResponse(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attributes = True
