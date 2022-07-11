from webbrowser import get
import telebot
import os 
import glpi_api
import pymysql

URL = 'http://172.16.112.164/glpi/apirest.php/'
APPTOKEN = 'ygGEvniPLTKkwVwl4hWm9eKnnbLpXDNYNpb9EAqV'                                           #TOKEN GERADO PARA TODO O SISTEMA
USERTOKEN = 'rLnv6bWO4s18LZZfofawFP7yEyQfekyomPKsYmC9'                                          #API TOKEN DO USUÁRIO

try:
    with glpi_api.connect(URL, APPTOKEN, USERTOKEN) as glpi:
        # #CRIAR CHAMADO
        # glpi.add("ticket", {"name": 'teste', "content":'Fui aberto via API', "itilcategories_id": "1"})
        # #DELETAR CHAMADO
        # glpi.delete("ticket", {"id":'20'})
        # #INSERIR INTERAÇÃO
        # glpi.add("ticketfollowup",{"items_id":'25',"itemstype":"ticket","content":'nova interação'})
        pass
except glpi_api.GLPIError as err:
    print(str(err))


def conexao():
    connection = pymysql.connect(host='localhost',
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

print(getUser('guilherme_rcunha'))
