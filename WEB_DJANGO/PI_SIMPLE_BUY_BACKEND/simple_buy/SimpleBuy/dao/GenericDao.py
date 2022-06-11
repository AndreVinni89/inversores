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