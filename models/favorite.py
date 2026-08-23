from extensions import db


class Favorite(db.Model):
    __tablename__ = "favorites"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id"),
        primary_key=True
    )

    user = db.relationship("User")
    recipe = db.relationship("Recipe")