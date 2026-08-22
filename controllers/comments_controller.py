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