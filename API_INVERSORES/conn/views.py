from random import randint

from django.shortcuts import render
import threading
import os
import minimalmodbus

from .models import Parametro
from .utils.Leitura import Leitura


# Create your views here.
def run(request):
    parameter = Parametro(nome="teste",
                          endereco="teste",
                          leitura_media=123,
                          id_inversor=1
                          )

    leitura = Leitura(leitura=1, parameter=parameter)

    return leitura.__dict__

    # connection()


def connection(inversor_id, parametros):
    dev = True

    if not dev:
        instrument = minimalmodbus.Instrument('COM6', inversor_id)  # Aonde 1 é o endereço do escravo
        # instrument.serial.port
        instrument.serial.baudrate = 19200
        instrument.serial.timeout = 5
        # instrument.serial.parity = serial.PARITY_NOME
        # instrument.serial.stopbits = 1
        # instrument.serial.stopbits = 0.2
        # instrument.address                         # this is the slave address number
        instrument.mode = minimalmodbus.MODE_RTU  # rtu or ascii mode
        instrument.clear_buffers_before_each_transaction = True
        instrument.debug = True

        # leitura =  instrument.read_register(parametro_id, 1)

    if dev:
        leituras_list = []

        for parameter in parametros:
            leitura = Leitura(leitura=randint(1, 100), parameter=parameter)
            leituras_list.append(leitura)

    return leituras_list
