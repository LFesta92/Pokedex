from flask import Flask

from routes import main_blueprint


def create_app():
    app = Flask(__name__, template_folder="TEMPLATES", static_folder="STATIC")
    app.register_blueprint(main_blueprint)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
