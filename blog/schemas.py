"""Models for blog posts."""

import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


# Best for timezone aware datetime objects, but requires Python 3.9+
def utc_now() -> datetime.datetime:
    """Timezone-aware UTC now."""
    return datetime.datetime.now(datetime.UTC)


class BlogBase(SQLModel):
    """Base model for blog posts."""

    title: str = Field(
        index=True
    )  # index=True for faster searches. Use when you want to filter by this field
    body: str
    published: bool = Field(default=False, index=True)
    created_at: datetime.datetime = Field(default_factory=utc_now)
    updated_at: Optional[datetime.datetime] = None


class Blog(BlogBase, table=True):
    """Blog model for database table."""

    __tablename__ = "blogs"
    id: int | None = Field(default=None, primary_key=True)


class BlogCreate(BlogBase):
    """Create model for blog posts."""

    pass


class BlogPublic(BlogBase):
    """Public model for blog posts."""

    id: int


class BlogUpdate(SQLModel):
    """Update model for blog posts."""

    title: str | None = None
    body: str | None = None
    published: bool | None = None
