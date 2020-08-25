from application import db
from datetime import datetime, timedelta


class Task(db.Model):
    _tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(2000))
    url = db.Column(db.String(1000))
    created_by = db.Column(db.Integer , db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime)
    end_on = db.Column(db.DateTime)

    def __init__(self, name, created_by, description , url):
        self.name = name
        self.created_by = created_by
        self.description = description
        self.url = url
        self.created_on = datetime.utcnow()
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def end_now(self):
        self.end_on = datetime.utcnow()
        self.save()

    @classmethod
    def get(cls,id):
        return cls.query.filter(cls.id == id).first()
    
    