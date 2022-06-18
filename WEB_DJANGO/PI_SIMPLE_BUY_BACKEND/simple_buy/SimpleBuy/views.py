from inspect import Parameter
from random import randint
from time import sleep
from django.http import HttpResponse
from django.shortcuts import render
from .dao.GenericDao import GenericDao
from .dao.DaoParametroInversor import DaoParametroInversor
from .models import *
from asgiref.sync import sync_to_async
from datetime import datetime
from.utils.Leitura import Leitura
import requests
import json
import sqlite3


localDB = R"C:\Users\T-GAMER\Documents\github\Inversores\WEB_DJANGO\PI_SIMPLE_BUY_BACKEND\simple_buy\db.sqlite3"

def format_number(num):
    if num < 10:
        return '0'+str(num)
    return str(num)



class usinaDTO:
    def __init__(self, usina_nome, usina_id, potencia, local, dia, mes, ano):
        self.usina_nome = usina_nome
        self.usina_id = usina_id
        self.usina_local = local
        self.dia = dia
        self.mes = mes
        self.ano = ano
        self.potencia = potencia

class InversorDTO:
    def __init__(self, inversor_nome, inversor_id, inversor_marca, potencia,dia, mes, ano, total):
        self.nome = inversor_nome
        self.id = inversor_id
        self.marca = inversor_marca
        self.dia = dia
        self.mes = mes
        self.ano = ano
        self.total = total
        self.potencia = potencia



def index(request):

    dao = GenericDao()
    daoParameter = DaoParametroInversor()
    usinas = dao.selectAll(Localidade)

    totalDia = 0
    totalMes = 0
    totalAno = 0



    usinasDados = []

    for usina in usinas:
        somaDia = 0
        somaMes = 0
        somaAno = 0
        somaTotal = 0
        somaPotencia = 0


        inversores = dao.get_inversores_by_usina(Inversor, usina)
        for inversor in inversores:
            parametros = daoParameter.get_parameters_by_inversor(inversor)

            for par in parametros:
                if 'potencia' in par.nome:
                    somaPotencia += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
                if 'geracao_dia' in par.nome:
                    somaDia += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
                if 'geracao_mes' in par.nome:
                    somaMes += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
                if 'geracao_ano' in par.nome:
                    somaAno += dao.get_last_leitura_by_param(Leitura_H, par.id).valor

        usinasDados.append(usinaDTO(usina.nome, usina.id, somaPotencia, usina.cidade, somaDia, somaMes, somaAno))
        totalAno += somaAno
        totalMes += somaMes
        totalDia += somaDia

    co2 = (totalMes * 12) * 0.57

    context = {
        "usinas": usinasDados,
        "totalDia": totalDia,
        "totalMes": totalMes,
        "totalAno": totalAno,
        "co2": co2
    }

    return render(request, 'SimpleBuy/index.html', context)

def visualizar_usina(request, id):
    dao = GenericDao()
    daoParameter = DaoParametroInversor()


    usinas = dao.selectAll(Localidade)

    for u in usinas:
        if str(u.id) == id:
            u.selected = True
            break

    usina = dao.get(Localidade, id)

    somaDia = 0
    somaMes = 0
    somaAno = 0
    somaPotencia = 0

    inversores = dao.get_inversores_by_usina(Inversor, usina)
    for inversor in inversores:
        parametros = daoParameter.get_parameters_by_inversor(inversor)

        for par in parametros:
            if 'potencia' in par.nome:
                somaPotencia += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
            if 'geracao_dia' in par.nome:
                somaDia += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
            if 'geracao_mes' in par.nome:
                somaMes += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
            if 'geracao_ano' in par.nome:
                somaAno += dao.get_last_leitura_by_param(Leitura_H, par.id).valor

    context = {
        "usinas": usinas,
        "usina": usina,
        "totalDia": somaDia,
        "totalMes": somaMes,
        "totalAno": somaAno,
        "potencia": somaPotencia
    }


    return render(request, 'SimpleBuy/visualizar-usina.html', context)

def equipamentos(request, id=1):
    dao = GenericDao()
    daoParameter = DaoParametroInversor()

    usina = dao.get(Localidade, id)
    usinas = dao.selectAll(Localidade)


    for u in usinas:
        if str(u.id) == id:
            u.selected = True
            break

    somaDia = 0
    somaMes = 0
    somaAno = 0
    somaPotencia = 0

    inversores = dao.get_inversores_by_usina(Inversor, usina)
    inversoresData = []
    for inversor in inversores:
        parametros = daoParameter.get_parameters_by_inversor(inversor)

        valorDia = 0
        valorMes = 0
        valorAno = 0
        valorPotencia = 0
        valorTotal = 0

        for par in parametros:
            if 'potencia' in par.nome:
                valorPotencia += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
            if 'geracao_dia' in par.nome:
                valorDia += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
            if 'geracao_mes' in par.nome:
                valorMes += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
            if 'geracao_ano' in par.nome:
                valorAno += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
            if 'geracao_total' in par.nome:
                valorTotal += dao.get_last_leitura_by_param(Leitura_H, par.id).valor


        inversoresData.append(InversorDTO(inversor.nome, inversor.id, inversor.marca, valorPotencia, valorDia, valorMes, valorAno, valorTotal))


        somaDia = valorDia
        somaMes = valorMes
        somaAno = valorAno
        somaPotencia = valorPotencia


    co2 = (somaMes * 12) * 0.57


    context = {
        "usinas": usinas,
        "usina": usina,
        "totalDia": somaDia,
        "totalMes": somaMes,
        "totalAno": somaAno,
        "potencia": somaPotencia,
        "inversores": inversoresData,
        "co2": co2
    }

    return render(request, 'SimpleBuy/equipamentos.html', context)


def visualizar_equipamento(request, id_usina, id_equipamento):
    dao = GenericDao()
    daoParameter = DaoParametroInversor()

    usina = dao.get(Localidade, id_usina)
    inversores = dao.get_inversores_by_usina(Inversor, usina)

    for i in inversores:
        if str(i.id) == id_equipamento:
            inversor = i
            i.selected = True
            break

    inversor = dao.get(Inversor, id_equipamento)



    parametros = daoParameter.get_parameters_by_inversor(inversor)

    valorDia = 0
    valorMes = 0
    valorAno = 0
    valorPotencia = 0
    valorTotal = 0
    valorFrequencia = 0
    horasHoje = 0


    for par in parametros:
        if 'potencia' in par.nome:
            valorPotencia += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
        if 'geracao_dia' in par.nome:
            valorDia += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
        if 'geracao_mes' in par.nome:
            valorMes += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
        if 'geracao_ano' in par.nome:
            valorAno += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
        if 'geracao_total' in par.nome:
            valorTotal += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
        if 'frequencia' in par.nome:
            valorFrequencia += dao.get_last_leitura_by_param(Leitura_H, par.id).valor
        if 'horasHoje' in par.nome:
            horasHoje += dao.get_last_leitura_by_param(Leitura_H, par.id).valor




    context = {
        "usina": usina,
        "inversores": inversores,
        "totalDia": valorDia,
        "totalMes": valorMes,
        "totalAno": valorAno,
        "potencia": valorPotencia,
        "valorFrequencia": valorFrequencia,
        "horasHoje": horasHoje
    }
    return render(request, 'SimpleBuy/visualizar-equipamento.html', context)


def performance(request):
    localidade = ""

    context = {
        "localidade": localidade
    }
    return render(request, 'SimpleBuy/performance.html', context)




def cadastrar_usina(request):

    dao = GenericDao()
    localidade = None

    cidade = request.POST.get('cidade')
    email = request.POST.get('email')
    cep = request.POST.get('cep')
    estado = request.POST.get('estado')
    bairro = request.POST.get('bairro')
    endereco = request.POST.get('endereco')
    identificacao = request.POST.get('identificacao')
    name = request.POST.get('name')


    if name and identificacao and endereco and bairro and cidade and estado and cep and email:

        localidade = Localidade(nome=name,
                                identificacao_unidade=identificacao,
                                endereco=endereco,
                                bairro=bairro,
                                cidade=cidade,
                                estado=estado,
                                cep=cep,
                                email=email)

        localidade = dao.create(localidade)

    context = {
        "localidade": localidade
    }
    return render(request, 'SimpleBuy/cadastrar-localidade.html', context)


def cadastrar_inversor(request):
    dao = GenericDao()
    localidades = dao.selectAll(Localidade)
    inversores = dao.selectAll(Inversor)
    inversor = None
    endereco_inversor = request.POST.get('endereco_inversor')
    name = request.POST.get('name')
    marca = request.POST.get('marca')

    try:
        localidade = dao.get(Localidade, request.POST.get('localidade'))
    except:
        localidade = None



    if name and marca and localidade:
        inversor = Inversor(endereco_inversor=endereco_inversor, nome=name, marca=marca, local_id=localidade)
        inversor = dao.create(inversor)




    context = {
        "localidades": localidades,

        "inversor": inversor
    }

    return render(request, 'SimpleBuy/cadastrar_inversores.html', context)


def lista_inversores(request):
    dao = GenericDao()

    inversores = dao.selectAll(Inversor)

    context = {
        "inversores": inversores
    }

    return render(request, 'SimpleBuy/lista_inversores.html', context)


def info_inversor(request, inversor_id, parametro_id=None, att=""):
    dao = GenericDao()
    daoParametros = DaoParametroInversor()
    inversor = dao.get(Inversor, inversor_id)
    delete = False

    parametros = daoParametros.get_parameters_by_inversor(inversor)


    name = request.POST.get('name-parametro')
    endereco = request.POST.get('endereco-parametro')




    if name and endereco:
        parametro = Parametro(nome=name, endereco=endereco, id_inversor=inversor)

        parametro = dao.create(parametro)


    if parametro_id != None:
        parametro = dao.get(Parametro, parametro_id)
        dao.delete(parametro)
        delete = True

    if att != "":

        inversor_id = inversor.endereco_inversor
        time_list = []
        leituras_list = []


        total_time = 5
        atual_time = 0


        #connection(inversor_id, parametros)
        parametros_ids = ''
        for param in parametros:
            parametros_ids += (str(param.endereco)+'_')

        print('here')
        print(parametros_ids)

        while atual_time <= total_time:
            res = requests.post("http://127.0.0.1:7000/Parametro/", data={"inversor_id": inversor_id, "parametros": parametros_ids}).content

            body_unicode = res.decode('utf-8')
            leituras_list_temp = json.loads(body_unicode)

            time_list.append(atual_time)
            leituras_list.append(leituras_list_temp)
            atual_time += 0.1
            sleep(0.1)
            

      


        tensao_x_x(parametros, leituras_list, time_list)
        tensao_simples(parametros, leituras_list, time_list)
        potencia(parametros, leituras_list, time_list)



        for parametro in parametros:
            temp = []
            for leituras in leituras_list:
                for leitura in leituras["leituras_list"]:
                    if int(leitura['parameter']) == int(parametro.endereco):
                        temp.append(int(leitura['leitura']))

            parametro.leitura = sum(temp) / len(temp)
            dao.update(parametro)

    context = {
        "inversor": inversor,
        "parametros": parametros,
        "delete": delete,
        "att": att
    }

    return render(request, 'SimpleBuy/info_inversor.html', context)


def tensao_x_x(parametros, leituras_list, time_list):

    parameters_filtered = []
    parameters_filtered.append(parametros.filter(endereco=1))
    parameters_filtered.append(parametros.filter(endereco=2))
    parameters_filtered.append(parametros.filter(endereco=3))

    parameter_reads = []




    for parametro in parameters_filtered:
        temp = []
        for leituras in leituras_list:
            for leitura in leituras["leituras_list"]:
                if int(leitura['parameter']) == int(parametro[0].endereco):
                    temp.append(leitura['leitura'])
                    parametro.leitura = leitura['leitura']

        parameter_reads.append(temp)


    fig, ax = plt.subplots()    
    for par in parameter_reads:
        ax.plot(time_list, par); 
    ax.set_xlabel('Tempo(S)')  # Add an x-label to the axes.
    ax.set_ylabel('Volts')  # Add a y-label to the axes.
    ax.set_title("Tensão")  # Add a title to the axes.
    ax.legend();  # Add a legend.
    ax.grid(True)
    fig.savefig(f'./SimpleBuy/static/img/Tensao_x_x') 
            
def tensao_simples(parametros, leituras_list, time_list):

    parameters_filtered = []
    parameters_filtered.append(parametros.filter(endereco=4))
    parameters_filtered.append(parametros.filter(endereco=5))
    parameters_filtered.append(parametros.filter(endereco=6))

    parameter_reads = []



    for parametro in parameters_filtered:
        temp = []
        for leituras in leituras_list:
            for leitura in leituras["leituras_list"]:
                if int(leitura['parameter']) == int(parametro[0].endereco):
                    temp.append(leitura['leitura'])
                    parametro.leitura = leitura['leitura']

        parameter_reads.append(temp)


    fig, ax = plt.subplots()  
    for par in parameter_reads:
        ax.plot(time_list, par); 
    ax.set_xlabel('Tempo(S)')  # Add an x-label to the axes.
    ax.set_ylabel('Volts')  # Add a y-label to the axes.
    ax.set_title("Tensão Simples")  # Add a title to the axes.
    ax.legend();  # Add a legend.
    ax.grid(True)
    fig.savefig(f'./SimpleBuy/static/img/Tensao_simples') 

def potencia(parametros, leituras_list, time_list):
    parameters_filtered = []
    parameters_filtered.append(parametros.filter(endereco=4))
    parameters_filtered.append(parametros.filter(endereco=5))
    parameters_filtered.append(parametros.filter(endereco=6))

    parameter_reads = []

    for parametro in parameters_filtered:
        temp = []
        for leituras in leituras_list:
            for leitura in leituras["leituras_list"]:
                if int(leitura['parameter']) == int(parametro[0].endereco):
                    temp.append(leitura['leitura'])
                    parametro.leitura = leitura['leitura']

        parameter_reads.append(temp)

    fig, ax = plt.subplots()  
    for par in parameter_reads:
        ax.plot(time_list, par); 
    ax.set_xlabel('Tempo(S)')  # Add an x-label to the axes.
    ax.set_ylabel('Volts')  # Add a y-label to the axes.
    ax.set_title("Potencia")  # Add a title to the axes.
    ax.legend();  # Add a legend.
    ax.grid(True)
    fig.savefig(f'./SimpleBuy/static/img/Potencia') 

def connection(inversor_id, parametros):

    dev = True

    if not dev:
        instrument = minimalmodbus.Instrument('COM6', inversor_id) # Aonde 1 é o endereço do escravo
        #instrument.serial.port
        instrument.serial.baudrate = 19200
        instrument.serial.timeout = 5
        #instrument.serial.parity = serial.PARITY_NOME
        #instrument.serial.stopbits = 1
        #instrument.serial.stopbits = 0.2
        #instrument.address                         # this is the slave address number
        instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
        instrument.clear_buffers_before_each_transaction = True
        instrument.debug = True

        #leitura =  instrument.read_register(parametro_id, 1)

    if dev:
        leituras_list = []

        for parameter in parametros:
            leitura = Leitura(leitura=randint(1, 100), parameter=parameter)
            leituras_list.append(leitura)
            


    return leituras_list