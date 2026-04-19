import os

from flask import Flask

from routes import main_blueprint


def create_app():
    # Factory principale dell'app Flask: centralizza configurazione e route.
    app = Flask(__name__, template_folder="TEMPLATES", static_folder="STATIC")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "mydex-dev-secret-key")
    app.register_blueprint(main_blueprint)
    return app


# Istanza usata sia in locale sia da eventuali server WSGI.
app = create_app()


if __name__ == "__main__":
    # Avvio in sviluppo locale.
    app.run(debug=True)
