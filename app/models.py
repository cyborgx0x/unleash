from dataclasses import dataclass
from datetime import datetime
from hashlib import md5
import ast
import json
from flask_login import UserMixin
from sqlalchemy import MetaData, Text
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login

meta = MetaData()

@dataclass
class Fiction(db.Model):
    'fiction', meta
    id: int
    name: str
    desc: str
    cover: str
    tag: str

    __tablename__ = "fiction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(300))
    status = db.Column(db.Boolean,  default = True)
    view = db.Column(db.Integer)
    desc = db.Column(db.Text)
    cover = db.Column(db.Text)
    publish_year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    tiki_link = db.Column(db.Text)
    mediafire_link = db.Column(db.Text)
    slug = db.Column(db.String(160))
    version = db.Column(db.Integer)
    chapter_count = db.Column(db.Integer)
    quote_count = db.Column(db.Integer)
    chapter = db.relationship('Chapter')
    tag = db.Column(db.Unicode(300))
    like = db.relationship('Like', backref ='fiction')
    media = db.relationship('Media', backref='fiction')

    def cutText(self):
        text = ast.literal_eval(self.desc)
        return text
    def set_count(self, chapter_count):
        self.chapter_count = chapter_count
        print("update completed")    
    def set_view(self, total_view):
        self.view = total_view
        print("update completed")    

    def __repr__(self):
        return 'Fiction info {}>'.format(self.name)


@dataclass
class FictionIndex(Fiction):
    id:int
    name: str
    desc: str 

    
@dataclass
class Chapter(db.Model):
    id:int
    name: str
    content: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(160))
    content = db.Column(db.Text)
    view_count = db.Column(db.Integer)
    fiction = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    bookmark = db.relationship('Bookmark', backref ='chapter')
    chapter_order = db.Column(db.Integer)
    def update_view(self):
        if self.view_count:
            self.view_count=self.view_count+1
        else:
            self.view_count = 1
        print(self.id, self.name, self.view_count)
        db.session.commit()
    def update_chapter_count_zero(self, count):
        self.view_count = count
        db.session.commit()
    def cutText(self):
        text = ast.literal_eval(self.content)
        return text


@dataclass
class Author(db.Model):
    id: int
    name: str 
    img: str
    fiction: Fiction
    about: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(160))
    birth_year = db.Column(db.Integer)
    author_page = db.Column(db.String(160))
    about = db.Column(db.Text)
    view = db.Column(db.Integer)
    fiction = db.relationship('Fiction', backref ='author')
    media = db.relationship('Media', backref ='author')
    email = db.Column('email', db.String(120))
    img = db.Column(db.String(240))
    fiction_count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def cutText(self):
        text = ast.literal_eval(self.about)
        return text
    def set_count(self, fiction_number):
        self.fiction_count = fiction_number
        print("update completed")
    def update_fiction_count(self):
        fiction_number = Fiction.query.filter_by(author_id=self.id).count()  
        self.fiction_count = fiction_number
        print (self.name, fiction_number)
        db.session.commit()
    def getChapter(self, fiction_id):
        chapters = Chapter.query.filter_by(fiction=fiction_id)
        return chapters

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quote = db.Column(db.Text)
    fiction = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    img = db.Column(db.Text)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(300))
    content = db.Column(db.Text)
    post_type = db.Column(db.Unicode(300))
    template = db.Column(db.Unicode(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def cutText(self):
        text = json.loads(self.content)
        return text
    def getFiction(self, id):
        fic = Fiction.query.filter_by(id=id).first()
        return fic
    def getMedia(self, id):
        getdata = Media.query.filter_by(id=id).first()
        return getdata

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(300))
    content = db.Column(db.Text)
    media_type = db.Column(db.Unicode(300))
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def cutText(self):
        text = json.loads(self.content)
        return text
    def getUser(self, id):
        user = User.query.filter_by(id=id).first()
        return user
    def getAuthor(self, id):
        author = Author.query.filter_by(id=id).first()
        return author

    def getFiction(self, id):
        fic = Fiction.query.filter_by(id=id).first()
        return fic
    def getMedia(self, id):
        getdata = Media.query.filter_by(id=id).first()
        return getdata

class Like(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'), primary_key=True)


class User(UserMixin, db.Model):
    'users', meta
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name',db.Unicode(50))
    last_name = db.Column('last_name',db.Unicode(50))
    user_name = db.Column('user_name', db.String(64))
    email = db.Column('email', db.String(120))
    password_hash = db.Column(db.String(128))
    like = db.relationship('Like', backref ='user')
    post = db.relationship('Post', backref ='user')
    media = db.relationship('Media', backref ='user')
    author = db.relationship('Author', backref ='user')
    # post = db.relationship('Post', backref ='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column (db.DateTime, default = datetime.utcnow)
    def __repr__(self):
        return '<User {}>'.format(self.user_name)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Bookmark(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), primary_key=True)
