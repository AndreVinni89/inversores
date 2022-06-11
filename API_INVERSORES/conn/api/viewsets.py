import json
from random import randint

import minimalmodbus
from rest_framework import viewsets, status
from rest_framework.response import Response

from conn.api import serializers
from conn import models
from conn.utils.Leitura import Leitura


class LocalidadeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LocalidadeSerializer
    queryset = models.Localidade.objects.all()


class InversorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InversorSerializer
    queryset = models.Inversor.objects.all()


class ParametroViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ParametroSerializer
    queryset = models.Parametro.objects.all()

    def create(self, request, *args, **kwargs):
        print('--------------------------')

        inversor_id = request.data["inversor_id"]
        parametros_raw = request.data["parametros"]
        parametros = parametros_raw.split('_')
        if len(parametros) > 0:
            parametros.pop()

        leituras_list = self.connection(inversor_id, parametros)


        headers = self.get_success_headers(request.data)
        return Response({"leituras_list": leituras_list}, status=status.HTTP_200_OK, headers=headers)

    def connection(self, inversor_id, parametros):
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
                leituras_list.append(leitura.__dict__)

        return leituras_list


class LeituraViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LeituraSerializer
    queryset = models.Leitura.objects.all()
