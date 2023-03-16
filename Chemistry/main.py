from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import LoginManager, login_user

from blueprint import jobs_api
from data.users import User
from forms.form import LoginForm
from data import db_session


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(jobs_api.blueprint)
    app.run(port='5001')


main()
