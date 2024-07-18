from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Database url
DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Initialize Database
def init_db():
    Base.metadata.create_all(bind=engine)

#Create a database session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()