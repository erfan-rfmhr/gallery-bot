from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    link = Column(String(1000), nullable=False)
    isSent = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id} {self.link} {self.isSent}>'
