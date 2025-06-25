### Imports

from django.shortcuts import render
from .models import Cliente, Producto
from .forms import ClienteCreateForm, ProductoCreateForm, ClienteUpdateForm
from django.shortcuts import redirect
from django.contrib import messages
from pprint import pprint

### Clientes
def conculta_clientes(request):
    clientes = Cliente.objects.all().order_by('id_cliente')
    context = {
        'clientes': clientes,
        'titulo': 'Lista de Clientes'
    }
    return render(request, 'venta/lista_clientes.html',context)

def crear_cliente(request):
    dni_duplicado = False
    if request.method == 'POST':
        #dni_duplicado = False
        form = ClienteCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            #return redirect('lista_clientes')
        else:
            if 'id_cliente' in form.errors:
                #pprint(f"form.errors.get_json_data() '{form.errors.get_json_data()}'")
                #pprint(form.errors['id_cliente'].get_json_data())
                for error in form.errors['id_cliente']:
                    #pprint(error)
                    if str(error) == "DNI_DUPLICADO":
                        dni_duplicado = True
                        form.errors['id_cliente'].clear()  # Limpiar el error de duplicado
                    break;
    else:
        form = ClienteCreateForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Cliente',
        'dni_duplicado': dni_duplicado
    }
    return render(request, 'venta/crear_cliente.html', context)

def editar_cliente(request):
    cliente = None
    dni_buscado = None
    form = None
    if request.method == 'POST':
        if 'buscar' in request.POST:
            dni_buscado = request.POST.get('dni_busqueda', '').strip()
            if dni_buscado:
                try:
                    cliente = Cliente.objects.get(id_cliente=dni_buscado)
                    form = ClienteUpdateForm(instance=cliente)
                    messages.success(request, f'Cliente encontrado: {cliente.ape_nom}.')
                    pprint(f"Cliente encontrado: {cliente.fec_reg}")
                except Cliente.DoesNotExist:
                    messages.error(request, 'Cliente no encontrado.')
                    #return redirect('crear_cliente')
            else: 
                messages.error(request, 'Por favor, ingrese un DNI válido para buscar.')
                #return redirect('crear_cliente')
        #form = ClienteCreateForm(request.POST, instance=cliente)
        elif 'guardar' in request.POST:
            dni_buscado = request.POST.get('dni_buscado', '').strip() or request.POST.get('id_cliente', '').strip()
            if dni_buscado:
                try:
                    cliente = Cliente.objects.get(id_cliente=dni_buscado)
                    form = ClienteUpdateForm(request.POST, instance=cliente)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Cliente actualizado exitosamente.')
                        cliente.refresh_from_db()
                        form = ClienteUpdateForm(instance=cliente)
                        #return redirect('lista_clientes')
                    else:
                        messages.error(request, 'Error en los datos. Verifique los datos ingresados.')
                except Cliente.DoesNotExist:
                    messages.error(request, 'Cliente no encontrado.')
            else:
                messages.error(request, 'Por favor, ingrese un DNI válido para guardar.')
                #return redirect('crear_cliente')
    #else:
        #form = ClienteCreateForm(instance=cliente)
    
    context = {
        'form': form,
        'titulo': 'Editar Cliente',
        'cliente_encontrado': cliente is not None,
        'cliente': cliente,
        'dni_buscado': dni_buscado
    }
    return render(request, 'venta/editar_cliente.html', context)
###End Clientes

#### Productos
def consulta_productos(request):
    productos = Producto.objects.all().order_by('-id_producto')[:10]  # Limitando a los últimos 10 productos
    context = {
        'productos': productos,
        'titulo': 'Lista de Productos'
    }
    return render(request, 'venta/lista_productos.html',context)

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('lista_productos')
    else:
        form = ProductoCreateForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Producto'
    }
    return render(request, 'venta/crear_producto.html', context)

### End Productos