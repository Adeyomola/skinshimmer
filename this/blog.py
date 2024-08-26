from this.db import get_db
from this.metadata import metadata
from flask import request, render_template, flash, redirect, session, Blueprint, g, url_for
from sqlalchemy import insert, select, delete, update
from sqlalchemy.engine import ResultProxy
from sqlalchemy.exc import IntegrityError
from this.auth import login_required
import re
from this.uploads import Upload
from this.verify import Verify

bp = Blueprint('blog', __name__, template_folder='templates', static_folder='static', static_url_path='/blog/static')

md = metadata()
table = md.tables['post']

def author_posts():
    connection = get_db()
    statement = (select(table).where(table.c.author_id == session['user_id']))
    posts = connection.execute(statement).fetchall()
    connection.close()
    return posts

def front_posts():
    connection = get_db()
    statement = (select(table))
    posts = connection.execute(statement).fetchmany(8)
    connection.close()
    return posts

@bp.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    if request.method == 'POST':
        error = None
        title = request.form['title']
        body = request.form['body']
        category = request.form['category']

        connection = get_db()
        image_url = Upload.upload_file(Upload)
        if error is None:
            try:
                statement = (insert(table).values(title=title, author_id=g.get('user')[0], firstname=g.get('user')[1], body=body, image_url=image_url, category=category))
                connection.execute(statement)
                connection.commit()
                return redirect('/')
            except IntegrityError as ie:
                error = ie._message()
                connection.rollback()
                if re.search('title', error):
                    error = "An article with this title already exists"
                elif re.search('body', error):
                    error = "This article might be a duplicate"
            finally:
                connection.close()
        flash(error)
    return render_template('write.html')

@bp.route('/post', strict_slashes=False)
def post():
    connection = get_db()
    statement = (select(table))
    posts = connection.execute(statement).fetchall()
    connection.close()
    return render_template('post.html', posts=posts)

@bp.route('/<post_category>/<post_title>', methods=['GET', 'POST'])
def get_post(post_title, post_category):
    connection = get_db()
    Verify.verify_post(post_title, table, connection)

    statement = (select(table).where(table.c.title == post_title and table.c.category == post_category))
    post_row = connection.execute(statement)
    post_row = ResultProxy.fetchone(post_row)

    tab = md.tables['comments']
    get_comments = (select(tab).where(tab.c.post == post_row[0]))
    comments = connection.execute(get_comments).fetchmany(5)

    users = md.tables['users']
    author_image = connection.execute((select(users.c.image_url).where(users.c.id == post_row[1])))
    author_image = ResultProxy.fetchone(author_image)[0]

    if request.method == 'POST':
        error = None
        comment = request.form['comment']
        name = request.form['name']
        
        if error is None:
            try:
                statement = (insert(tab).values(post=post_row[0], name=name, comment=comment))
                connection.execute(statement)
                connection.commit()
                return redirect("/" + post_category + "/" + post_title)
            except IntegrityError as ie:
                error = ie._message()
                connection.rollback()
                if re.search('comment', error):
                    error = "Duplicate comment"
            finally:
                connection.close()
        flash(error)

    connection.close()
    return render_template('get_post.html', post_row=post_row, author_image=author_image, comments=comments)

@bp.route('/post/update/<post_title>',  methods=['GET', 'POST'])
@login_required
def update_post(post_title):
    connection = get_db()
    Verify.verify_author(post_title, table, connection)
    post_row = ResultProxy.fetchone(connection.execute(select(table).where(table.c.title == post_title)))
    if request.method == 'POST':
        try:
            if request.files['file'] and post_row[6]:
                Upload.delete_file(post_row[6])
                image_url = Upload.upload_file(Upload)
            elif request.files['file'] and not post_row[6]:
                image_url = Upload.upload_file(Upload)
            elif post_row[6]:
                image_url = post_row[6]
            else:
                image_url = None
                
            title = request.form['title']
            body = request.form['body']
            category = request.form['category']

            connection.execute((update(table).where(table.c.title == post_title).values(title=title, body=body, image_url=image_url, category=category)))
            connection.commit()
            return redirect(url_for('blog.get_post', post_title=title, post_category=category))
        finally:
            connection.close()
    connection.close()
    return render_template('update.html', post_row=post_row)

@bp.route('/post/delete/<post_title>',  methods=['POST', 'GET'])
@login_required
def delete_post(post_title):
    if request.method == 'GET':
        return redirect('/')
    
    connection = get_db()
    Verify.verify_author(post_title, table, connection)

    post_image = connection.execute((select(table.c.image_url).where(table.c.title == post_title)))
    post_image = ResultProxy.fetchone(post_image)[0]

    if post_image:
        Upload.delete_file(post_image)

    connection.execute((delete(table).where(table.c.title == post_title)))
    connection.commit()
    connection.close()
    return redirect(url_for('blog.post'))