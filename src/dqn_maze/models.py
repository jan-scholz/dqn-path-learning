from pydantic import BaseModel


class MazeInput(BaseModel):
    maze: str
