from extensions import db


recipe_ingredient = db.Table(
    "recipe_ingredient",

    db.Column(
        "recipe_id",
        db.Integer,
        db.ForeignKey("recipes.id"),
        primary_key=True
    ),

    db.Column(
        "ingredient_id",
        db.Integer,
        db.ForeignKey("ingredients.id"),
        primary_key=True
    )
)


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    instructions = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    ingredients = db.relationship(
        "Ingredient",
        secondary=recipe_ingredient,
        backref="recipes"
    )