from extensions import db, pwd_context

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def validate_user_password(cls, username: str, password: str):
        user = cls.query.filter_by(username=username).first()
        if user and pwd_context.verify(password, user.password):
            return user
        return None

    def save_to_db(self):
        self.password = pwd_context.hash(self.password)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
