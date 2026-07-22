from typing import Optional
from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    customer_id: int
    menu_item_id: int
    rating: int
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None


class Review(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
