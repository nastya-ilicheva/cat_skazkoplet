from telegram.ext import CallbackContext


class Command:

    async def translate_to_russian(update, context: CallbackContext):
        text = update.message.text[12:]
        translated_text = ""

        for char in text:
            if char.isalpha():
                if char.lower() in "qwertyuiop[]asdfghjkl;'zxcvbnm,.`":
                    translated_char = chr(ord(char) - 32) if char.isupper() else char
                else:
                    translated_char = chr(ord(char) + 32) if char.isupper() else char
            else:
                translated_char = char

            translated_text += translated_char

        await update.message.reply_text(translated_text)

    async def translate_to_english(update, context: CallbackContext):
        text = update.message.text[12:]
        translated_text = ""

        for char in text:
            if char.isalpha():
                if char.lower() in "йцукенгшщзхъфывапролджэячсмитьбю":
                    translated_char = chr(ord(char) - 32) if char.isupper() else char
                else:
                    translated_char = chr(ord(char) + 32) if char.isupper() else char
            else:
                translated_char = char

            translated_text += translated_char

        await update.message.reply_text(translated_text)

    async def start(update, context: CallbackContext):
        user = update.effective_user
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Привет {user.first_name}! Смотрите, что я могу!\n"
                                      "/start - начать\n"
                                      "/to_Russian [текст] - перевести с английского на русский\n"
                                      "/to_English [текст] - перевести с русского на английский\n"
                                      "/education - образование")

    async def education(update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="я умная и опытная, мамой клянусь")
