"""My main file"""

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Models


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None
    updated: bool | None = None


# Paths or Routes (Endpoints)


@app.get("/")
def index(limit: int = 10, published: bool = True, sort: str | None = None):
    """Entry route fetches all blogs"""

    if not published:
        return {"data": f"Returning all blogs with limit {limit}"}

    return {"data": f"Returning published blogs and limiting to {limit}"}


# Should always be above the dynamic route of the same kind.
@app.get("/blog/unpublished")
def unpublished(sort: Optional[str] = None):
    """Fetch all unpublished blogs"""

    return {"data": "Unpublished blog list"}


@app.get("/blog/{blog_id}")
def show(blog_id: int):
    """Show individual blog"""

    return {"data": f"blog {blog_id} fetched"}


@app.get("/blog/{blog_id}/comments")
def comments(blog_id: int):
    """Returns comments for a single blog"""

    return {
        "message": f"Comments for blog {blog_id}",
        "data": [{"1": "Comment 1", "2": "Comment 2", "3": "Comment 3"}],
    }


# Request body


@app.post("/blog")
def create_blog(data: Blog):
    """Create a new blog"""

    return data
