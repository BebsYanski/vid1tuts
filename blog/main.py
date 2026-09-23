"""Main file"""

from contextlib import asynccontextmanager
from typing import Annotated, Generator

from fastapi import FastAPI, Depends, status
from sqlmodel import SQLModel, Session

from blog.schemas import Blog, BlogCreate, BlogPublic
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


@app.post(
    "/blog",
    response_model=BlogPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_blog(data: BlogCreate, session: SessionDep) -> Blog:
    """Blog creation function"""
    blog = Blog.model_validate(data)
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog
