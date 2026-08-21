from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from models.category_service import CategoryService
from models.user import User


categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/categories")
def index():
    categories = CategoryService.get_all_categories()

    user_id = session.get("user_id")
    is_admin = False

    if user_id is not None:
        user = User.query.get(user_id)

        if user is not None:
            is_admin = user.is_admin

    return render_template(
        "categories.html",
        categories=categories,
        is_admin=is_admin,
        title="Kategorije"
    )


@categories_bp.route("/categories/create", methods=["GET", "POST"])
def create():
    user_id = session.get("user_id")

    if user_id is None:
        return redirect(url_for("users.login"))

    user = User.query.get(user_id)

    if user is None or not user.is_admin:
        return redirect(url_for("categories.index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if not name:
            return render_template(
                "category_create.html",
                title="Dodaj kategoriju",
                error="Naziv kategorije je obavezan."
            )

        created = CategoryService.create_category(name)

        if not created:
            return render_template(
                "category_create.html",
                title="Dodaj kategoriju",
                error="Kategorija s tim nazivom već postoji."
            )

        return redirect(url_for("categories.index"))

    return render_template(
        "category_create.html",
        title="Dodaj kategoriju"
    )

@categories_bp.route("/categories/<int:category_id>")
def show(category_id):
    category = CategoryService.get_category(category_id)

    if category is None:
        return "Kategorija nije pronađena.", 404

    recipes = CategoryService.get_recipes_for_category(category_id)

    return render_template(
        "category_recipes.html",
        category=category,
        recipes=recipes,
        title=category.name
    )