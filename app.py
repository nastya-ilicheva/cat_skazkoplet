from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from sqlalchemy.sql.expression import func
from data import db_session
from data.login import LoginForm
from data.__all_models import *
from data.register import RegisterForm
# from data.new_game import NewGameForm
# from flask_restful import abort

from all import voice
import webbrowser

import json
import datetime
import random

'''!!!!Очень важный факт, комментарии тоже могут работать как код, так что лучше УДАЛЯТЬ!!!!!'''

from candinsky_and_gigachat.giga import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JGKzpcce9ajD72k'

login_manager = LoginManager()
login_manager.init_app(app)

alphabet = [list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"[i:i + 3]) for i in range(0, 33, 3)]


# messages = [
#     SystemMessage(
#         content="Ты помогаешь детям писать сказки подсказывая им и художественно дополняя их предложения."
#     )
# ]


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
    ''' У нас есть БД там таблица, user  и history, у History в столбике story сохраняется история (весь диалог) тут мы, собственно, заполняем эту таблицу'''
    db_sess = db_session.create_session()
    history = History(
        user_id=current_user.id,  #
        giga_id=get_token(auth).json()['access_token'],
        story=""
    )
    messages = [
        SystemMessage(
            content="Ты помогаешь детям писать сказки подсказывая им и художественно дополняя их предложения."
        )
    ]
    history.story = str(messages)
    db_sess.add(history)
    db_sess.commit()
    return redirect(f'/tale/{history.id}')


@app.route("/tales")
def my_tales():
    db_sess = db_session.create_session()
    library = db_sess.query(History).filter(History.user_id == current_user.id)
    tales = []
    for i in library:
        try:
            msg = eval(i.story)[1].content
        except Exception:
            msg = 'Новая сказка'
        tales.append((i.id, msg))
    return render_template("tales.html", tales=tales)


@app.route("/tale/<story_id>", methods=['POST', 'GET'])
def last_tale(story_id):
    c = 0
    '''тут идет создание самого диалога, добавление его в бд'''
    db_sess = db_session.create_session()
    print(story_id)
    if story_id is None:
        story_id = db_sess.query11(History).filter(History.user_id == current_user.id).order_by(
            History.id.desc()).first().id
        print(story_id)
    history = db_sess.query(History).filter(History.id == story_id).first()
    messages = eval(history.story)
    text = []
    for i in messages[1:]:
        text.append(i.content)
    if request.method == 'GET':
        return render_template("test.html", story_content=text)
    elif request.method == 'POST':
        print(request.form['story'])
        user_input = request.form['story']

        # это системный промт, если порусски, тут мы озадачиваем гигy

        print(history.story)

        # messages.append(HumanMessage(content=f'Ты - писатель, который составляет сказки вместе с ребенком. Ты и '
        #                                      f'пользователь вместе пишите сказку. Ты должен дополнять сказку ТОЛЬКО'
        #                                      f'на 2 '
        #                                      f'предложения. Повествование последовательное. Добавляй как '
        #                                      f'можно больше деталей внешности и описания окружающей среды. Если '
        #                                      f'пользователь затрудняется с описанием, то придумай сам. Если '
        #                                      f'пользователь сам описывает историю, то ты просто продолжаешь. История '
        #                                      f'должна быть логически правильно построенной. Сюжет понятный. Далее, в '
        #                                      f'кавычках, будет приведено начало сказки, если они пусты, то значит это '
        #                                      f'сказка новая, если нет, то продолжай эту."{history.story + user_input}"'
        #                                      f'Ты дополняешь историю ТОЛЬКО НА 2 ПРЕДЛОЖЕНИЯ. При выведении ответа не '
        #                                      f'пиши двойные скобки'))
        messages.append(HumanMessage(content=user_input))
        res = chat(messages)
        print(res.content)
        speach_rec = voice.speach(res.content)
        webbrowser.open(speach_rec)
        messages.append(AIMessage(content=res.content))
        # Ответ модели
        # ЭТО НАШ ОТВЕТ
        print(messages)

        history.story = str(messages)
        c += 1
        db_sess.commit()

        return render_template("test.html", story_content=text)
        # return render_template("test.html", story_content=text, im='static/img/image1.png')


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

        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/db.db")
    app.run()


if __name__ == "__main__":
    main()