from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from sqlalchemy.sql.expression import func
from data import db_session
from data.login import LoginForm
from data.__all_models import *
from data.register import RegisterForm
# from data.new_game import NewGameForm
# from flask_restful import abort

import json
import datetime
import random

from candinsky_and_gigachat.giga import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JGKzpcce9ajD72k'

login_manager = LoginManager()
login_manager.init_app(app)

alphabet = [list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"[i:i + 3]) for i in range(0, 33, 3)]

messages = [
    SystemMessage(
        content="Ты помогаешь детям писать сказки подсказывая им и художественно дополняя их предложения."
    )
]


@login_manager.user_loader
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
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/test')
def test():
    return render_template('index.html')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ntale", methods=['POST', 'GET'])
def new_tale():
    db_sess = db_session.create_session()
    history = History(
        user_id=current_user.id,
        giga_id=get_token(auth).json()['access_token'],
        story=""
    )
    db_sess.add(history)
    db_sess.commit()
    return redirect('/tale')


@app.route("/tale", methods=['POST', 'GET'])
def last_tale():
    db_sess = db_session.create_session()
    history = db_sess.query(History).filter(History.user_id == current_user.id).order_by(History.id.desc()).first()
    if request.method == 'GET':
        text = history.story.split("$$$")
        return render_template("test.html", story_content=text)
    elif request.method == 'POST':
        print(request.form['story'])
        user_input = request.form['story']
        print(history.story)
        print()
        print(user_input)
        messages.append(HumanMessage(content=f'Ты - писатель, который составляет сказки вместе с ребенком. Ты и '
                                             f'пользователь вместе пишите сказку. Ты должен дополнять сказку ТОЛЬКО'
                                             f'на 2 '
                                             f'предложения. Повествование последовательное. Добавляй как '
                                             f'можно больше деталей внешности и описания окружающей среды. Если '
                                             f'пользователь затрудняется с описанием, то придумай сам. Если '
                                             f'пользователь сам описывает историю, то ты просто продолжаешь. История '
                                             f'должна быть логически правильно построенной. Сюжет понятный. Далее, в '
                                             f'кавычках, будет приведено начало сказки, если они пусты, то значит это '
                                             f'сказка новая, если нет, то продолжай эту."{history.story + user_input}"'
                                             f'Ты дополняешь историю ТОЛЬКО НА 2 ПРЕДЛОЖЕНИЯ. При выведении ответа не '
                                             f'пиши двойные скобки'))
        res = chat(messages)
        messages.append(res)
        # Ответ модели
        history.story += f"{user_input}$$${res.content}$$$"
        db_sess.commit()
        # create_json(user_input + res.content)
        # history += f"Bot: {res.content} "
        text = history.story.split("$$$")

        print(text)

        return render_template("test.html", story_content=text)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        # print(form.email.data)
        # print(form.login.data)
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="Пользователь с такой почтой уже есть")
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="Пользователь с таким именем уже есть")
        user = User(
            login=form.login.data,
            email=form.email.data,
            status=2
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        history = History(
            user_id=user.id,
            story="")

        db_sess.add(history)
        db_sess.commit()
        # print(user)


        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/db.db")
    app.run()


if __name__ == "__main__":
    main()
