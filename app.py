from flask import Flask, render_template, redirect, request, send_file, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from data.login import LoginForm
from data.register import RegisterForm
from data.utils import *
from candinsky_and_gigachat.candy import generate_image
from candinsky_and_gigachat import voice
from candinsky_and_gigachat.giga import *
from candinsky_and_gigachat.generate_prompt_for_kandy import create_prompt
from candinsky_and_gigachat.create_all_stoty import *
import asyncio
from random import choice

'''!!!!Очень важный факт, комментарии тоже могут работать как код, так что лучше УДАЛЯТЬ!!!!!'''

chat = init_giga()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'JGKzpcce9ajD72k'

db_session.global_init("db/db.db")

login_manager = LoginManager()
login_manager.init_app(app)

CHAT_DEBUG = 0
VOICE_DEBUG = 0
IMAGE_DEBUG = 0

IMAGE_DELAY = 1
CHAT_DELAY = 1
VOICE_DELAY = 1


def story_picture(story_id):
    pictures = []
    try:
        for root, dirs, files in os.walk('static/mes_images'):
            for file in files:
                if f'_{story_id}_' in file:
                    pictures.append(os.path.join(root, file).split('\\')[1])
        return choice(pictures)
    except Exception:
        return 'end_picture.jpg'


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
            db_sess = db_session.create_session()
            msg__ = db_sess.query(Message).filter(Message.story_id == story_id)
            text__ = [eval(i.text).content for i in msg__[1:]]
            full_story_text = await create_all_story(text__)
            full_story = Full_Stories(
                story_id=story_id,
                user_id=user_id,
                username=user_name,
                title=title,
                text=full_story_text,
                picture=story_picture(story_id)
            )
            db_sess.add(full_story)
            db_sess.commit()
            return jsonify({'url': f'/get-all-story/{story_id}'})

    if request.method == 'GET':
        db_sess = db_session.create_session()
        text = db_sess.query(Full_Stories).filter(Full_Stories.story_id == story_id).first().text
        title = db_sess.query(Full_Stories).filter(Full_Stories.story_id == story_id).first().title
        username = db_sess.query(Full_Stories).filter(Full_Stories.story_id == story_id).first().username
        picture = db_sess.query(Full_Stories).filter(Full_Stories.story_id == story_id).first().picture
        return render_template('full_story.html', title=title, text=text, username=username,
                               picture=picture)


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
    db_sess = db_session.create_session()
    history = Story(
        user_id=current_user.id,
        title="Новая сказка"
    )

    messages = [
        SystemMessage(
            content=f'Ты -добрый находчивый кот писатель по имени Сказкоплет.'
                    f'Ты помогаешь ребенку писать увлекательные сказки с конкретным понятным захватывающим сюжетом, '
                    f'ты по 1 сообщению с пользователем по кусочкам пишешь большую увлекательную сказку.'
                    f'после приветствия сразу же приступайте к написанию сказки'
                    f'предлогая пользователю выбрать главного героя и его имя, место, где развивается сюжет, стиль сказки и другие детали'
                     f'В зависимости от ввода пользователя, ты развиваешь сюжет истори,'
                    f' добавляя фрагменты длиной в 40 слов. Если пользователь не предоставляет ввод или просит продолжить,'
                    f'ты самостоятельно придумываешь последующие интереные события, которые подрузумевают продолжение,'
                    f'ты самостоятельно придумываешь последующие интереные события, которые соответствуют требованиям предыдущего фрагмента,'
                    f'длина одного ответа должна быть меньше 3 предложений.'
                    f'твой текст всегда должен иметь возможное продолжение событий в нем, а в историях  больше конкретных действий персонажей,'
                    f' так как ты даешь пользователю возможность дополнять сюжет'

                    f'Если пользователь пишет имена исторических политических и культурных деятелей,'
                    f' то придумай про них чудесную сказку, а не расказывай биографию.'
                    f'ты предлогаешь пользователю выбор между вариантами развития событий'
                    f' Ты должен продолжать сюжет сказки польователя  на 20-40 слов.'

                    f'ты даешь пользователю выбор между возможными  продолжениями сказки'
                    f'Ты  должен продолжать  сказку собеседника на'
                    f' 40 слов и задать пользователю вопрос, о том, какой вариан развития событий из предложенных тобой он выберет.'
                    f'Каждое твое сообщение заканчивается вопросом о дальнейших событиях сказки, на который должен ответить пользователь.'
                    f'Если пользователь начинает общение со слов "про...." то начини сказку сам, написав первые 2 предложения и многоточие со знаком вопроса,'
                    f' и спроси у пользователя вопросы для более интресного продолжения'
                    f' Никогда не спорь с пользователем и не подтверждай его речь и не переспрашивай его.'
                    f'сказки бесконечные, поэтому всегда имеют открытую концовку и могут постоянно продолжаться')

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


@app.route("/delete/tale/<del_id>", methods=['POST'])
def delete_history(del_id):
    if request.method == 'POST':
        db_sess = db_session.create_session()
        story = db_sess.query(Story).filter(Story.id == del_id).first()
        if story:
            story.enable = 0
            db_sess.commit()
            return f"History {del_id} disenabled successfully"
        else:
            print(f'сказка {del_id} не найдена')
            return "History not found"


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
        if i.enable == 1:
            db_sess = db_session.create_session()
            if_full_story = db_sess.query(Full_Stories).filter(Full_Stories.story_id == i.id).first()
            tales.append((i.id, i.title, if_full_story))
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
        if filename.endswith(img_id + ".png"):
            return send_file(
                f"static/mes_images/{filename}",
                mimetype='image/jpeg'
            )

    user_id, story_id = user_story_from_message(img_id)
    path = f'static/mes_images/{current_user.id}_{story_id}_{img_id}.png'
    if os.path.exists(path):
        return send_file(
            path,
            mimetype='image/jpeg'
        )
    db_sess = db_session.create_session()
    msg = db_sess.query(Message).filter(Message.story_id == story_id)
    db_sess.close()
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
    if db_sess.query(Story).filter(Story.id == story_id).first().enable == 0:
        return redirect("/tales")
    try:
        if db_sess.query(Story).filter(Story.id == story_id).first().user_id != current_user.id:
            pass
    except Exception:
        return redirect("/")
    messages, msg_id = get_all_story(story_id)
    if request.method == 'GET':
        text = []
        for i, j in zip(messages[1:], msg_id[1:]):
            if VOICE_DEBUG:
                await asyncio.sleep(VOICE_DELAY)
                # print("voice_DEBUG!!!!!!!!!!!!!!!!")
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
        print('ai mes', msg.text)
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
    try:
        if current_user.id:
            pass
    except Exception:
        return redirect("/")
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


@app.route('/publications', methods=['GET', 'POST'])
def publications():
    if request.method == 'GET':
        db_sess = db_session.create_session()
        public = db_sess.query(Full_Stories).all()
        publ_data = []
        for i in public:
            publ_data.append((i.id, i.title, i.username))  # ид, название, автор
        return render_template('publications.html', info=publ_data)

    elif request.method == 'POST':
        return jsonify({'url': '/publications'})


@app.route('/publication/<publ_id>', methods=['GET', 'POST'])
def publication_view(publ_id):
    if request.method == 'GET':
        db_sess = db_session.create_session()
        autor = db_sess.query(Full_Stories).filter(Full_Stories.id == publ_id).first().username
        text = db_sess.query(Full_Stories).filter(Full_Stories.id == publ_id).first().text
        title = db_sess.query(Full_Stories).filter(Full_Stories.id == publ_id).first().title
        picture = db_sess.query(Full_Stories).filter(Full_Stories.id == publ_id).first().picture
        return render_template('publicatioN.html', autor=autor, text=text, title=title, picture=picture)


def main():
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT", default=5000))


if __name__ == "__main__":
    main()
