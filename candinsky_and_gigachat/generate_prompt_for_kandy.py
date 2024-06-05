from candinsky_and_gigachat.giga import *


def create_prompt(chat, msg):
    # messages = [SystemMessage(content="Ты упрощаешь введенный текст. Убери все ненужное, но оставь описания.")] + msg
    messages = [SystemMessage(content="Ты - редактор. Ты упрощаешь и сокращаешь текст. Максимум 200 символов. "
                                      " Никогда не придумывай нового.")]
    messages.append(HumanMessage(content=msg))
    print("prompt", messages)
    res = chat(messages)
    print("gen_prompt_result", res.content)
    return res.content
