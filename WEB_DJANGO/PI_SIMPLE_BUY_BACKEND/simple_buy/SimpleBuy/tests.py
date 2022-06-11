from django.test import TestCase


from .models import *
from .utils.ValidateLogin import ValidadeLogin
from .dao.GenericDao import GenericDao

class LoginValidateTests(TestCase):
    def test_invalid_login(self):
        user = 'Inexisting User'
        password = '***'

        validate_login = ValidadeLogin()

        context = validate_login.validate_and_get_context(user, password)

        self.assertTrue(context['err'])

    def test_registration(self):
        user = 'adm'
        password = 'adm'
        dao = GenericDao()

        administrador = Administrador(nomeUsuario=user, senha=password, nome=user, email=user, telefone='(41) 3547-8382', plano=1)

        administrador = dao.create(administrador)

        self.assertTrue(administrador)
