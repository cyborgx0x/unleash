from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import JSON, Boolean, MetaData, Text
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login

meta = MetaData()


class Fiction(db.Model):
    "fiction", meta
    __tablename__ = "fiction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(300))
    status = db.Column(db.Unicode(300), default="draft")
    view = db.Column(db.Integer, default=0)
    desc = db.Column(JSON)
    cover = db.Column(db.Text)
    publish_year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    tiki_link = db.Column(db.Text)
    mediafire_link = db.Column(db.Text)
    slug = db.Column(db.String(160))
    version = db.Column(db.Integer)
    chapters = db.relationship("Chapter", backref="fiction_r")
    short_desc = db.Column(db.String(160))
    tag = db.Column(db.Unicode(300))
    like = db.relationship("Like", backref="fiction")
    media = db.relationship("Media", backref="fiction")
    history = db.relationship("History", backref="fiction")
    follower = db.relationship("FictionFollowing", backref="fiction")
    quote = db.relationship("Quote")
    task = db.relationship("Task")
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "cover": self.cover,
            "tag": self.tag,
            "publish_year": self.publish_year,
            "status": self.status,
            "view": self.view,
            "page_count": self.page_count,
            "author_id": self.author_id,
            "tiki_link": self.tiki_link,
            "mediafire_link": self.mediafire_link,
            "slug": self.slug,
            "version": self.version,
            "short_desc": self.short_desc,
        }

    def update_view(self):
        try:
            self.view += 1
        except:
            self.view = 1
        db.session.commit()

    def __repr__(self):
        return "{}>".format(self.name)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fiction = db.Column(db.Integer, db.ForeignKey("fiction.id"))


class Chapter(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(160))
    content = db.Column(JSON)
    view_count = db.Column(db.Integer)
    fiction = db.Column(db.Integer, db.ForeignKey("fiction.id"))
    bookmark = db.relationship("Bookmark", backref="chapter")
    chapter_order = db.Column(db.Integer)
    history = db.relationship("History", backref="chapter")
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,  # Consider security/size implications of sending content
            "view_count": self.view_count,
            "fiction": self.fiction,
            "chapter_order": self.chapter_order,
            # You may choose to include or exclude details about relationships depending on the use case
            # For instance, 'bookmarks' and 'history' might be summarized or detailed further if necessary
            # "bookmarks": [bookmark.serialize() for bookmark in self.bookmark] if self.bookmark else [],
            # "history": [history.serialize() for history in self.history] if self.history else [],
        }

    def update_view(self):
        if self.view_count:
            self.view_count = self.view_count + 1
        else:
            self.view_count = 1
        db.session.commit()


class Author(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(160))
    birth_year = db.Column(db.Integer)
    author_page = db.Column(db.String(160))
    about = db.Column(JSON)
    view = db.Column(db.Integer)
    fiction = db.relationship("Fiction", backref="author")
    media = db.relationship("Media", backref="author")
    email = db.Column("email", db.String(120))
    img = db.Column(db.String(240))
    fiction_count = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    history = db.relationship("History", backref="author")
    follower = db.relationship("AuthorFollowing", backref="author")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "author_page": self.author_page,
            "about": self.about,
            "view": self.view,
            "email": self.email,
            "img": self.img,
            "fiction_count": self.fiction_count,
            # Relationships like 'fiction', 'media', 'history', 'follower' can be serialized similarly if needed
            # Example: "fictions": [fiction.serialize() for fiction in self.fiction] if self.fiction else [],
        }


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quote = db.Column(db.Text)
    fiction = db.Column(db.Integer, db.ForeignKey("fiction.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    history = db.relationship("History", backref="quote")

    img = db.Column(db.Text)


class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(300))
    content = db.Column(db.Text)
    media_type = db.Column(db.Unicode(300))
    fiction_id = db.Column(db.Integer, db.ForeignKey("fiction.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    history = db.relationship("History", backref="media")


class Like(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    fiction_id = db.Column(db.Integer, db.ForeignKey("fiction.id"), primary_key=True)


class User(UserMixin, db.Model):
    "users", meta
    id = db.Column("id", db.Integer, primary_key=True)
    facebook = db.Column(db.String(50))
    first_name = db.Column(db.Unicode(256))
    last_name = db.Column(db.Unicode(256))
    user_name = db.Column("user_name", db.String(64))
    avatar = db.Column(db.String(200))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column("email", db.String(120))
    password_hash = db.Column(db.String(256))
    like = db.relationship("Like", backref="user")
    bookmark = db.relationship("Bookmark", backref="user")
    media = db.relationship("Media", backref="user")
    author = db.relationship("Author", backref="user")
    history = db.relationship("History", backref="user")
    fictions = db.relationship("Fiction", backref="creator")
    author = db.relationship("Author", backref="creator")
    following = db.relationship(
        "UserFollowing",
        foreign_keys="[UserFollowing.user_id]",
        backref="user_following",
    )
    follower = db.relationship(
        "UserFollowing",
        foreign_keys="[UserFollowing.user_following_id]",
        backref="user_follower",
    )
    author_following = db.relationship(
        "AuthorFollowing",
        foreign_keys="[AuthorFollowing.user_id]",
        backref="user_following",
    )
    fiction_following = db.relationship(
        "FictionFollowing",
        foreign_keys="[FictionFollowing.user_id]",
        backref="user_following",
    )
    is_admin = db.Column(Boolean, default=False)
    is_mod = db.Column(Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Bookmark(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), primary_key=True)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"))
    fiction_id = db.Column(db.Integer, db.ForeignKey("fiction.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    quote_id = db.Column(db.Integer, db.ForeignKey("quote.id"))
    media_id = db.Column(db.Integer, db.ForeignKey("media.id"))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.String(300))
    type = db.Column(db.String(30))


class UserFollowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_following_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    time = db.Column(db.DateTime, default=datetime.utcnow)


class AuthorFollowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    time = db.Column(db.DateTime, default=datetime.utcnow)


class FictionFollowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("fiction.id"))
    time = db.Column(db.DateTime, default=datetime.utcnow)
