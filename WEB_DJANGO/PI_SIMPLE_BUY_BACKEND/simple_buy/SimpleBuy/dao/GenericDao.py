class GenericDao:

    def create(self, model):
        try:
           model.save()
        except:
            raise

        return model


    def update(self, model):
        try:
             model.save()
        except:
             raise
        return model

    def delete(self, model):
        return model.delete()

    def selectAll(self, Model):
        list = []
        for i in Model.objects.all():
            list.append(i)
        return list


    def get(self, Model, id):
        try:
            model = Model.objects.get(id=id)
        except:
            raise
        return model


    def get_by_username(self, Model, username):
        try:
            model = Model.objects.get(nomeUsuario=username)
        except:
            raise
        return model

    def get_inversores_by_usina(self, Model, usina):
        try:

            model = Model.objects.all().filter(local_id=usina.id)
        except:
            raise
        return model


    def get_last_leitura_by_param(self, Model, param):
        try:
            model = Model.objects.all().filter(parametro_id=param).order_by('-data')
        except:
            raise
        return model[0]