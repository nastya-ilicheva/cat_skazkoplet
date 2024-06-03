from candinsky_and_gigachat.giga import *

def create_prompt(msg):
    # messages = [SystemMessage(content="Ты упрощаешь введенный текст. Убери все ненужное, но оставь описания.")] + msg
    messages = [SystemMessage(content="Ты упрощаешь введенный текст. Убери все ненужное, но оставь описания. Милая "
                                      "картинка, для малышей. стиль мультяшный. для сказки. baby")]
    messages.append(HumanMessage(content=msg))
    print(messages)
    res = chat(messages)
    print(res.content)
    return res.content
