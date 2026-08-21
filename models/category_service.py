from extensions import db
from models.category import Category
from models.recipe_category import RecipeCategory


class CategoryService:

    DEFAULT_CATEGORIES = [
        "Deserti",
        "Hladna jela",
        "Finger food"
    ]

    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def get_category(category_id):
        return Category.query.get(category_id)

    @staticmethod
    def create_category(name):
        categories = Category.query.all()

        for category in categories:
            if category.name.lower() == name.lower():
                return False

        category = Category(name=name)

        db.session.add(category)
        db.session.commit()

        return True

    @staticmethod
    def seed_default_categories():
        categories = Category.query.all()

        existing_names = [
            category.name.lower()
            for category in categories
        ]

        for name in CategoryService.DEFAULT_CATEGORIES:
            if name.lower() not in existing_names:
                category = Category(name=name)
                db.session.add(category)

        db.session.commit()

    @staticmethod
    def get_recipes_for_category(category_id):
        recipe_categories = RecipeCategory.query.filter(
            RecipeCategory.category_id == category_id
        ).all()

        recipes = []

        for recipe_category in recipe_categories:
            recipes.append(recipe_category.recipe)

        return recipes