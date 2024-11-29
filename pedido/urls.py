from django.urls import path
from pedido import views


app_name = 'pedido'

urlpatterns = [
    path('pagar/', views.Pagar.as_view(), name='pagar'),
    path('fechar/', views.Fechar.as_view(), name='fechar'),
    path('detalhe/<int:pk>/', views.Detalhe.as_view(), name='detalhe'),
]
