from django.contrib import admin

from .models import Cliente
from .models import Producto
#Agregar el modelo Cliente al sitio de administración
admin.site.register(Cliente)
admin.site.register(Producto)

