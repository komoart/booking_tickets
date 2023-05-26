from datetime import datetime

from pydantic import BaseModel


class ReviewInfo(BaseModel):
    id: str  # noqa: VNE003
    movie_id: str
    text: str
    author_id: str
    pub_date: datetime
    likes: int
    dislikes: int
    author_score: float

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['pub_date'] = _dict['pub_date'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict
