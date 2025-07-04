from django.urls import path, re_path
from . import views 

urlpatterns = [
    path('home', views.home, name= 'home'), # Pagina Principal
    path('', views.user_login, name= 'login'),
    #path('login/', views.user_login, name= 'login'),
    path('logout', views.user_logout, name= 'logout'),
    path('venta/q_cliente', views.conculta_clientes, name = 'lista_clientes'),
    path('venta/c_cliente', views.crear_cliente, name = 'crear_cliente'),
    path('venta/u_cliente', views.editar_cliente, name = 'editar_cliente'),
    path('venta/d_cliente', views.borrar_cliente, name = 'borrar_cliente'),

    path('venta/q_producto', views.consulta_productos, name = 'lista_productos'),
    path('venta/c_producto', views.crear_producto, name = 'crear_producto'),    
    path('venta/d_producto', views.borrar_producto, name = 'borrar_producto'),

    path('venta/c_venta', views.crear_venta, name = 'crear_venta'),  
    path('venta/q_venta', views.consulta_ventas, name = 'lista_ventas'),
    path('venta/q_venta_detalle/<int:id>/', views.consulta_detalle, name = 'lista_detalle_ventas'),

    re_path(r'^.*/$', views.handle_undefined_url, name = 'catch_all')
]
