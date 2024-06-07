from candinsky_and_gigachat.giga import *


def create_prompt(chat, msg):
    # messages = [SystemMessage(content="Ты упрощаешь введенный текст. Убери все ненужное, но оставь описания.")] + msg
    messages = [SystemMessage(content="Ты - редактор. Ты упрощаешь и сокращаешь текст последнего предложения отрывка сказки. страшное содержание делаешь менее страшным. "
                                      " Никогда не придумывай нового. Если ты встречаешь иена исторических персонажей, оставляй описание персонажа и дай ему новое имя ")]
    messages.append(HumanMessage(content=msg))
    print("prompt", messages)
    res = chat(messages)
    print("gen_prompt_result", res.content)
    return res.content
