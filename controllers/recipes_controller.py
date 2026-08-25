from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from extensions import db
from models.recipe import Recipe
from models.category_service import CategoryService
from models.user import User
from models.comment import Comment
from models.favorite_service import FavoriteService
from models.rating_service import RatingService


recipes_bp = Blueprint("recipes", __name__)


@recipes_bp.route("/recipes")
def index():
    recipes = Recipe.query.all()

    return render_template(
        "my_recipes.html",
        recipes=recipes,
        title="Recepti"
    )


@recipes_bp.route("/recipes/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    categories = CategoryService.get_all_categories()

    if request.method == "POST":
        category_ids = request.form.getlist("categories[]")

        if not category_ids:
            return render_template(
                "recipe_create.html",
                categories=categories,
                error="Odaberite barem jednu kategoriju.",
                title="Novi recept"
            )

        recipe = Recipe(
            title=request.form["title"].strip(),
            description=request.form["description"].strip(),
            instructions=request.form["instructions"].strip(),
            user_id=session["user_id"]
        )

        db.session.add(recipe)
        db.session.commit()

        CategoryService.set_categories_for_recipe(
            recipe.id,
            category_ids
        )

        return redirect(
            url_for(
                "recipes.show",
                recipe_id=recipe.id
            )
        )

    return render_template(
        "recipe_create.html",
        categories=categories,
        title="Novi recept"
    )


@recipes_bp.route("/recipes/<int:recipe_id>")
def show(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    categories = CategoryService.get_categories_for_recipe(
        recipe.id
    )

    comments = Comment.query.filter_by(
        recipe_id=recipe.id
    ).all()

    user_id = session.get("user_id")

    is_admin = False
    is_favorite = False
    user_rating = None

    rating_info = RatingService.get_rating_info(
        recipe.id
    )

    if user_id is not None:
        user = User.query.get(user_id)

        if user is not None:
            is_admin = user.is_admin

            is_favorite = FavoriteService.is_favorite(
                user_id,
                recipe.id
            )

            user_rating = RatingService.get_user_rating(
                user_id,
                recipe.id
            )

    return render_template(
        "recipe_show.html",
        recipe=recipe,
        categories=categories,
        comments=comments,
        is_admin=is_admin,
        is_favorite=is_favorite,
        user_rating=user_rating,
        rating_average=rating_info["average"],
        rating_count=rating_info["count"],
        title=recipe.title
    )


@recipes_bp.route(
    "/recipes/<int:recipe_id>/edit",
    methods=["GET", "POST"]
)
def edit(recipe_id):
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user_id != session["user_id"]:
        return "Nemate dopuštenje za uređivanje ovog recepta.", 403

    categories = CategoryService.get_all_categories()

    selected_categories = (
        CategoryService.get_categories_for_recipe(recipe.id)
    )

    selected_category_ids = [
        category.id
        for category in selected_categories
    ]

    if request.method == "POST":
        category_ids = request.form.getlist("categories[]")

        if not category_ids:
            return render_template(
                "recipe_edit.html",
                recipe=recipe,
                categories=categories,
                selected_category_ids=[],
                error="Odaberite barem jednu kategoriju.",
                title="Uredi recept"
            )

        recipe.title = request.form["title"].strip()
        recipe.description = request.form["description"].strip()
        recipe.instructions = request.form["instructions"].strip()

        db.session.commit()

        CategoryService.set_categories_for_recipe(
            recipe.id,
            category_ids
        )

        return redirect(
            url_for(
                "recipes.show",
                recipe_id=recipe.id
            )
        )

    return render_template(
        "recipe_edit.html",
        recipe=recipe,
        categories=categories,
        selected_category_ids=selected_category_ids,
        title="Uredi recept"
    )


@recipes_bp.route(
    "/recipes/<int:recipe_id>/delete",
    methods=["POST"]
)
def delete(recipe_id):
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user_id != session["user_id"]:
        return "Nemate dopuštenje za brisanje ovog recepta.", 403

    db.session.delete(recipe)
    db.session.commit()

    return redirect(
        url_for("recipes.index")
    )


@recipes_bp.route("/my-recipes")
def my_recipes():
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    recipes = Recipe.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "my_recipes.html",
        recipes=recipes,
        title="Moji recepti"
    )