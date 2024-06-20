from candinsky_and_gigachat.giga import *


async def normal_history(text):
    messages = [SystemMessage(content=('''коротко и литературно 
    перескажи этот диалог в виде связного текста; 
    тебе категорически запрещено здороваться и представляться.
     Тебе нельзя добавлять в текст что-либо новое.
    Не рассказывай и не добавляй в текст новые фрагменты или факты'''))]

    messages.append(HumanMessage(content=text))
    chat = init_giga()
    res = chat(messages)
    print(res.content)
    return res.content
