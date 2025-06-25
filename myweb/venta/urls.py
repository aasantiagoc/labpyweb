from django.urls import path
from . import views 

urlpatterns = [
    path('q_cliente', views.conculta_clientes, name = 'lista_clientes'),
    path('c_cliente', views.crear_cliente, name = 'crear_cliente'),
    path('q_producto', views.consulta_productos, name = 'lista_productos'),
    path('c_producto', views.crear_producto, name = 'crear_producto'),
    path('u_cliente', views.editar_cliente, name = 'editar_cliente'),
    path('d_cliente', views.borrar_cliente, name = 'borrar_cliente'),
    path('d_producto', views.borrar_producto, name = 'borrar_producto'),
]
