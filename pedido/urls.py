from django.urls import path
from pedido import views


app_name = 'pedido'

urlpatterns = [
    path('pagar/<int:pk>', views.Pagar.as_view(), name='pagar'),
    path('fechar/', views.Fechar.as_view(), name='fechar'),
    path('lista/', views.Lista.as_view(), name='lista'),
    path('detalhe/<int:pk>', views.Detalhe.as_view(), name='detalhe'),
]
