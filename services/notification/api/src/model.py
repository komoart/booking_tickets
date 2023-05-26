from typing import Dict, Any

from pydantic import BaseModel


class Event(BaseModel):
    is_promo: bool
    template_id: int
    user_ids: list[str] | None
    context: Dict[str, Any]

    class Config:
        use_enum_values = True
