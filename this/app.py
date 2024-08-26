from flask import Flask, render_template, session, redirect
import sqlalchemy
import os

secret_key=os.environ.get('SECRET_KEY')

db_password=os.environ.get('DB_PASSWORD')
db_user=os.environ.get('DB_USER')
host=os.environ.get('HOST')
db_name=os.environ.get('DATABASE')
db_path = "./data"

def create_app():
    app=Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='secret_key',
        ENGINE= sqlalchemy.create_engine(f"sqlite:///{db_path}")
    )

    import this.blog
    app.register_blueprint(this.blog.bp)

    import this.auth
    app.register_blueprint(this.auth.bp)

    @app.route('/', methods=['GET', 'POST'])
    def home():
            return render_template('index.html', posts=blog.front_posts())
    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/')
    
    import this.db
    this.db.init_app(app)
    return app

app = create_app()