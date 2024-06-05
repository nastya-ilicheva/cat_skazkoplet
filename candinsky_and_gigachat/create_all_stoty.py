from data import db_session
from data.__all_models import *
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessage
from candinsky_and_gigachat.normal_history import normal_history


def create_all_story(story_id):
    '''Создание полной истории. сдесь сбор всего текста в мессендре по ид пользователя'''
    db_session.global_init("../db/db.db")
    db_sess = db_session.create_session()
    msg = db_sess.query(Message).filter(Message.story_id == story_id)
    text = "".join([eval(i.text).content for i in msg[1:]])
    # all_history = normal_history(text) # вызываем гигу для приведения в человеческий вид
    # return all_history
    return text  # пока что заглушка


if __name__ == '__main__':
    create_all_story(1)