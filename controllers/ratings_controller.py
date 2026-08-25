from flask import (
    Blueprint,
    request,
    session,
    jsonify
)

from models.recipe import Recipe
from models.rating_service import RatingService


ratings_bp = Blueprint("ratings", __name__)


@ratings_bp.route(
    "/recipes/<int:recipe_id>/rating",
    methods=["POST"]
)
def rate(recipe_id):
    if "user_id" not in session:
        return jsonify({
            "status": "error"
        }), 401

    recipe = Recipe.query.get_or_404(recipe_id)

    data = request.get_json()

    value = data.get("value")

    if value not in [1, 2, 3, 4, 5]:
        return jsonify({
            "status": "error"
        }), 400

    RatingService.set_rating(
        session["user_id"],
        recipe.id,
        value
    )

    rating_info = RatingService.get_rating_info(
        recipe.id
    )

    return jsonify({
        "status": "ok",
        "user_rating": value,
        "average": rating_info["average"],
        "count": rating_info["count"]
    })