from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager # jwt_required
from passlib.context import CryptContext

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
