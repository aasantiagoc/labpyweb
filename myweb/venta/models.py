from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.
class Cliente(models.Model): # type: ignore
    id_cliente = models.CharField(
        primary_key=True,
        max_length=8,                      
        error_messages={'max_length': 'El texto debe tener un máximo de 10 caracteres'}
    )
    ape_nom = models.CharField(max_length=200)
    fec_reg = models.DateField()
    fec_sis = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Nombres: {self.ape_nom} - DNI: {self.id_cliente}"
    


'''
Crear el modelo Producto, 
Producto
    id_producto, auto_increment, primary_key, comienza en 1
    nom_prod, varchar(50), caracteres maximo 50
    des_prod, varchar(500), caracteres maximo 500
    precio, numero real de dos decimales, positivo.
    stock, numero entero, positivo, mayor o igual a 0
    activo, valor booleano,(true si esta activo, false si no esta activo)
    fec_vencim, tipo fecha (aaaa-mm-dd)
    fecha_reg, tipo fecha y hora (aaaa-mm-dd hh:mm:ss), auto_now=True

'''
class Producto(models.Model): # type: ignore
    id_producto = models.AutoField(primary_key=True)
    nom_prod = models.CharField(max_length=50, error_messages={'max_length': 'El texto debe tener un máximo de 50 caracteres'})
    des_prod = models.CharField(max_length=500, error_messages={'max_length': 'El texto debe tener un máximo de 500 caracteres'})
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]  # Solo acepta valores > 0
    )
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    fec_vencim = models.DateField()
    fecha_reg = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Producto: {self.nom_prod} - Precio: $/. {self.precio} - Stock: {self.stock} Unidades"

'''
Captura de la Image de la tabla del Producto en el Admin.
'''

class Venta(models.Model): 
    id_venta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)    
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]  # Solo acepta valores > 0
    )
    fecha_reg = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Venta ID: {self.id_venta} - Cliente: {self.id_cliente}"
    

class VentaDetalle(models.Model): 
    id_venta_detalle = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]  # Solo acepta valores > 0
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]  # Solo acepta valores > 0
    )
    fecha_reg = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        cantidad = Decimal(str(self.cantidad))
        precio = Decimal(str(self.precio_unitario))
        self.subtotal = cantidad * precio
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle ID: {self.id_venta_detalle} - Venta: {self.id_venta} - Producto: {self.id_producto} - Cantidad: {self.cantidad}"
    