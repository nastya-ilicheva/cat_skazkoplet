from data import db_session
from data.__all_models import *
from candinsky_and_gigachat.normal_history import normal_history


def create_all_story(id):
    '''Создание полной истории. сдесь сбор всего текста в мессендре по ид СООБЩЕНИЯ'''
    db_session.global_init("../db/db.db")
    db_sess = db_session.create_session()
    story_id = db_sess.query(Message).filter(Message.id == id).first().story_id
    print(story_id)
    msg = db_sess.query(Message).filter(Message.story_id == story_id)
    text = "".join([eval(i.text).content for i in msg[1:]])
    print(text)
    all_history = normal_history(text) # вызываем гигу для приведения в человеческий вид
    return all_history

