from webbrowser import get
import telebot
import os 
import glpi_api
import pymysql
import telegram

URL = 'http://172.16.112.164/glpi/apirest.php/'
APPTOKEN = 'ygGEvniPLTKkwVwl4hWm9eKnnbLpXDNYNpb9EAqV'                                           #TOKEN GERADO PARA TODO O SISTEMA
USERTOKEN = 'rLnv6bWO4s18LZZfofawFP7yEyQfekyomPKsYmC9'                                          #API TOKEN DO USUÁRIO
BOTTOKEN = '5341319826:AAHpKduSpGQeO_T2fLpbGmb7hg5lax97Fns'
bot = telebot.TeleBot(BOTTOKEN) # creating a instance


try:
    with glpi_api.connect(URL, APPTOKEN, USERTOKEN) as glpi:
        # #CRIAR CHAMADO
        # glpi.add("ticket", {"name": 'teste', "content":'Fui aberto via API', "itilcategories_id": "1"})
        # #DELETAR CHAMADO
        # glpi.delete("ticket", {"id":'20'})
        # #INSERIR INTERAÇÃO
        # glpi.add("ticketfollowup",{"items_id":'25',"itemstype":"ticket","content":'nova interação'})
        # ALTERAR STATUS TICKET
        # glpi.update('ticket',{"id":'22','status':'5'})
        pass
except glpi_api.GLPIError as err:
    print(str(err))


def conexao():
    connection = pymysql.connect(host='172.16.112.164',
                             user='root',
                             password='vetorial',
                             database='verdanatech_glpi_lab')    
    return connection

def getUser(usuario):
    usuarioExiste = False 
    con = conexao()
    cursor = con.cursor()

    sql = f'''SELECT username FROM glpi_plugin_telegrambot_users WHERE username = '{usuario}' '''
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

def verificar(message):
        return True

def verificaUser(user, message):

    if getUser(user):
        return True
    else:
        return False





def main():
    

    @bot.message_handler(func=verificar)
    def greet(message):
        user = message.from_user.username
        uservalido = lambda x : True if (x) else False
        # bot.reply_to(message, uservalido(getUser(user)))
        if (uservalido(getUser(user))):
            bot.reply_to(message, '''
                Para abrir chamado digite /chamado.
            ''')
        else:
            bot.reply_to(message, '''
                Usuário inválido, se isso for um erro solciite acesso através de suporte.sti@vetorial.com
            ''')

    bot.polling() # looking for message

if __name__ == '__main__':
    main() 