import glpi_api

URL = 'http://172.16.112.164/glpi/apirest.php/'
APPTOKEN = 'ygGEvniPLTKkwVwl4hWm9eKnnbLpXDNYNpb9EAqV'                                           #TOKEN GERADO PARA TODO O SISTEMA
USERTOKEN = 'rLnv6bWO4s18LZZfofawFP7yEyQfekyomPKsYmC9'                                          #API TOKEN DO USUÁRIO

try:
    with glpi_api.connect(URL, APPTOKEN, USERTOKEN) as glpi:
        #CRIAR CHAMADO
        glpi.add("ticket", {"name": 'teste', "content":'Fui aberto via API', "itilcategories_id": "1"})
        #DELETAR CHAMADO
        glpi.delete("ticket", {"id":'20'})
        #INSERIR INTERAÇÃO
        glpi.add("ticketfollowup",{"items_id":'25',"itemstype":"ticket","content":'nova interação'})
except glpi_api.GLPIError as err:
    print(str(err))


=

