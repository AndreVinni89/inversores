from rest_framework import serializers
from conn import models

class LocalidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Localidade
        fields = '__all__'

class InversorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inversor
        fields = '__all__'

class ParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Parametro
        fields = '__all__'

class LeituraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leitura
        fields = '__all__'