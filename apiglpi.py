import numbers
from webbrowser import get
import telebot
import os 
import glpi_api
import pymysql
import telegram
import datetime

URL = 'http://172.16.112.164/glpi/apirest.php/'
APPTOKEN = 'XvRM61PGyo70FTwMEmJxDilK8lXmacjtoyciiuNj'                                           #TOKEN GERADO PARA TODO O SISTEMA
USERTOKEN = 'CZoqXFVys4u0IKRssKIbDsQRwwMFIxwTY6ZqvE2L'                                          #API TOKEN DO USUÁRIO
BOTTOKEN = '5341319826:AAHpKduSpGQeO_T2fLpbGmb7hg5lax97Fns'
bot = telebot.TeleBot(BOTTOKEN) # creating a instance
sessao = {"chat_id": {}}



# try:
#     with glpi_api.connect(URL, APPTOKEN, USERTOKEN) as glpi:
#         # #CRIAR CHAMADO
#         # glpi.add("ticket", {"name": 'teste', "content":'Fui aberto via API', "itilcategories_id": "1"})
#         # #DELETAR CHAMADO
#         # glpi.delete("ticket", {"id":'20'})
#         # #INSERIR INTERAÇÃO
#         # glpi.add("ticketfollowup",{"items_id":'25',"itemstype":"ticket","content":'nova interação'})
#         # ALTERAR STATUS TICKET
#         # glpi.update('ticket',{"id":'22','status':'5'})
#         pass
# except glpi_api.GLPIError as err:
#     print(str(err))

#CONECTA BANCO
def conexao():
    connection = pymysql.connect(host='172.16.112.164',
                             user='root',
                             password='vetorial',
                             database='verdanatech_glpi_lab')    
    return connection

def conglpi():
    return glpi_api.connect(URL, APPTOKEN, USERTOKEN)

#RETORNA SE USUÀRIO TELEGRAM ESTA REGISTRADO NO BANCO
def getUser(usuario):
    usuarioExiste = False 
    con = conexao()
    cursor = con.cursor()

    sql = f'''SELECT username FROM glpi_plugin_telegrambot_users WHERE username = '{usuario}' '''
    # print(sql)
    cursor.execute(sql)


    for i in cursor.fetchall():
        if len(i[0]) > 0:
            usuarioExiste = True 
        else:
            usuarioExiste = False 

    cursor.close()
    con.close()

    return usuarioExiste

#RETORNA O ID DO USUÁRIO NO GLPI BASEADO NO USUÁRIO DO TELEGRAM
def getglpiid(usuario):
    
    con = conexao()
    cursor = con.cursor()

    sql = f'''SELECT id,username FROM glpi_plugin_telegrambot_users WHERE username = '{usuario}' '''
    # print(sql)
    cursor.execute(sql)
    id = cursor.fetchone()

    
    cursor.close()
    con.close()

    return id[0]

#CAPTURA TITULO
def comecaChamado(message):
    titulo = bot.send_message(message.chat.id, 'Digite o titulo do chamado!')
    bot.register_next_step_handler(titulo, descricaoChamado)

#CAPTURA DESCRIÇÃO
def descricaoChamado(message):
    sessao['chat_id'][message.chat.id]['titulo'] = message.text
    descricao = bot.send_message(message.chat.id, 'Digite o descricao do chamado!')
    bot.register_next_step_handler(descricao, montaChamado)
    
#CRIA CHAMADO  
def montaChamado(message):
    sessao['chat_id'][message.chat.id]['conteudo'] = message.text
    titulo = sessao['chat_id'][message.chat.id]['titulo']
    conteudo = sessao['chat_id'][message.chat.id]['conteudo']
    user = message.from_user.username
    glpiid = getglpiid(user)
    try:
        with conglpi() as glpi:
            id = getglpiid(user)
            glpi.add("ticket", 
                    {"name": titulo, 
                    "content": conteudo,   
                    "itilcategories_id": "1", 
                    "_users_id_requester": id})
            #atualiza_requester_id(glpiid)
    except conglpi().GLPIError as err:
        print(str(err))

def validausernotify(idtelegram, idglpi, usertelegram):
    dt = datetime.datetime.now()
    data_atual = dt.strftime("%Y-%m-%d %H:%M:%S")

    con = conexao()
    cursor = con.cursor()

    sql = f'''SELECT username FROM glpi_plugin_telegrambot_user WHERE username = '{usertelegram}' '''
    cursor.execute(sql)

    usernotify = cursor.fetchall()
        
    if usernotify:
        usuarioExiste = True 
    else:
        usuarioExiste = False 
        sql1 = f'''SELECT firstname,realname FROM glpi_users WHERE id = '{idglpi}' '''
        cursor.execute(sql1)
        nomeCompleto = cursor.fetchone()
        nome = nomeCompleto[0]
        sobrenome = nomeCompleto[1]

    if usuarioExiste:
        pass
    else:
        sql3 = f'''INSERT INTO glpi_plugin_telegrambot_user(id, is_bot, first_name, last_name, username, language_code, created_at, updated_at) VALUES ('{idtelegram}',0,'{nome}','{sobrenome}','{usertelegram}','pt-br','{data_atual}','{data_atual}') '''
        cursor.execute(sql3)



    cursor.close()
    con.close()

#CAPTURA CHAMADOS DO USUARIO
def estruturachamdos(usertelegram):
    id = getglpiid(usertelegram)
    listaids = []
    con = conexao()
    cursor = con.cursor()

    sql = f'''SELECT tickets_id FROM glpi_tickets_users WHERE users_id = '{id}' '''
    cursor.execute(sql)
    idticket = cursor.fetchall()
    for x in idticket:
        listaids.append(x[0])

      
    cursor.close()
    con.close()
    
    return listaids

def listaTodosChamados(message):
    comando = message.text
    ticketid = comando[1:]
    listaids = []
    con = conexao()
    cursor = con.cursor()

    sql = f'''SELECT tickets_id FROM glpi_tickets_users WHERE 1 '''
    cursor.execute(sql)
    idticket = cursor.fetchall()

    cursor.close()
    con.close()

    for x in idticket:
        listaids.append(str(x[0]))

    if ticketid in listaids:
        return True
    else:
        return False

    

def listaInteracoes(idticket):

    listafollowups = []
    try:
        with conglpi() as glpi:
            followups = glpi.get_item("ticketfollowup",{"items_id": idticket,"itemstype":"ticket","content":'nova interação'})
            for x in followups:
                followup = x['content'].split(';')[2][:-3]
                listafollowups.append(followup)
    except glpi_api.GLPIError as err:
        print(str(err))

    return listafollowups

def main():

    @bot.message_handler(commands=['chamado'])
    def novochamado(message):
        telegramId = message.from_user.id
        usertelegram = message.from_user.username
        glpiid = getglpiid(usertelegram)
        validausernotify(telegramId, glpiid, usertelegram)
        sessao['chat_id'][message.chat.id] = {"titulo": "", "conteudo": ""}
        comecaChamado(message)

    @bot.message_handler(commands=['meuschamados'])
    def listachamados(message):
        user = message.from_user.username
        chamados = estruturachamdos(user)
        for x in chamados:
            bot.send_message(message.chat.id, f'Chamado: /{x}')
    
    @bot.message_handler(func=listaTodosChamados)
    def mostrainteracoes(message):
        usertelegram = message.from_user.username
        glpiid = getglpiid(usertelegram)
        user = message.from_user.username
        chamadosDoUsuario = estruturachamdos(user)
        ticketid = message.text[1:]
        if ticketid in chamadosDoUsuario:
            interacoes = listaInteracoes(ticketid)
            i = 0
            for x in interacoes:
                bot.send_message(message.chat.id, f'Interação {i}: \n{x}')
                i += 1
        else:
            bot.send_message(message.chat.id, f'Esse ticket não pertence ao seu usuário')
    # @bot.message_handler(commands=['meuschamados'])dfg
    # def meuschamados(message):
    #     listachamados()

    @bot.message_handler(func=lambda message: True)
    def greet(message):
        user = message.from_user.username

        uservalido = lambda x : True if (x) else False
        if (uservalido(getUser(user))):
            bot.reply_to(message, '''
                Para abrir chamado digite /chamado.
                Para listar chamados digite /meuschamados
            ''')
        else:
            bot.reply_to(message, '''
                Usuário inválido, se isso for um erro solciite acesso através de suporte.sti@vetorial.com
            ''')

    bot.polling() # looking for message

if __name__ == '__main__':
    main()
    