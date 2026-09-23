"""Database configurations"""

from sqlmodel import create_engine, SQLModel

sqlite_file_name = "database.db"
sqlite_url = "sqlite:///blog.db"


sqlite_file_name = "blog.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

SQLModel.metadata.create_all(engine)  # Create tables if they don't exist

# SQLModel.metadata.create_all(bind=engine)  # Create tables

# SQLModel.metadata.drop_all(engine)  # Drop tables
