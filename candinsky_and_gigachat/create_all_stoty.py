from data import db_session
from data.__all_models import *
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessage
from candinsky_and_gigachat.normal_history import normal_history


async def create_all_story(text):
    '''Создание полной истории. сдесь сбор всего текста в мессендре по ид пользователя'''
    # db_session.global_init("../db/db.db")
    # db_sess = db_session.create_session()
    # msg = db_sess.query(Message).filter(Message.story_id == story_id)
    # text = [eval(i.text).content for i in msg[1:]]

    result = ""
    for i in text:
        all_history = await normal_history(i)  # вызываем гигу для приведения в человеческий вид
        result = result + " " + all_history
    # return all_history
    print("all", result)
    return result


if __name__ == '__main__':
    create_all_story(1)