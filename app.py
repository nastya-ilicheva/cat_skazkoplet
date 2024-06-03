from flask import Flask, render_template, redirect, request, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
import candinsky_and_gigachat.create_all_stoty

from data import db_session
from data.login import LoginForm
from data.__all_models import *
from data.register import RegisterForm
# from data.new_game import NewGameForm
# from flask_restful import abort
from candinsky_and_gigachat.candy import generate_image

from static.voice import voice

'''!!!!Очень важный факт, комментарии тоже могут работать как код, так что лучше УДАЛЯТЬ!!!!!'''

from candinsky_and_gigachat.giga import *
from candinsky_and_gigachat.generate_prompt_for_kandy import create_prompt
from candinsky_and_gigachat.create_all_stoty import *

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
    return render_template("about.html")


@app.route("/ntale", methods=['POST', 'GET'])
def new_tale():
    ''' У нас есть БД там таблица, user  и history, у History в столбике story сохраняется история (весь диалог) тут мы, собственно, заполняем эту таблицу'''
    db_sess = db_session.create_session()
    history = Story(
        user_id=current_user.id,  #
        title="Новая сказка"
    )
    messages = [
        SystemMessage(
            content=f'Ты - писатель, который составляет сказки вместе с ребенком. Ты и '
                    f'пользователь вместе пишите сказку. Ты должен дополнять сказку ТОЛЬКО'
                    f'на 2 '
                    f'предложения. Повествование последовательное. Добавляй как '
                    f'можно больше деталей внешности и описания окружающей среды. Если '
                    f'пользователь затрудняется с описанием, то придумай сам. Если '
                    f'пользователь сам описывает историю, то ты просто продолжаешь. История '
                    f'должна быть логически правильно построенной. Сюжет понятный.'
                    f'Ты дополняешь историю ТОЛЬКО НА 2 ПРЕДЛОЖЕНИЯ.'
        )
    ]
    db_sess.add(history)
    db_sess.commit()
    print(repr(messages[0]))
    msg = Message(
        story_id=history.id,
        text=repr(messages[0])
    )
    db_sess.add(msg)
    db_sess.commit()

    return redirect(f'/tale/{history.id}')


@app.route("/tales", methods=['POST', 'GET'])
def my_tales():
    db_sess = db_session.create_session()
    if request.method == 'POST':
        data = request.get_json()
        id = data['id']
        new_text = data['newText']
        history = db_sess.query(Story).filter(Story.id == id).first()
        history.title = new_text
        db_sess.commit()
    library = db_sess.query(Story).filter(Story.user_id == current_user.id)
    tales = []
    for i in library:
        # try:
        #     msg = eval(i.story)[1].content
        # except Exception:
        #     msg = 'Новая сказка'
        tales.append((i.id, i.title))
    return render_template("tales.html", tales=tales)



@app.route('/get-image/<img_id>')
async def get_image(img_id):
    db_sess = db_session.create_session()
    story_id = db_sess.query(Message).filter(Message.id == img_id).first().story_id
    print(story_id)
    msg = db_sess.query(Message).filter(Message.story_id == story_id)
    print("rtgrshkejthrth", msg)
    text = "".join([eval(i.text).content for i in msg[1:]])
    print(text)
    prompt = create_prompt(text)
    path = f'static/mes_images/{current_user.id}_{story_id}_{img_id}.png'
    if not os.path.exists(path):
        await generate_image(prompt, path)
    return send_file(
        path,
        mimetype='image/jpeg'
    )


@app.route("/get-all-story/<story_id>", methods=['POST', 'GET'])
async def all_story(story_id):
    if request.method == 'POST':
        full_story = await create_all_story(story_id)
        return full_story

@app.route("/tale/<story_id>", methods=['POST', 'GET'])
def last_tale(story_id):
    '''тут идет создание самого диалога, добавление его в бд'''
    db_sess = db_session.create_session()
    if story_id is None:
        return redirect("/tales")
    history = db_sess.query(Story).filter(Story.id == story_id).first()
    messages = []
    msg = db_sess.query(Message).filter(Message.story_id == history.id)
    msg_id = []
    for i in msg:
        messages.append(eval(i.text))
        msg_id.append(i.id)
    print(messages)
    # создание всей истории по запросу, пока тру просто
    # if True:
    #     all_story = create_all_story(Message)
    if request.method == 'GET':
        text = [(i.content,
                 "AIMessage" in str(type(i)),
                 str(voice.speach(i.content, "AIMessage" in str(type(i)), f'{history.id}_{messages.index(i)}')),
                 j) for i, j in zip(messages[1:], msg_id)]
        a = [i[2] for i in text]
        print(a)
        return render_template("test.html", story_content=text, story_id=story_id)
    elif request.method == 'POST':
        print(request.form['story'])
        user_input = request.form['story']

        # это системный промт, если порусски, тут мы озадачиваем гигy

        messages.append(HumanMessage(content=user_input))
        if len(messages) == 2:
            history.title = user_input
        msg = Message(
            story_id=history.id,
            text=repr(messages[-1])
        )
        db_sess.add(msg)
        db_sess.commit()
        res = chat(messages)
        print(res.content)
        # speach_rec = voice.speach(res.content, f'{history.id}_{messages.index(i)}')

        messages.append(AIMessage(content=res.content))
        # Ответ модели
        # ЭТО НАШ ОТВЕТ
        print(messages)
        msg = Message(
            story_id=history.id,
            text=repr(messages[-1]),
        )
        db_sess.add(msg)
        db_sess.commit()

        msg.image_path = f'static/mes_images/{current_user.id}_{history.id}_{msg.id}.png'
        # generate_image(messages, msg.image_path)
        db_sess.add(msg)
        db_sess.commit()
        msg_id.append(msg.id)

        text = [(i.content,
                 "AIMessage" in str(type(i)),
                 str(voice.speach(i.content, "AIMessage" in str(type(i)), f'{history.id}_{j}')),
                 j) for i, j in zip(messages[1:], msg_id)]
        print(text)
        return render_template("test.html", story_content=text, story_id=story_id)
        # return render_template("test.html", story_content=text, im='static/img/image1.png')


@app.route('/')
def home():
    return render_template('about.html')


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
