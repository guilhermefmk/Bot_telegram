#pip install pymysql
#pip install glpi_api
#pip install pyTelegramBotAPI


import telebot
import os 
import glpi_api
import pymysql



bot = telebot.TeleBot("1872478293:AAEW602eb2HEjVxSbHd5v_g7gd7YwFElUm0")
#bot = telebot.TeleBot("1868072018:AAGS0iwI1P93eTdhOccNR5XQKYqBsPFcDjE")

URL = 'https://sgc.mundopet.com/apirest.php'
APPTOKEN = 'WTzXyl6NWnwfP5oendJyW5RZUCOyLIIz0BIzMj9t'
#USERTOKEN = 'fFvCjdaLrs3OwMlsCEw9etRAaQ0lRBg9up0w1HAF'
USERNAME = 'suporte_ti'
PASSWORD = '123456'

sessao = {"chat_id": {}}

SALDACOES = False

def ler_texto():
    dir_atual = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir_atual, 'texto.txt')
    lista = []
    file = open(path, "r")
    lista.append(file.read())
    file.close()
    return lista

def ler_pdf(filename):
    dir_atual = os.path.dirname(os.path.abspath(__file__)) + '\\arquivos'
    path = os.path.join(dir_atual, filename)

    file = open(path, 'rb')

    return file 


def handle_messages(messages):
    global SALDACOES
    for message in messages:
        #print(message)
        if message.text in ("bom dia", "boa tarde"):
            #usuario = message.chat.first_name +'.'+message.chat.last_name
            #print("Meu id", usuario)
            sessao['chat_id'][message.chat.id] = {"titulo": "", "conteudo": ""}

            SALDACOES = True
            texto = ler_texto()            
            bot.send_message(message.chat.id, texto) 

        # Tem que ter dado bom dia, boa tarde primeiro
        if SALDACOES == True: 
            if message.text == "1":
                texto = f'''Preparando o pdf da impressora de etiquetas, espere um pouco...'''
                bot.send_message(message.chat.id, texto)
                
                filename = 'Manual para configuração de scanner.pdf'
                file = ler_pdf(filename=filename)
                bot.send_document(message.chat.id, file)
                
                file.close()

                SALDACOES = False 

            elif message.text == "2":
                texto = f'''Huummm, percebi que você está com problema na Impressora correto?\nEntão, clica nesse link abaixo, e segue o passo a passo informado.\nLink: https://sgc.mundopet.com/front/knowbaseitem.form.php?id=8\nAh, caso você realizar o processo informado acima e mesmo assim não conseguiu basta entrar em contato com a  nossa TI que teremos o prazer em lhe atender!\nAté mais! 😊'''
                bot.send_message(message.chat.id, texto)

                SALDACOES = False 

            elif message.text == "3":
                texto = f'''Huummm, percebi que você está com problema no Protheus correto?\nEntão, segue o passo a passo abaixo.\n1º: Fecha o protheus,\n2º:reinicia o start\n3º: acessa o pdv novamente\nAh, caso você realizar o processo informado acima e mesmo assim não conseguiu basta entrar em contato com a  nossa TI que teremos o prazer em lhe atender!\nAté mais! 😊'''
                bot.send_message(message.chat.id, texto)

                SALDACOES = False 

            elif message.text == "4":
                texto = f'''Huummm, percebi que você está com problema no PetMoura correto?\nEntão, clica nesse link abaixo, e segue o passo a passo informado.\nLink: https://sgc.mundopet.com/front/knowbaseitem.form.php?id=11\nAh, caso você realizar o processo informado acima e mesmo assim não conseguiu basta entrar em contato com a  nossa TI que teremos o prazer em lhe atender!\nAté mais! 😊'''
                bot.send_message(message.chat.id, texto)

                SALDACOES = False 

            elif message.text == "5":
                texto = f'''Huummm, percebi que você está com dúvida ao abrir um chamado no SGC correto?\nEntão, segue o passo a passo abaixo.\nLink do Documento: https://sgc.mundopet.com/front/document.send.php?docid=2417\nLink do Video: https://www.youtube.com/watch?v=0azWcq6vYeM\nAh, caso você realizar o processo informado acima e mesmo assim não conseguiu basta entrar em contato com a  nossa TI que teremos o prazer em lhe atender!\nAté mais! 😊'''
                bot.send_message(message.chat.id, texto)

                SALDACOES = False


            elif message.text == "6":
                #usuario = message.chat.first_name +'.'+message.chat.last_name
                                
                #if getUser(usuario.lower()):
                sent = bot.send_message(message.chat.id, 'Digite o nome do seu usuário para abrir o chamado!')
                bot.register_next_step_handler(sent, buscaUsuario)
                    
                SALDACOES = False 
                #else:
                #    sent = bot.send_message(message.chat.id, 'Usuário não existe!')

            elif message.text == "7":
                SALDACOES = False
            
            
def buscaUsuario(message):
    
    if getUser(message.text.lower()):

        sent = bot.send_message(message.chat.id, 'Digite o titulo do chamado!')
        bot.register_next_step_handler(sent, tituloChamado)
    else:
            sent = bot.send_message(message.chat.id, 'Usuário não existe!')


def tituloChamado(message):
    sessao['chat_id'][message.chat.id]['titulo'] = message.text

    sent = bot.send_message(message.chat.id, 'Digite o descricao do chamado!')
    bot.register_next_step_handler(sent, descricaoChamado)
    
    

def descricaoChamado(message):
    sessao['chat_id'][message.chat.id]['conteudo'] = message.text

    titulo = sessao['chat_id'][message.chat.id]['titulo']
    conteudo = sessao['chat_id'][message.chat.id]['conteudo']

    glpi = glpi_api.GLPI(url=URL,
                             apptoken=APPTOKEN,
                             auth=(USERNAME, PASSWORD))

    
    
    glpi.add("ticket", {"name": titulo, "content":conteudo, "itilcategories_id": "260"})



    del sessao['chat_id'][message.chat.id] 
    bot.send_message(message.chat.id, 'Chamado salvo com sucesso!')

    print(sessao)


def conexao():
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='q1w2e3r4',
                             database='biblioteca')    
    return connection


def getUser(usuario):
    usuarioExiste = False 
    con = conexao()
    cursor = con.cursor()

    sql = f'''SELECT NAME FROM glpi_users WHERE IS_ACTIVE = 1 AND NAME = '{usuario}' '''
    print(sql)
    cursor.execute(sql)


    for i in cursor.fetchall():
        if len(i[0]) > 0:
            usuarioExiste = True 
        else:
            usuarioExiste = False 

    cursor.close()
    con.close()

    return usuarioExiste

bot.set_update_listener(handle_messages)
bot.polling()


bot.polling()