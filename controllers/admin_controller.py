from flask import Blueprint, render_template, redirect, url_for, session

from models.user import User
from models.recipe import Recipe
from models.comment import Comment
from models.category import Category


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
def index():
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    user = User.query.get(session["user_id"])

    if user is None or not user.is_admin:
        return "Nemate dopuštenje za pristup.", 403

    users = User.query.all()
    recipe_count = Recipe.query.count()
    comment_count = Comment.query.count()
    category_count = Category.query.count()

    return render_template(
        "admin.html",
        users=users,
        recipe_count=recipe_count,
        comment_count=comment_count,
        category_count=category_count,
        title="Admin"
    )