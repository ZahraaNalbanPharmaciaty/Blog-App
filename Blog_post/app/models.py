from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

# Post database model
class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index = True)
    title = Column(String, index = True)
    description = Column(String, index = True)
    URL = Column(String, index=True)
    tags = Column(String, index = True)
    author = Column(String, index=True)
    deleted = Column(Boolean, index = True, default=False)