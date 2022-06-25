from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('visualizar-usina/<str:id>', views.visualizar_usina, name='visualizar-usina'),
    path('equipamentos/<str:id>/<str:filtro>', views.equipamentos, name='equipamentos'),
    path('visualizar-equipamento/<str:id_usina>/<str:id_equipamento>', views.visualizar_equipamento, name='visualizar-equipamento'),
    path('performance', views.performance, name='performance'),
    path('cadastrar_localidade', views.cadastrar_usina, name='cadastrar_localidade'),
    path('cadastrar_inversor', views.cadastrar_inversor, name='cadastrar_inversor'),
    path('lista_inversores', views.lista_inversores, name='lista_inversores'),
    path('info-inversor/<str:inversor_id>', views.info_inversor, name='info_inversor'),
    path('info-inversor/<str:inversor_id>/<str:parametro_id>/excluir', views.info_inversor, name='info_inversor'),
    path('info-inversor/<str:inversor_id>/<str:att>', views.info_inversor, name='info_inversor'),
]