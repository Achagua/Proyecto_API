from pydantic import BaseModel

class Task(BaseModel):
    """Class Model"""
    start: int
    end: int
    iter_num: int