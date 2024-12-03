from django.urls import path
from pedido import views


app_name = 'pedido'

urlpatterns = [
    path('', views.Pagar.as_view(), name='pagar'),
    path('fechar/', views.Fechar.as_view(), name='fechar'),
    path('detalhe/', views.Detalhe.as_view(), name='detalhe'),
]
