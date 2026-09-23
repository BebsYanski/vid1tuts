"""Main file"""

from fastapi import FastAPI
from blog.schemas import Blog

app = FastAPI()


@app.post("/blog")
def create_blog(data: Blog):
    """Blog creation function"""

    return data
