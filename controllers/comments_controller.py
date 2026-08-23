from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    session
)

from extensions import db
from models.comment import Comment
from models.recipe import Recipe
from models.user import User


comments_bp = Blueprint("comments", __name__)


@comments_bp.route(
    "/recipes/<int:recipe_id>/comments",
    methods=["POST"]
)
def create(recipe_id):
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    recipe = Recipe.query.get_or_404(recipe_id)

    content = request.form.get("content", "").strip()

    if not content:
        return redirect(
            url_for(
                "recipes.show",
                recipe_id=recipe.id
            )
        )

    comment = Comment(
        content=content,
        user_id=session["user_id"],
        recipe_id=recipe.id
    )

    db.session.add(comment)
    db.session.commit()

    return redirect(
        url_for(
            "recipes.show",
            recipe_id=recipe.id
        )
    )

@comments_bp.route(
    "/comments/<int:comment_id>/delete",
    methods=["POST"]
)
def delete(comment_id):
    if "user_id" not in session:
        return redirect(url_for("users.login"))

    comment = Comment.query.get_or_404(comment_id)

    user_id = session["user_id"]

    user = User.query.get(user_id)

    if user is None:
        return redirect(url_for("users.login"))

    if comment.user_id != user_id and not user.is_admin:
        return "Nemate dopuštenje za brisanje ovog komentara.", 403

    recipe_id = comment.recipe_id

    db.session.delete(comment)
    db.session.commit()

    return redirect(
        url_for(
            "recipes.show",
            recipe_id=recipe_id
        )
    )