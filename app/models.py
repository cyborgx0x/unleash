import ast
import json
from dataclasses import dataclass
from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from sqlalchemy import JSON, Boolean, MetaData, Text
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
    status = db.Column(db.Unicode(300), default ="draft")
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
    chapter = db.relationship('Chapter')
    short_desc = db.Column(db.String(160))
    tag = db.Column(db.Unicode(300))
    like = db.relationship('Like', backref ='fiction')
    media = db.relationship('Media', backref='fiction')
    history = db.relationship('History', backref ='fiction')
    follower = db.relationship('FictionFollowing', backref ='fiction')
    quote = db.relationship('Quote')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def cutText(self):
        try: 
            file = json.loads(self.desc)
            return file
        except:
            return 'nội dung chứa ký tự không hợp lệ'
    def set_count(self, chapter_count):
        self.chapter_count = chapter_count
        print("update completed")    
    def set_view(self, total_view):
        self.view = total_view
        print("update completed")    

    def __repr__(self):
        return '{}>'.format(self.name)


    
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
    history = db.relationship('History', backref ='chapter')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

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
        try: 
            file = json.loads(self.content)
            return file
        except:
            return 'nội dung chứa ký tự không hợp lệ'
    def __repr__(self):
        return '{}>'.format(self.name)




@dataclass
class Author(db.Model):
    id: int
    name: str 
    img: str
    about: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(160))
    birth_year = db.Column(db.Integer)
    author_page = db.Column(db.String(160))
    about = db.Column(JSON)
    view = db.Column(db.Integer)
    fiction = db.relationship('Fiction', backref ='author')
    media = db.relationship('Media', backref ='author')
    email = db.Column('email', db.String(120))
    img = db.Column(db.String(240))
    fiction_count = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    history = db.relationship('History', backref ='author')
    follower = db.relationship('AuthorFollowing', backref ='author')


    def set_count(self, fiction_number):
        self.fiction_count = fiction_number
        print("update completed")
    def update_fiction_count(self):
        fiction_number = Fiction.query.filter_by(author_id=self.id).count()  
        self.fiction_count = fiction_number
        print (self.name, fiction_number)
        db.session.commit()


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quote = db.Column(db.Text)
    fiction = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    history = db.relationship('History', backref ='quote')

    img = db.Column(db.Text)



class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(300))
    content = db.Column(db.Text)
    media_type = db.Column(db.Unicode(300))
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    history = db.relationship('History', backref ='media')

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
    def __repr__(self):
        return '{}>'.format(self.media_type)

class Like(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'), primary_key=True)

@dataclass
class User(UserMixin, db.Model):

    'users', meta
    id = db.Column('id', db.Integer, primary_key=True)
    facebook = db.Column(db.String(50))
    first_name = db.Column(db.Unicode(256))
    last_name = db.Column(db.Unicode(256))
    user_name = db.Column('user_name', db.String(64))
    avatar = db.Column(db.String(200))
    about_me = db.Column(db.String(140))
    last_seen = db.Column (db.DateTime, default = datetime.utcnow)
    email = db.Column('email', db.String(120))
    password_hash = db.Column(db.String(128))
    like = db.relationship('Like', backref ='user')
    bookmark = db.relationship('Bookmark', backref ='user')
    media = db.relationship('Media', backref ='user')
    author = db.relationship('Author', backref ='user')
    history = db.relationship('History', backref ='user')
    fictions = db.relationship('Fiction', backref ='creator')
    author = db.relationship('Author', backref ='creator')
    following = db.relationship('UserFollowing', foreign_keys='[UserFollowing.user_id]', backref ='user_following')
    follower = db.relationship('UserFollowing', foreign_keys='[UserFollowing.user_following_id]', backref ='user_follower')
    author_following = db.relationship('AuthorFollowing', foreign_keys='[AuthorFollowing.user_id]', backref ='user_following')
    fiction_following = db.relationship('FictionFollowing', foreign_keys='[FictionFollowing.user_id]', backref ='user_following')
    is_admin = db.Column(Boolean, default=False)
    is_mod = db.Column(Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))




class Bookmark(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), primary_key=True)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    fiction_id = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'))
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'))
    time = db.Column(db.DateTime, default = datetime.utcnow)
    content = db.Column(db.String(300))
    type = db.Column(db.String(30))

class UserFollowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_following_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime, default = datetime.utcnow)

class AuthorFollowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    time = db.Column(db.DateTime, default = datetime.utcnow)

class FictionFollowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('fiction.id'))
    time = db.Column(db.DateTime, default = datetime.utcnow)


@dataclass
class FictionIndex(Fiction):
    id: int
    name: str
    desc: str
    cover: str
    tag: str


@dataclass
class UserIndex(User):
    id:int
    user_name: str

@dataclass
class AuthorIndex(Author):
    id:int
    name: str

