from pydantic import BaseModel


class Blog(BaseModel):
    """Contains fields for creating a blog"""

    title: str
    body: str
