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
    selected = False


    def __str__(self):
        return self.nome

class Inversor(models.Model):
    endereco_inversor = models.IntegerField(default=0)
    nome = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    local_id = models.ForeignKey(Localidade, on_delete=models.CASCADE)
    selected = False

    def __str__(self):
        return self.nome

class Parametro(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    leitura_media = models.CharField(max_length=300, default="0")
    id_inversor = models.ForeignKey(Inversor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Leitura_H(models.Model):
    parametro_id = models.FloatField()
    valor = models.FloatField()
    data = models.DateTimeField()

    def __str__(self):
        return str(self.data) + " - " + str(self.valor)




