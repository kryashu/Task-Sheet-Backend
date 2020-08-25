import jwt
from application import db
from datetime import datetime, timedelta
from application.configs.jwt import JWTConfig
association_table = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('manager_id', db.Integer, db.ForeignKey('users.id'))
)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(200))
    email = db.Column("email", db.String(200), unique=True)
    task = db.relationship('Task', backref = 'user', lazy = 'joined')
    manager = db.relationship('User',secondary=association_table , backref = 'associate',primaryjoin=id==association_table.c.user_id,secondaryjoin=id==association_table.c.manager_id)

    def __init__(self, name, email):
        self.name = name
        self.email = email
        

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def get_all():
        return User.query.all()
    
    def add_manager(self,manager_email):
        manager = User.get_by_email(manager_email)
        self.manager.append(manager)
        self.save()

    @classmethod
    def get(cls,id):
        return cls.query.filter(cls.id == id).first()    

    @classmethod
    def get_by_email(cls,email):
        return cls.query.filter(cls.email == email).first()
   
    @classmethod
    def generate_access_token(cls, user):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=365),
            "iat": datetime.utcnow(),
            "user_id": user.id,
        }
        access_token = jwt.encode(
            payload, JWTConfig.USER_WEB_AUTH_API_SECRET, algorithm="HS256"
        ).decode("utf-8")
        return access_token



    