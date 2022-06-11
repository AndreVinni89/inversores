
from datetime import datetime
import sqlite3
from time import sleep
import requests
import json
from inversor import Inversor

# conecta ao banco de dados 'todo-app'
# caso o banco não exista ele será criado
conn = sqlite3.connect(R"C:\Users\T-GAMER\Documents\github\Inversores\WEB_DJANGO\PI_SIMPLE_BUY_BACKEND\simple_buy\db.sqlite3")



def add(parametro, valor, data):
    """ adiciona uma nova tarefa """
    conn.execute("insert into SimpleBuy_leitura_h (parametro_id, valor, data) values (?, ?, ?)", (parametro, valor, data))
    conn.commit()


def get_inversores(): # retorna um cursor
    return conn.execute("select id from SimpleBuy_inversor")



def get_parameters(inversor_id):
     return conn.execute(f"select id, endereco from SimpleBuy_parametro where id_inversor_id = '{inversor_id}'")


def main():
    x = 200

    while True:
        
        if x == 200:
            x = 0
            list_inversores_ids = [] 
            list_inversores = [] 

            inversores = get_inversores()
            for i in inversores:
                if i[0] not in list_inversores_ids:
                    list_inversores_ids.append(i[0])
                    list_inversores.append(Inversor(i[0]))

            for i in list_inversores:
                parameters = get_parameters(i.id)
                for p in parameters:               
                    if int(p[0]) not in i.parametros_ids:
                        i.parametros_ids.append(p[0])
                        i.parametros_enderecos.append(p[1])
        x += 1

        for inversor in list_inversores:
            parametros_ids = ''
            for param in inversor.parametros_enderecos:
                parametros_ids += (str(param)+'_')

            res = requests.post("http://127.0.0.1:7000/Parametro/",
                                data={"inversor_id": inversor.id, "parametros": parametros_ids}).content
            sleep(1)
            
            body_unicode = res.decode('utf-8')
            leituras_list_temp = json.loads(body_unicode)
            
            print("Leituras: " + str(leituras_list_temp))


            pos = 0
            for leitura in leituras_list_temp["leituras_list"]:
                add(inversor.parametros_ids[pos], leitura['leitura'], datetime.now())
                pos+=1


main()