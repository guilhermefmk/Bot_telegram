import telebot

# Chave fornecida pelo telegram
chave_api = '5341319826:AAHpKduSpGQeO_T2fLpbGmb7hg5lax97Fns'

# Conecta com o bot
bot = telebot.TeleBot(chave_api)



@bot.message_handler(commands=['abrirchamado'])
def abrir(x):
    text = """
        Olá, abriu chamado!
    """
    bot.reply_to(x, text)

@bot.message_handler(commands=['acompanharchamado'])
def acompanhar(x):
    text = """
        Olá, acompanhou chamado!
    """
    bot.reply_to(x, text)








def verifica(x):
    return True
# Define quando a função vai ser chamada
# @bot.message_handler(commands=["ola"])
@bot.message_handler(func=verifica)
def responder(x):
    text = """
        Olá, selecione a opção desejada:
        /abrirchamado
        /acompanharchamado
    """
    bot.reply_to(x, text)


bot.polling()
