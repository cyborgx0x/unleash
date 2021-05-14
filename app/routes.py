import json
import re

from flask import (Flask, Markup, flash, jsonify, redirect, render_template,
                   request, send_file, url_for, session)
from flask_login import current_user, login_required, login_user, logout_user
from img_crop import return_img
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.urls import url_parse
import ast
import requests
from app import app, db
from app.form import (AuthorForm, ChapterForm, FictionForm, LoginForm,
                      Quiz_answer, RegistrationForm)
from app.models import (Author, Chapter, Fiction, FictionIndex, History, Like, Media,
                        Quote, User, Bookmark, AuthorFollowing, UserIndex, AuthorIndex)


@app.route("/")
def index():
    top_view_fictions = Fiction.query.filter_by(status="public").order_by(Fiction.view.desc()).limit(20).all()
    top_authors = Author.query.order_by(Author.fiction_count.desc()).limit(12).all()

    return  render_template("home.html", top_view_fictions = top_view_fictions, top_authors=top_authors)


@app.route('/privacy-policy')
def pp():
    return render_template('pp.html')

@app.route('/TOS')
def tos():
    return render_template('TOS.html')

@app.route('/media/')
def view_all_media():
    medias = Media.query.all()
    return render_template('media.html', medias = medias)


@app.route("/test/search/", methods=['GET', 'POST'])
def test_search():
    return render_template('_search.html')

'''
function area
chứa những chức năng mở rộng
'''

@app.route("/img-cover/<path:link>")
def img_proxy(link):
    url="http://skybooks.vn/wp-content/uploads/2021/03/chung-ta-khong-the-la-ban-tang-kem-bookmark-so-tay-1.jpg"
    print(link)
    img = return_img(link)
    img.seek(0)
    return  send_file(img, mimetype='image/jpeg')


@app.route("/author/<author_name>", methods=['GET', 'POST'])
def author_page(author_name):
    author = Author.query.filter_by(name=author_name).first()
    fictions = Fiction.query.filter_by(author_id=author.id)
    return render_template("author.html", author = author, fictions =fictions)

@app.route("/editor/author/<int:author_id>", methods=['GET', 'POST'])
def edit_author(author_id):
    author = Author.query.filter_by(id=author_id).first()
    if request.method == 'POST':
        incoming_data= json.loads(request.data.decode('UTF-8'))
        print(json.dumps(incoming_data))
        if incoming_data["type"] == "content":
            return jsonify(author.about)
        elif incoming_data["type"] == "upload":
            author.about = json.dumps(incoming_data["value"])
            db.session.commit()
            return "success 🔥🔥🔥"
        elif incoming_data["type"] == "author_name":
            author.name = incoming_data["value"]
            db.session.commit()
            return "success 🔥🔥🔥"
        elif incoming_data["type"] == "author_birth_year":
            author.birth_year = incoming_data["value"]
            db.session.commit()
            return "success 🔥🔥🔥"
        elif incoming_data["type"] == "author_page":
            author.author_page = incoming_data["value"]
            db.session.commit()
            return "success 🔥🔥🔥"
        elif incoming_data["type"] == "author_img":
            author.img = incoming_data["value"]
            db.session.commit()
            return "success 🔥🔥🔥"
    return render_template("author_editor.html", author = author)


@app.route("/authors/")
def all_authors():
    authors = Author.query.all()
    top_authors = Author.query.order_by(Author.fiction_count.desc()).limit(12).all()
    return render_template("authors.html", authors = authors, top_authors=top_authors, title="All Authors")

@app.route("/u/<int:user_id>/following/")
def following_author(user_id):
    following = Author.query.join(Author.follower).filter_by(user_id=user_id)
    top_authors = Author.query.order_by(Author.fiction_count.desc()).limit(12).all()
    return render_template("authors.html", authors = following, top_authors=top_authors, title="Following")

@app.route("/fictions")
def fictions():
    fictions = Fiction.query.filter_by(status="public")
    return  render_template("fictions.html", fictions = fictions)

@app.route("/u/<int:user_id>/liked")
def liked_fiction(user_id):
    fictions = Fiction.query.join(Fiction.like).filter_by(user_id=current_user.id)
    return  render_template("fictions.html", fictions = fictions)


@app.route("/fiction/<int:fiction_id>/", methods=['GET', 'POST'])
def specific_post(fiction_id):
    fiction = Fiction.query.filter_by(id=fiction_id).first()
    return  render_template("viewer.html", fiction = fiction)


@app.route("/fiction/<int:fiction_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_specific_post(fiction_id):
    fiction = Fiction.query.filter_by(id=fiction_id).first()
    authors = Author.query.all()
    if request.method == 'POST':
        incoming_data= json.loads(request.data.decode('UTF-8'))
        print(json.dumps(incoming_data))
        if incoming_data["type"] == "content":
            return jsonify(fiction.desc)
        elif incoming_data["type"] == "upload":
            try: 
                fiction.desc = json.dumps(incoming_data["value"])
                print(fiction.desc)
                db.session.commit()
                return "Đã cập nhật lời tựa"
            except:
                return "incoming data invalid"
        elif incoming_data["type"] == "init":
            return render_template("_editorjs.html")
        elif incoming_data["type"] == "publish_year":
            fiction.publish_year = incoming_data["value"]
            db.session.commit()
            return "year updated"
        elif incoming_data["type"] == "fiction_name":
            fiction.name = incoming_data["value"]
            db.session.commit()
            return "name updated"
        elif incoming_data["type"] == "tag-manage":
            fiction.tag = incoming_data["value"]
            db.session.commit()
            return "tag updated"
        elif incoming_data["type"] == "link-download":
            fiction.mediafire_link = incoming_data["value"]
            db.session.commit()
            return "link download updated"
        elif incoming_data["type"] == "book-cover":
            fiction.cover = incoming_data["value"]
            db.session.commit()
            return "Đã cập nhật ảnh bìa"
        elif incoming_data["type"] == "short-desc":
            fiction.short_desc = incoming_data["value"]
            db.session.commit()
            return "Mô tả ngắn được cập nhật"
        elif incoming_data["type"] == "fiction-author":
            fiction.author_id = incoming_data["value"]
            db.session.commit()
            return "Đã cập nhật tác giả"
        elif incoming_data["type"] == "fiction-status":
            fiction.status = incoming_data["value"]
            db.session.commit()
            return "Đã đăng tác phẩm"
    return  render_template("editor.html", fiction = fiction, authors=authors)


@app.route("/fiction/<fiction_name>/")
def specific_fiction_name(fiction_name):
    fiction = Fiction.query.filter_by(name=fiction_name).first()
    return  render_template("viewer.html", fiction = fiction)


@app.route("/chapter/<int:chapter_id>/")
def chapter_viewer(chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    chapter.update_view()
    fiction = Fiction.query.filter_by(id=chapter.fiction).first()
    chapters = Chapter.query.filter_by(fiction=fiction.id).order_by(Chapter.chapter_order.asc())
    return render_template('chapter.html', chapter = chapter, fiction=fiction, chapters = chapters)



@app.route("/editor/<int:chapter_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_chapter(chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    if request.method == 'POST':
        incoming_data = json.loads(request.data.decode('UTF-8'))
        if incoming_data["type"] == "chapter_name":
            chapter.name = incoming_data["value"]
            db.session.commit()
            return "Đã cập nhật tên chương"
        if incoming_data["type"] == "chapter_order":
            chapter.chapter_order = incoming_data["value"]
            db.session.commit()
            return "Đã cập nhật thứ tự"
        elif incoming_data["type"] == "content":
            return jsonify(chapter.content)
        elif incoming_data["type"] == "upload":
            chapter.content = json.dumps(incoming_data["value"])
            print(chapter.content)
            db.session.commit()
            return "Đã cập nhật nội dung chương"
    return render_template('chapter_editor.html', chapter=chapter)


@app.route("/quote/<int:quote_id>", methods = ['GET'])
def get_quote(quote_id):
    quote = Quote.query.filter_by(id=quote_id).first()
    author = Author.query.filter_by(id=quote.author_id).first()
    fiction = Fiction.query.filter_by(id=quote.fiction).first()
    return render_template("quote.html", quote = quote, author = author, fiction = fiction)


'''
API SESSION
Contain interaction with the request from client
'''

@app.route ("/api/bookmark/", methods=['POST'])
def bookmark_api():
    if request.method == 'POST':
        incoming_data= json.loads(request.data.decode('UTF-8'))
        if incoming_data['value'] == "remove":
            item = Bookmark.query.filter_by(chapter_id=incoming_data['chapter'], user_id=current_user.id).delete()
            db.session.commit()
            return "remove bookmark successfully"
        else:
            newitem = Bookmark(user_id=current_user.id, chapter_id=incoming_data['chapter'])
            db.session.add(newitem)
            db.session.commit()
            return "added bookmark successfully"
    return "message received"


@app.route("/editor/<int:fiction_id>/new-chapter/", methods=['GET', 'POST'])
def new_chapter(fiction_id):
    form=ChapterForm()
    if form.validate_on_submit():
        content = form.content.data 
        content.replace("\/r\/n",'</p><p>')
        new_chapter = Chapter(name=form.name.data, content=content, chapter_order=form.chapter_order.data, fiction=fiction_id)
        db.session.add(new_chapter)
        db.session.commit()
        db.session.refresh(new_chapter)
        return redirect(url_for('chapter_viewer', chapter_id=new_chapter.id))
    new_chapter = Chapter(name="New Chapter", fiction=fiction_id)
    db.session.add(new_chapter)
    db.session.commit()
    db.session.refresh(new_chapter)
    return redirect(url_for('edit_chapter', chapter_id=new_chapter.id))


@app.route("/build_indexing/", methods=['GET', 'POST'])
def build_indexing():
    fictions=FictionIndex.query.all()
    users = UserIndex.query.all()
    authors = AuthorIndex.query.all()
    if request.method=='POST':
        incoming_data = json.loads(request.data.decode('UTF-8'))
        if incoming_data["query"] == "author":
            return jsonify(authors)           
    return jsonify(fictions)



@app.route("/new-author/")
def new_author():
    new_author = Author(name="Tên Tác Giả", user_id=current_user.id)
    db.session.add(new_author)
    db.session.commit()
    db.session.refresh(new_author)
    return redirect(url_for('edit_author', author_id=new_author.id))

@app.route("/new-fiction/", methods=['GET', 'POST'])
def new_fiction():
    new_fiction = Fiction(name="Tác phẩm mới")
    db.session.add(new_fiction)
    db.session.commit()
    db.session.refresh(new_fiction)
    return redirect(url_for('edit_specific_post', fiction_id=new_fiction.id))


@app.route("/user/fiction/<int:fiction_id>/",methods=['GET', 'POST'])
def update_like(fiction_id):
    if request.method == 'POST':
        incoming_data= json.loads(request.data.decode('UTF-8'))
        print(incoming_data)
        if incoming_data['type'] == 'heart':
            if incoming_data['value'] == True:
                like = Like(user_id=current_user.id, fiction_id=fiction_id)
                db.session.add(like)
                db.session.commit()
                fiction_like = Like.query.filter_by(fiction_id=fiction_id).count()
                return "has " + str(fiction_like) + " ❤"
            else:
                itemdelete = Like.query.filter_by(user_id=current_user.id,fiction_id=fiction_id).delete()
                db.session.commit()
                fiction_like = Like.query.filter_by(fiction_id=fiction_id).count()
                return "has " + str(fiction_like) + " ❤"
    return {"message":"like updated"}


@app.route("/api/following/author/",methods=['GET', 'POST'])
def update_author_follower():
    if request.method == 'POST':
        incoming_data= json.loads(request.data.decode('UTF-8'))
        data = incoming_data['data']
        print(incoming_data)
        if data['type'] == "author-follow" and data['value'] == "follow":
            AuthorFollowing.query.filter_by(user_id=current_user.id,author_id=int(data['author'])).delete()
            db.session.commit()
            string = " follower 🧑"
            follower = AuthorFollowing.query.filter_by(author_id=int(data['author'])).count()
            return "<strong>" + str(follower) + string + "</strong>"
        elif data['type'] == "author-follow" and data['value'] == "followed":
            author_follower = AuthorFollowing(user_id=current_user.id, author_id=int(data['author']))
            db.session.add(author_follower)
            db.session.commit()
            string = " follower 🧑"
            follower = AuthorFollowing.query.filter_by(author_id=int(data['author'])).count()
            return "<strong>" + str(follower) + string + "</strong>"
    return "no input"


@app.route("/api/all_authors/", methods = ['GET'])
def api_all_authors():
    authors=Author.query.all()
    return jsonify(authors)

@app.route("/api/<int:fiction_id>/", methods = ['GET'])
def api_send_fiction(fiction_id):
    fiction = Fiction.query.filter_by(id=fiction_id).first()
    chapter = Chapter.query.filter_by(fiction=fiction_id) 
    return jsonify(fiction)
    

@app.route("/api/<int:fiction_id>/<int:chapter_order>", methods = ['GET'])
def api_send_chapter_content(chapter_order, fiction_id):
    chapter = Chapter.query.filter_by(fiction=fiction_id, chapter_order=chapter_order).first()
    return jsonify(chapter)


@app.route("/api/chapter/<int:chapter_id>/", methods = ['GET'])
def api_chapter_id(chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    return jsonify(chapter)

@app.route("/api/chapter_list_by_fiction/<int:fiction_id>", methods = ['GET'])
def api_send_chapter_list(fiction_id):
    chapter = Chapter.query.filter_by(fiction=fiction_id)
    newdict ={}
    for c in chapter:
       newdict[c.id] = c.name
    return newdict

'''
DANGER SESSION
contain link and API for delete item
must control it with carefully behaviour
'''

@app.route("/fiction/<int:fiction_id>/delete", methods=['GET', 'POST'])
def delete_fiction(fiction_id):
    chapters = Chapter.query.filter_by(fiction=fiction_id).delete()
    fiction = Fiction.query.filter_by(id=fiction_id).delete()
    db.session.commit()
    return  redirect(url_for("specific_post", fiction_id=fiction.id))

@app.route("/chapter/<int:chapter_id>/delete", methods=['GET', 'POST'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    fiction = Fiction.query.filter_by(id=chapter.fiction).first()
    chapter = Chapter.query.filter_by(id=chapter_id).delete()
    db.session.commit()
    return  redirect(url_for("specific_post", fiction_id=fiction.id))

@app.route("/author/<int:author_id>/delete")
def delete_author(author_id):
    fictions = Fiction.query.filter_by(author_id=author_id).delete()
    author = Author.query.filter_by(id=author_id).delete()
    db.session.commit()
    return redirect(url_for('all_authors'))

'''
User Session
Contain route about user authentication, profile, configuration and dashboard
'''
@app.route('/authorized', methods=['GET','POST'])
def authorized():
    access_token = request.args.get("access_token")
    print(access_token)
    return redirect("/")



@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        incoming_data = json.loads(request.data.decode('UTF-8'))
        incoming_data = incoming_data['data']
        core_url = "https://graph.facebook.com/v10.0/me?fields=id%2Cname&access_token="
        access_token = incoming_data['authResponse']['accessToken']
        facebook_id = incoming_data['authResponse']['userID']
        auth = requests.get(core_url + access_token)
        print(auth)
        if auth.status_code == 200:
            r = json.loads(auth.text)
            id = r['id']
            name = r['name']
            user = User.query.filter_by(facebook=id).first()
            if user is None:
                new_user = User(facebook=id, name=name)
                db.session.add(new_user)
                db.session.commit()
                db.session.refresh(new_user)
                login_user(new_user,duration=incoming_data['authResponse']['data_access_expiration_time'])
                return "added" 
            login_user(user,duration=incoming_data['authResponse']['data_access_expiration_time'])
            return "signed"
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form = form)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.firstname.data, last_name=form.lastname.data, user_name=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('reg.html', title='Register', form=form)

@app.route('/u/<id>')
@login_required
def user(id):
    user = User.query.filter_by(id=id).first_or_404()
    fictions = Fiction.query.join(Fiction.like).filter_by(user_id=current_user.id)
    all_fictions = Fiction.query.all()
    all_authors = Author.query.all()
    return render_template('dash.html', user=user, fictions=fictions, all_fictions=all_fictions, all_authors=all_authors)

