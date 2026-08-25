from flask import Flask

from config import Config
from extensions import db, migrate
from models.user import User
from models.recipe import Recipe
from models.comment import Comment
from models.rating import Rating
from controllers.users_controller import users_bp
from controllers.categories_controller import categories_bp
from controllers.db_controller import db_bp
from controllers.recipes_controller import recipes_bp
from controllers.comments_controller import comments_bp
from controllers.favorites_controller import favorites_bp
from controllers.ratings_controller import ratings_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(db_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(ratings_bp)

    @app.route("/")
    def home():
        return "Aplikacija radi!"

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)