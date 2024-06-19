from data import db_session
from data.__all_models import *
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessage
from candinsky_and_gigachat.normal_history import normal_history


async def create_all_story(text):
    '''Создание полной истории. сдесь сбор всего текста в мессендре по ид пользователя'''
    result = ""
    for i in text:
        all_history = await normal_history(i)  # вызываем гигу для приведения в человеческий вид
        result = result + " " + all_history
    # print("all", result)
    return result


if __name__ == '__main__':
    create_all_story(1)