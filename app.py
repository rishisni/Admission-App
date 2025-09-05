from flask import Flask
from config import Config
from extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from routes.student_routes import student_bp
    from routes.admin_routes import admin_bp
    from routes.main_routes import main_bp
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
