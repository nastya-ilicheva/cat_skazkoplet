from candinsky_and_gigachat.giga import *

def normal_history(text):
    '''Сдесь гига приводит текст в человеческий вид'''
    messages = [SystemMessage(content="Ты олитературиваешь текст, не убирай смысл и длину сообщений."
                                      "Никогда не придумывай текст. Ты только редактируешь имеющийся")]
    messages.append(HumanMessage(content=text))
    res = chat(messages)
    print(res.content)
    return res.content
