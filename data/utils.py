from data import db_session
from data.__all_models import *
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessage


def user_story_from_message(msg_id):
    try:
        db_sess = db_session.create_session()
        story_id = db_sess.query(Message).filter(Message.id == msg_id).first().story_id
        user_id = db_sess.query(Story).filter(Story.id == story_id).first().user_id
        return user_id, story_id
    except Exception as e:
        print(e)


def get_all_story(story_id):
    text = []
    msg_id = []
    db_sess = db_session.create_session()
    for i in db_sess.query(Message).filter(Message.story_id == story_id):
        text.append(eval(i.text))
        msg_id.append(i.id)
    return text, msg_id


if __name__ == '__main__':
    db_session.global_init("../db/db.db")
    a, b = get_all_story(4)
    print(a)
    # for i, j in zip(a, b):
    #     print(i, j)
