from extensions import db


class Rating(db.Model):
    __tablename__ = "ratings"

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

    value = db.Column(
        db.Integer,
        nullable=False
    )

    user = db.relationship("User")
    recipe = db.relationship("Recipe")