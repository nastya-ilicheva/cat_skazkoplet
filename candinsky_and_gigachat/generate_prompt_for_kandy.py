from candinsky_and_gigachat.giga import *


def create_prompt(chat, msg):
    # messages = [SystemMessage(content="Ты упрощаешь введенный текст. Убери все ненужное, но оставь описания.")] + msg
    messages = [SystemMessage(content="Ты оставляешь короткие описания персонажей из текста. Милая "
                                      "картинка, для малышей. стиль мультяшный. для сказки. baby")]
    messages.append(HumanMessage(content=msg))
    print("prompt",messages)
    res = chat(messages)
    print("gen_prompt_result", res.content)
    return res.content
