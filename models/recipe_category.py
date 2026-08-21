from extensions import db


class RecipeCategory(db.Model):
    __tablename__ = "recipe_categories"

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id"),
        primary_key=True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        primary_key=True
    )

    recipe = db.relationship("Recipe")
    category = db.relationship("Category")