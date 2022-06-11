from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('cadastrar_inversor', views.cadastrar_inversor, name='cadastrar_inversor'),
    path('lista_inversores', views.lista_inversores, name='lista_inversores'),
    path('info-inversor/<str:inversor_id>', views.info_inversor, name='info_inversor'),
    path('info-inversor/<str:inversor_id>/<str:parametro_id>/excluir', views.info_inversor, name='info_inversor'),
    path('info-inversor/<str:inversor_id>/<str:att>', views.info_inversor, name='info_inversor'),
]