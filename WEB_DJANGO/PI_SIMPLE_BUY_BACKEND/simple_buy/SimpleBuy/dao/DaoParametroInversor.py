from .GenericDao import GenericDao
from ..models import Parametro

class DaoParametroInversor(GenericDao):
    def get_parameters_by_inversor(self, inversor):
        try:
            parametros = Parametro.objects.all().filter(id_inversor=inversor.id)
        except:
            raise
        return parametros
