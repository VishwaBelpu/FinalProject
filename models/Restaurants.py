from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dependencies.database import Base

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    address = Column(String(255), nullable=False)
    menu_items = relationship("MenuItem", back_populates="restaurant")
    