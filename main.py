"""My main file"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    """Entry route"""

    return {"data": {"message": "Hello, World!"}}


@app.get("/about")
def about():
    """The about page"""
    return {"data": {"message": "About"}}
