from flask import Flask, render_template, redirect, request, send_file, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os

from data import db_session
from data.login import LoginForm
from data.__all_models import *
from data.register import RegisterForm
from data.utils import *
# from flask_restful import abort
from candinsky_and_gigachat.candy import generate_image
from candy_new import generate_image_new

from candinsky_and_gigachat import voice

'''!!!!Очень важный факт, комментарии тоже могут работать как код, так что лучше УДАЛЯТЬ!!!!!'''

from candinsky_and_gigachat.giga import *
from candinsky_and_gigachat.generate_prompt_for_kandy import create_prompt
from candinsky_and_gigachat.create_all_stoty import *
import asyncio

chat = init_giga()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'JGKzpcce9ajD72k'

db_session.global_init("db/db.db")

login_manager = LoginManager()
login_manager.init_app(app)

CHAT_DEBUG = True
CHAT_DELAY = 1
VOICE_DEBUG = True
VOICE_DELAY = 1
IMAGE_DEBUG = True
IMAGE_DELAY = 1


@app.route("/get-all-story/<story_id>", methods=['POST', 'GET'])
async def all_story(story_id):
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user_id = db_sess.query(Story).filter(Story.id == story_id).first().user_id
        title = db_sess.query(Story).filter(Story.id == story_id).first().title
        user_name = db_sess.query(User).filter(User.id == user_id).first().login  # получаем ник пользователя
        if_full_story = db_sess.query(Full_Stories).filter(Full_Stories.story_id == story_id).first()
        if if_full_story is not None:
            return jsonify({'url': f'/get-all-story/{story_id}'})

        else:
            full_story_text = create_all_story(story_id)
            full_story = Full_Stories(
                story_id=story_id,
                user_id=user_id,
                username=user_name,
                title=title,
                text=full_story_text
            )
            db_sess.add(full_story)
            db_sess.commit()
            return jsonify({'url': f'/get-all-story/{story_id}'})

    if request.method == 'GET':
        db_sess = db_session.create_session()
        text = db_sess.query(Full_Stories).filter(Full_Stories.story_id == story_id).first().text
        title = db_sess.query(Full_Stories).filter(Full_Stories.story_id == story_id).first().title
        username = db_sess.query(Full_Stories).filter(Full_Stories.story_id == story_id).first().username
        return render_template('full_story.html', title=title, text=text, username=username)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.email.data)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/my_home")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/test')
def test():
    return render_template('index.html')


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect('my_home')
    return render_template("about.html")


@app.route("/ntale", methods=['POST', 'GET'])
def new_tale():
    ''' У нас есть БД там таблица, user  и history, у History в столбике story сохраняется история (весь диалог) тут мы, собственно, заполняем эту таблицу'''
    db_sess = db_session.create_session()
    history = Story(
        user_id=current_user.id,
        title="Новая сказка"
    )
    messages = [
        SystemMessage(
            # content=f'Ты - писатель, который составляет сказки вместе с ребенком. Ты и '
            #         f'пользователь вместе пишите сказку. Ты должен дополнять сказку ТОЛЬКО'
            #         f'на 2 '
            #         f'предложения. Повествование последовательное. Добавляй как '
            #         f'можно больше деталей внешности и описания окружающей среды. Если '
            #         f'предложения. Повествование последовательное. Добавляй больше деталей внешности и описания окружающей среды. Если '
            #         f'пользователь затрудняется с описанием, то придумай сам. Если '
            #         f'пользователь сам описывает историю, то ты просто продолжаешь. История '
            #         f'должна быть логически правильно построенной. Сюжет понятный.'
            #         f'Ты дополняешь историю ТОЛЬКО НА 2 ПРЕДЛОЖЕНИЯ.'
            #         f'должна быть логически правильно построенна. Сюжет понятный.'
            #         f'Ты дополняешь историю РОВНО НА 2 ПРЕДЛОЖЕНИЯ.'
            content=f'Ты -добрый писатель, который составляет сказки вместе с ребенком. Ты должен дополнять сказку польователя на'
                    f'одно единственное предложение '

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
        tales.append((i.id, i.title))
    return render_template("tales.html", tales=tales)


@app.route('/get-image/<img_id>')
async def get_image(img_id):
    if IMAGE_DEBUG:
        await asyncio.sleep(IMAGE_DELAY)
        return send_file(
            "static/img/image1.png",
            mimetype='image/jpeg'
        )

    for filename in os.listdir('static/mes_images'):
        print(filename)
        if filename.endswith(img_id + ".png"):
            return send_file(
                f"static/mes_images/{filename}",
                mimetype='image/jpeg'
            )

    db_sess = db_session.create_session()
    user_id, story_id = user_story_from_message(img_id)
    path = f'static/mes_images/{current_user.id}_{story_id}_{img_id}.png'
    if os.path.exists(path):
        return send_file(
            path,
            mimetype='image/jpeg'
        )
    msg = db_sess.query(Message).filter(Message.story_id == story_id)
    text = "".join([eval(i.text).content for i in msg[1:]])
    if CHAT_DEBUG:
        await asyncio.sleep(CHAT_DELAY)
        prompt = "Нарисуй лопату"
    else:
        prompt = create_prompt(chat, text)
    if not os.path.exists(path):
        await generate_image(prompt, path)
    return send_file(
        path,
        mimetype='image/jpeg'
    )


@app.route("/tale/<story_id>", methods=['POST', 'GET'])
async def last_tale(story_id):
    if story_id is None:
        return redirect("/tales")
    '''тут идет создание самого диалога, добавление его в бд'''
    db_sess = db_session.create_session()
    messages, msg_id = get_all_story(story_id)
    if request.method == 'GET':
        text = []
        for i, j in zip(messages[1:], msg_id[1:]):
            if VOICE_DEBUG:
                await asyncio.sleep(VOICE_DELAY)
                voice_path = "voice/11_2.mp3"
            else:
                voice_path = str(
                    voice.speach(i.content, "AIMessage" in str(type(i)), f'{story_id}_{messages.index(i)}'))
            text.append((i.content,
                         "AIMessage" in str(type(i)),
                         voice_path,
                         j))
        return render_template("test.html", story_content=text)

    elif request.method == 'POST':
        user_input = request.form['story']
        print(user_input)
        if user_input.strip() == "":
            return redirect(f'/tale/{story_id}')
        # это системный промт, если порусски, тут мы озадачиваем гигy
        msg = Message(
            story_id=story_id,
            text=repr(HumanMessage(content=user_input))
        )
        db_sess.add(msg)
        db_sess.commit()
        messages, msg_id = get_all_story(story_id)

        print("post", messages)
        if CHAT_DEBUG:
            await asyncio.sleep(CHAT_DELAY)
            res = "Мне нравятся истории о животных, которые помогают людям. Это показывает, что даже самые маленькие и слабые создания могут сделать большой вклад в жизнь других."
        else:
            res = chat(messages).content

        db_sess = db_session.create_session()
        history = db_sess.query(Story).filter(Story.id == story_id).first()
        if len(messages) == 2:
            history.title = user_input
            db_sess.commit()
        # Ответ модели
        # ЭТО НАШ ОТВЕТ
        msg = Message(
            story_id=story_id,
            text=repr(AIMessage(content=res)),
        )
        db_sess.add(msg)
        db_sess.commit()
        return redirect(f'/tale/{story_id}')


@app.route('/')
def home():
    return render_template('about.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/my_home')
def my_home():
    return render_template('my_home.html')


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
    app.run()


if __name__ == "__main__":
    main()
