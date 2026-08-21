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

    if request.method == "POST":
        recipe = Recipe(
            title=request.form["title"].strip(),
            description=request.form["description"].strip(),
            instructions=request.form["instructions"].strip(),
            user_id=session["user_id"]
        )

        db.session.add(recipe)
        db.session.commit()

        return redirect(
            url_for(
                "recipes.show",
                recipe_id=recipe.id
            )
        )

    return render_template(
        "recipe_create.html",
        title="Novi recept"
    )


@recipes_bp.route("/recipes/<int:recipe_id>")
def show(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    return render_template(
        "recipe_show.html",
        recipe=recipe,
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

    if request.method == "POST":
        recipe.title = request.form["title"].strip()
        recipe.description = request.form["description"].strip()
        recipe.instructions = request.form["instructions"].strip()

        db.session.commit()

        return redirect(
            url_for(
                "recipes.show",
                recipe_id=recipe.id
            )
        )

    return render_template(
        "recipe_edit.html",
        recipe=recipe,
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