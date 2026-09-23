"""Main file"""

from contextlib import asynccontextmanager
from typing import Annotated, Generator

from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session

from blog.schemas import Blog
from blog.database import engine


def create_db_and_tables() -> None:
    """Create all tables defined by SQLModel table classes."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    create_db_and_tables()
    yield
    # Runs on shutdown (optional)


app = FastAPI(lifespan=lifespan)


@app.post("/blog")
def create_blog(data: Blog, session: SessionDep):
    """Blog creation function"""
    session.add(data)
    session.commit()
    session.refresh(data)
    return data
