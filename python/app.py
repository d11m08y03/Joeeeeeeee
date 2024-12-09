from flask import Flask
from flask_login import LoginManager
from database import db
from controllers.auth import auth_blueprint
from controllers.chat import chat_blueprint

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# Register Blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(chat_blueprint)


@login_manager.user_loader
def load_user(user_id):
    from models.user import User

    return User.query.get(int(user_id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
