from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session
)

from models.recipe import Recipe
from models.favorite_service import FavoriteService


favorites_bp = Blueprint("favorites", __name__)


@favorites_bp.route("/favorites")
def index():
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    recipes = FavoriteService.get_favorites_for_user(
        session["user_id"]
    )

    return render_template(
        "favorites.html",
        recipes=recipes,
        title="Favoriti"
    )


@favorites_bp.route(
    "/recipes/<int:recipe_id>/favorite",
    methods=["POST"]
)
def add(recipe_id):
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    recipe = Recipe.query.get_or_404(recipe_id)

    FavoriteService.add_favorite(
        session["user_id"],
        recipe.id
    )

    return redirect(
        url_for(
            "recipes.show",
            recipe_id=recipe.id
        )
    )


@favorites_bp.route(
    "/recipes/<int:recipe_id>/favorite/remove",
    methods=["POST"]
)
def remove(recipe_id):
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    recipe = Recipe.query.get_or_404(recipe_id)

    FavoriteService.remove_favorite(
        session["user_id"],
        recipe.id
    )

    return redirect(
        url_for(
            "recipes.show",
            recipe_id=recipe.id
        )
    )