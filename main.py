"""My main file"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    """Entry route fetches all blogs"""

    return {"data": "blog list"}


@app.get("/blog/{blog_id}")
def show(blog_id: int):
    """Show individual blog"""
    return {"data": f"blog {blog_id} fetched"}
