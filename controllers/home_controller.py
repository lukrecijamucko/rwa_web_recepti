from flask import (
    Blueprint,
    render_template
)

from models.home_service import HomeService


home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    suggestions = HomeService.get_random_recipes()

    return render_template(
        "home.html",
        suggestions=suggestions,
        title="Početna"
    )