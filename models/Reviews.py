from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(String(500))

    customer = relationship("User", back_populates="reviews")
    menu_item = relationship("MenuItem", back_populates="reviews")