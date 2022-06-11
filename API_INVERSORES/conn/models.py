from django.db import models

from django.db import models
# Create your models here.

class Localidade(models.Model):
    nome = models.CharField(max_length=200)
    identificacao_unidade = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    cep = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Inversor(models.Model):
    endereco_inversor = models.IntegerField(default=0)
    nome = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    local_id = models.ForeignKey(Localidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Parametro(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    leitura_media = models.CharField(max_length=300, default="0")
    id_inversor = models.IntegerField()

    def __str__(self):
        return self.nome


class Leitura(models.Model):
    leitura = models.IntegerField()
    parametro = models.ForeignKey(Parametro, on_delete=models.CASCADE)

    def __str__(self):
        return self.leitura



