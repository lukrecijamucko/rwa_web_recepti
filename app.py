from flask import Flask

from config import Config
from extensions import db, migrate
from models.user import User
from controllers.users_controller import users_bp
from controllers.categories_controller import categories_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)

    @app.route("/")
    def home():
        return "Aplikacija radi!"

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)