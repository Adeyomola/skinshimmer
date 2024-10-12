from flask import Flask, render_template, session, redirect, send_from_directory
import sqlalchemy
import os
import urllib.parse as up
from datetime import timedelta

secret_key=os.environ.get('SECRET_KEY')

db_password=up.quote_plus(os.environ.get('DB_PASSWORD'))
db_user=os.environ.get('DB_USER')
host=os.environ.get('HOST')
db_name=os.environ.get('DATABASE')
db_path = "./data"

def create_app():
    app=Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        ENGINE= sqlalchemy.create_engine(f"mysql://{db_user}:{db_password}@{host}/{db_name}")
    )

    from . import blog
    app.register_blueprint(blog.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/', methods=['GET', 'POST'])
    def home():
            return render_template('index.html', posts=blog.front_posts())
    
    @app.route('/privacy', methods=['GET'])
    def privacy():
            return render_template('privacy.html')
    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/')
    
    @app.route('/sitemap.xml')
    def sitemap():
          return send_from_directory(app.static_folder, 'sitemap.xml')

    from . import db
    db.init_app(app)
    return app

app = create_app()