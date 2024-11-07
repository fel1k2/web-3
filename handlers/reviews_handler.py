from fastapi import HTTPException
from models.Reviews import reviews
from sqlalchemy import insert, select, update, delete
from datetime import datetime

async def create_review(review, user, db):
     query = insert(reviews).values(
        user_id=user["id"],
        book_id=review.book_id,
        rating=review.rating,
        review_text=review.review_text,
        created_at=datetime.utcnow()
    )

     await db.execute(query)

     return {"message": "review added successfully"}

async def get_reviews_for_book(book_id, db):
     query = select(reviews).where(reviews.c.book_id==book_id)
     result = await db.fetch_all(query)
     return result

async def update_review(review_id, updated_review, user, db):
     query = select(reviews).where(reviews.c.id==review_id)
     existing_review = await db.fetch_one(query)

     if not existing_review:
          raise HTTPException (status_code=404, detail="Review not found")

     if existing_review.user_id != user["id"]:
          raise HTTPException (status_code=403, detail="You are not able to update this review")

     query = update(reviews).where(reviews.c.id==review_id).values(
          review_text=updated_review.review_text,
          rating=updated_review.rating
     )

     await db.execute(query)

     return {"message": "Review updated successfully"}

async def delete_review(review_id, user, db):
     query = select(reviews).where(reviews.c.id==review_id)
     existing_review = await db.fetch_one(query)

     if not existing_review:
          raise HTTPException (status_code=404, detail="Review not found")

     if user["role"] != "admin":
          raise HTTPException (status_code=403, detail="Only admins can delete reviews")

     query = delete(reviews).where(reviews.c.id==review_id)

     await db.execute(query)

     return {"message": "Review deleted successfully"}