from candinsky_and_gigachat.giga import *


async def normal_history(text):
    '''Сдесь гига приводит текст в человеческий вид'''

    messages = [SystemMessage(content=('''Анализируйте текстовый отрывок и 
      создайте текст, 
      к котором выделено основное  ключевые события и детали и  и описание персонажей,  
      ; вам категорически запрещено здороваться и прдедтляться .'''))]

   # messages = [SystemMessage(
        # content="Ваша задача - соеденить отрывки текста и сделать его связным в цельную скузку, которую они рассказали"
        #         "у тебя должна получиться истрия, а не диалог"
        #
        #         # "и соединять их в одну цельную историю."
        #         "При этом, вы должны учитывать контекст каждого отрывка и стремиться к тому, "
        #         "чтобы переходы между ними были плавными и логичными. Ваша цель соединить поочередный рассказ друзей в одну историю "
        #         ", не добавляя при этом ничего нового"
        #         "Помните, что вам категорически запрещено здороваться или добавлять что-либо новое в тексте истории."
        #         "ваша задача - соединить отрывки в историю,"
        #         " которая начинается сразу без вступительных приветствий.")]

    messages.append(HumanMessage(content=text))
    chat = init_giga()
    res = chat(messages)
    print(res.content)
    return res.content
