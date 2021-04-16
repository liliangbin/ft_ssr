from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'ft_user'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    user_name = db.Column(db.String(64), comment='用户名，没啥用')
    wx_name = db.Column(db.String(256), unique=True)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    key = db.Column(db.String(256), unique=True, comment='用户请求唯一key，路由上用')

    def __repr__(self):
        return '< user %r>' % self.user_name
