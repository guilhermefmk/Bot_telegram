'''
Campos API 

- Entidade
- Tipo
- Categoria
- Origem da requisição
- Titulo
- Descrição
'''

#!/bin/bash

GLPI_URL_API='http://172.16.112.164/glpi/apirest.php/'                                                              #URL DA API
GLPI_APP_TOKEN='ygGEvniPLTKkwVwl4hWm9eKnnbLpXDNYNpb9EAqV'                                                                                                   #TOKEN GERADO PELO INIT
GLPI_USER_TOKEN='c4uvzQcjI7l0WLuBL07PHO04NGJ8UTVsuVZJXawD'                                                          #TOKEN GERADO PARA CADA USER
GLPI_ID_ENTIDADE='0'                                                                                                #ID DA ENTIDADE DE ABERTURA DO CHAMADO
GLPI_ID_CATEGORIA='1'                                                                                               #ID DA CATEGORIA
GLPI_ID_TIPO='2'                                                                                                    #TIPO DE CHAMADO [1=Incidente,2=Requisição]
GLPI_ID_ORIGEM_REQUISICAO='8'                                                                                       #ORIGEM DA REQUISIÇÂO, É DE ONDE VEIO O CHAMADO


#API criar sessão


echo -e $(echo $(date +"$LOG_TIME_FORMAT"))"  \tAbrir sessão" >> $LOGFILE;
SESSION_TOKEN
