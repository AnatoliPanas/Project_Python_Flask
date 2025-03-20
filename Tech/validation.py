from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Post(BaseModel):
    title: str
    description: str
    author: str
    is_moderated: bool = Field(default=False)
    created_at: datetime
    updated_at: Optional[datetime] = None

json_input = """{
    "title": "Test Title",
    "description": "Test Description",
    "author": "Anatoli Panas",
    "is_moderated": true,
    "created_at": "2025-03-10", 
    "updated_at": "2025-03-19"
}"""

try:
    post = Post.model_validate_json(json_input)
    print(post)
except Exception as e:
    print(f"Ошибка валидации: {e}")