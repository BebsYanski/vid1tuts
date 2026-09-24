"""Main file"""

from contextlib import asynccontextmanager
from typing import Annotated, Generator

from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlmodel import SQLModel, Session, select


from blog.schemas import Blog, BlogCreate, BlogPublic, BlogUpdate
from blog.database import engine
from blog.helpers import create_and_refresh


def create_db_and_tables() -> None:
    """Create all tables defined by SQLModel table classes."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Yield a database session for dependency injection."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Initialize the database when the application starts."""
    # Runs on startup
    create_db_and_tables()
    yield
    # Runs on shutdown (optional)


app = FastAPI(lifespan=lifespan)


# Creating a blog
@app.post(
    "/blog",
    response_model=BlogPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_blog(data: BlogCreate, session: SessionDep) -> Blog:
    """Blog creation function"""
    # blog = Blog(**data.model_dump())  # ** is used to unpack the data
    blog = Blog.model_validate(
        data
    )  # model_validate is used to validate the data and create a Blog instance
    return create_and_refresh(session, blog)


# Getting the blogs from the database
@app.get("/blog", response_model=list[BlogPublic])
def fetch_blogs(session: SessionDep):
    """Fetch all blogs from the database."""
    stmt = select(Blog)
    blogs = session.exec(stmt).all()
    return blogs


# from fastapi import Query
# from sqlmodel import select


# @app.get("/blog", response_model=list[BlogPublic])
# def fetch_blogs(
#     session: SessionDep,
#     published: bool | None = None,
#     offset: int = 0,
#     limit: int = Query(default=20, le=100),
# ):
#     """List blog posts, newest first."""
#     stmt = select(Blog)

#     if published is not None:
#         stmt = stmt.where(Blog.published == published)

#     stmt = stmt.order_by(Blog.created_at.desc()).offset(offset).limit(limit)

#     return session.exec(stmt).all()


# Fetching a single blog
@app.get("/blog/{blog_id}", response_model=BlogPublic, status_code=status.HTTP_200_OK)
def fetch_blog(blog_id: int, session: SessionDep, response: Response):
    """Fetch a single blog post by ID."""
    blog = session.get(Blog, blog_id)
    # response.status_code = status.HTTP_201_CREATED
    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )
    return blog


# Deleting a blog
@app.delete("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, session: SessionDep):
    """Delete a blog post."""
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )
    session.delete(blog)
    session.commit()
    return {"ok": True}


# Updating a blog
@app.patch("/blog/{blog_id}", response_model=BlogPublic)
def update_blog(blog_id: int, blog: BlogUpdate, session: SessionDep):
    """Update a blog post."""

    blog_db = session.get(Blog, blog_id)
    if not blog_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )
    blog_data = blog.model_dump(
        exclude_unset=True
    )  # Get the data from the request body and exclude unset fields
    blog_db.sqlmodel_update(blog_data)  # Update the blog
    session.add(blog_db)
    session.commit()
    session.refresh(blog_db)
    return blog_db
