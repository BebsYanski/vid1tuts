"""My main file"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    """Entry route fetches all blogs"""
    return {"data": "blog list"}


@app.get("/blog/unpublished")  # Should always be above the dynamic route of same kind.
def unpublished():
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
