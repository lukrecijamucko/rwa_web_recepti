from flask import Blueprint

from models.category_service import CategoryService


db_bp = Blueprint("db", __name__)


@db_bp.route("/db/seed_categories")
def seed_categories():
    CategoryService.seed_default_categories()

    return "Početne kategorije su dodane."