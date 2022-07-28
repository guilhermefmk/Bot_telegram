from webbrowser import get
import telebot
import glpi_api
import pymysql
import paramiko
from paramiko import SSHClient

URL = 'http://172.16.112.164/glpi/apirest.php/'                                                 #URL API GLPI
APPTOKEN = 'XvRM61PGyo70FTwMEmJxDilK8lXmacjtoyciiuNj'                                           #TOKEN GERADO PARA TODO O SISTEMA
USERTOKEN = 'CZoqXFVys4u0IKRssKIbDsQRwwMFIxwTY6ZqvE2L'                                          #API TOKEN DO USUÁRIO
BOTTOKEN = '5573257814:AAEBOz58TqmfdmT_AmSguhW1Nr8xmMxjpPE'
bot = telebot.TeleBot(BOTTOKEN)
sessao = {"chat_id": {}}





#CONECTA BANCO
def conexao():
    connection = pymysql.connect(host='172.16.112.164',
                             user='root',
                             password='vetorial',
                             database='verdanatech_glpi_lab')    
    return connection

#CONECTA GLPI
def conglpi():
    return glpi_api.connect(URL, APPTOKEN, USERTOKEN)

def captura_senha_antiga_ad(message):
    senha = bot.send_message(message.chat.id, 'Digite sua senha atual da VPN')
    bot.register_next_step_handler(senha, estrutura_validacao)

def estrutura_validacao(message):
    senha_antiga = message.text
    usertelegram = message.from_user.username
    userglpi = getglpiuser(getglpiid(usertelegram))
    valida_senha_ad(message,userglpi, senha_antiga)



#VALIDA SE A SENHA ANTIGA DO USUÁRIO É VÁLIDA, FAZENDO UMA CONEXÃO SIMPLES VIA SSH E FECHANDO LOGO EM SEGUIDA
def valida_senha_ad(message, user,senha):
    client_valida_senha=SSHClient()
    client_valida_senha.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client_valida_senha.connect('172.16.112.141', 22, username=f'{user}', password=f'{senha}', timeout=5)
        client_valida_senha.close()
        autenticou = True
    except:
        client_valida_senha.close()
        autenticou = False
    print(autenticou)
    if autenticou:
        nova_senha = bot.send_message(message.chat.id, 'Digite sua nova senha para a VPN')
        bot.register_next_step_handler(nova_senha, estrutura_alteracao)
    else:
        bot.send_message(message.chat.id, 'Senha não eh valida')




def estrutura_alteracao(message):
    nova_senha = message.text

    usertelegram = message.from_user.username
    userglpi = getglpiuser(getglpiid(usertelegram))
    
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('172.16.112.141', 22, username='Administrator', password='Vetorial#20', timeout=5)

    cmd = f"powershell -InputFormat none -OutputFormat TEXT ./Desktop/script.ps1 -user '{userglpi}' -senha '{nova_senha}'"
    stdin, stdout, stderr = client.exec_command(cmd)
            #  gets the result of the command execution, and the data returned is one list

    stdin.close()


    client.close()





#RETORNA O ID DO USUÁRIO NO GLPI BASEADO NO USUÁRIO DO TELEGRAM
def getglpiid(usuariotelegram):
    
    con = conexao()
    cursor = con.cursor()

    sql = f'''SELECT id,username FROM glpi_plugin_telegrambot_users WHERE username = '{usuariotelegram}' '''
    # print(sql)
    cursor.execute(sql)
    id = cursor.fetchone()

    
    cursor.close()
    con.close()

    return id[0]
#RETORNA O USER NO GLPI BASEADO NO USUÁRIO DO TELEGRAM
def getglpiuser(idglpi):
    
    con = conexao()
    cursor = con.cursor()

    sql = f'''SELECT name FROM glpi_users WHERE id = '{idglpi}' '''
    # print(sql)
    cursor.execute(sql)
    id = cursor.fetchone()

    
    cursor.close()
    con.close()

    return id[0]

#RETORNA SE USUÀRIO ESTA REGISTRADO NO BANCO BASEADO NA TABELA DO PLUGIN DO GLPI
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
    

def main():

    
    @bot.message_handler(commands=['senhavpn'])
    def trocasenhavpn(message):
        captura_senha_antiga_ad(message)
  

        

    @bot.message_handler(func=lambda message: True)
    def greet(message):
        usertelegram = message.from_user.username
        userglpi = getglpiuser(getglpiid(usertelegram))
        uservalido = lambda x : True if (x) else False
        if (uservalido(getUser(usertelegram))):
            bot.reply_to(message, f'''
                Olá {userglpi}, para redefinir sua senha de VPN digite /senhavpn
            ''')
        else:
            bot.reply_to(message, '''
                Usuário inválido, se isso for um erro solciite acesso através de suporte.sti@vetorial.com
            ''')

    

    bot.polling() # looking for message

if __name__ == '__main__':
    main()
    