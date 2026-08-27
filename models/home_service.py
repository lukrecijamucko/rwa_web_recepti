import random

from models.recipe_category import RecipeCategory


class HomeService:

    @staticmethod
    def get_random_recipes():
        recipe_categories = RecipeCategory.query.all()

        random.shuffle(recipe_categories)

        selected = []

        used_recipe_ids = set()
        used_category_ids = set()

        for recipe_category in recipe_categories:

            if recipe_category.recipe_id in used_recipe_ids:
                continue

            if recipe_category.category_id in used_category_ids:
                continue

            selected.append(recipe_category)

            used_recipe_ids.add(
                recipe_category.recipe_id
            )

            used_category_ids.add(
                recipe_category.category_id
            )

            if len(selected) == 3:
                break

        return selected