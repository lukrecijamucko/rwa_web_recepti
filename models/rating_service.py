from extensions import db
from models.rating import Rating


class RatingService:

    @staticmethod
    def get_user_rating(user_id, recipe_id):
        rating = Rating.query.filter_by(
            user_id=user_id,
            recipe_id=recipe_id
        ).first()

        if rating is None:
            return None

        return rating.value

    @staticmethod
    def set_rating(user_id, recipe_id, value):
        rating = Rating.query.filter_by(
            user_id=user_id,
            recipe_id=recipe_id
        ).first()

        if rating is None:
            rating = Rating(
                user_id=user_id,
                recipe_id=recipe_id,
                value=value
            )

            db.session.add(rating)

        else:
            rating.value = value

        db.session.commit()

    @staticmethod
    def get_rating_info(recipe_id):
        ratings = Rating.query.filter_by(
            recipe_id=recipe_id
        ).all()

        if not ratings:
            return {
                "average": 0,
                "count": 0
            }

        total = 0

        for rating in ratings:
            total += rating.value

        average = total / len(ratings)

        return {
            "average": round(average, 1),
            "count": len(ratings)
        }