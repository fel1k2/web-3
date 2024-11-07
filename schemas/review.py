from pydantic import BaseModel

class ReviewCreate(BaseModel):
    #user_id: int
    book_id: int
    rating: int
    review_text: str


class ReviewUpdate(BaseModel):
    rating: int
    review_text: str