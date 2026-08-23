from extensions import db
from models.favorite import Favorite


class FavoriteService:

    @staticmethod
    def get_favorites_for_user(user_id):
        favorites = Favorite.query.filter(
            Favorite.user_id == user_id
        ).all()

        recipes = []

        for favorite in favorites:
            recipes.append(favorite.recipe)

        return recipes

    @staticmethod
    def is_favorite(user_id, recipe_id):
        favorite = Favorite.query.filter_by(
            user_id=user_id,
            recipe_id=recipe_id
        ).first()

        return favorite is not None

    @staticmethod
    def add_favorite(user_id, recipe_id):
        if FavoriteService.is_favorite(user_id, recipe_id):
            return False

        favorite = Favorite(
            user_id=user_id,
            recipe_id=recipe_id
        )

        db.session.add(favorite)
        db.session.commit()

        return True

    @staticmethod
    def remove_favorite(user_id, recipe_id):
        favorite = Favorite.query.filter_by(
            user_id=user_id,
            recipe_id=recipe_id
        ).first()

        if favorite is None:
            return False

        db.session.delete(favorite)
        db.session.commit()

        return True