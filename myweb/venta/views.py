### Imports

from django.shortcuts import render
from .models import Cliente, Producto, Venta, VentaDetalle
from .forms import ClienteCreateForm, ProductoCreateForm, ClienteUpdateForm, VentaCreateForm
from django.shortcuts import redirect
from django.contrib import messages
from pprint import pprint
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden

###Others

def handle_undefined_url(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Debe iniciar sesión para acceder al sistema')
        return redirect('login')
    #else:
        #messages.info(request, 'La página solicitada no existe. Se ha redirigirá al inicio.')
    
    return redirect('home')
        

###End 

###login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Usuario y/o contraseña son incorrectos')
        else:
            messages.error(request, 'Usuario y/o contraseña no son válidos')
    
    return render(request, 'venta/login.html')

@login_required
def user_logout(request):
    logout(request)
    #return render(request, 'venta/login.html')
    return redirect('login')

@login_required
def home(request):
    #pprint(request.user.groups)
    #for perm in request.user.get_all_permissions():
        #print(perm)
    #for group in request.user.groups.all():
        #print(group.name)
    user_permissions = {
        'can_manage_clients': (
            request.user.is_superuser or 
            request.user.groups.filter( name = 'gpr_cliente').exists() or
            request.user.has_perm('venta.add_cliente')
        ),
        'can_manage_products': (
            request.user.is_superuser or 
            request.user.groups.filter( name = 'gpr_producto').exists() or
            request.user.has_perm('venta.add_producto')
        ),
        'can_manage_sales': (
            request.user.is_superuser or 
            request.user.groups.filter( name = 'gpr_venta').exists() or
            request.user.has_perm('venta.add_venta')
        ),
        'is_admin': request.user.is_superuser
    }
    #print("Puede gestionar clientes:", user_permissions['can_manage_clients'])
    #print("Puede gestionar productos:", user_permissions['can_manage_products'])
    #print("Puede gestionar todo:", user_permissions['is_admin'])
    context = {
        'user_permissions': user_permissions,
        'user': request.user
    }
    return render(request, 'venta/home.html', context)
###End Login

### Clientes
@login_required
@permission_required('venta.view_cliente', raise_exception=True)
def conculta_clientes(request):

    if not (request.user.is_superuser or 
            request.user.groups.filter(name = 'grp_cliente').exists() or 
            request.user.has_perm('venta.view_cliente')):
        return HttpResponseForbidden('No tiene permisos para ingresar aquí.')

    clientes = Cliente.objects.all().order_by('id_cliente')
    context = {
        'clientes': clientes,
        'titulo': 'Lista de Clientes'
    }
    return render(request, 'venta/lista_clientes.html',context)

@login_required
@permission_required('venta.add_cliente',raise_exception=True)
def crear_cliente(request):
    if not (request.user.is_superuser or 
        request.user.groups.filter(name = 'grp_cliente').exists() or 
        request.user.has_perm('venta.add_cliente')):        
        return render(request, '403.html', {
            'mensaje': 'No tiene permisos para actualizar cliente.'
        }, status=403)

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

@login_required
#@permission_required('venta.change_cliente',raise_exception=True)
def editar_cliente(request):

    if not (request.user.is_superuser or 
            request.user.groups.filter(name = 'grp_cliente').exists() or 
            request.user.has_perm('venta.change_cliente')):
         return render(request, 'venta/403.html', {
            'mensaje': 'No tiene permisos para actualizar cliente.'
        }, status=403)

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
                    #pprint(f"Cliente encontrado: {cliente.fec_reg}")
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

@login_required
@permission_required('venta.delete_cliente',raise_exception=True)
def borrar_cliente( request ):

    if not (request.user.is_superuser or 
            request.user.groups.filter(name = 'grp_cliente').exists() or 
            request.user.has_perm('venta.delete_cliente')):
        return HttpResponseForbidden('No tiene permisos para eliminar cliente.')
   
    clientes_encontrados = []
    tipo_busqueda = 'dni'
    termino_busqueda = '' #dentro de las cajas
    total_registros = 0

    if request.method == 'POST':
        if 'consultar' in request.POST:
            tipo_busqueda = request.POST.get('tipo_busqueda','dni')
            termino_busqueda = request.POST.get('termino_busqueda','dni').strip()

            if termino_busqueda:
                if tipo_busqueda == 'dni':
                    try:
                        cliente = Cliente.objects.get(id_cliente = termino_busqueda)
                        clientes_encontrados = [cliente]
                    except Cliente.DoesNotExist:
                        messages.error(request, 'No se encontraron registros...')
                elif tipo_busqueda == 'nombre':
                      clientes_encontrados = Cliente.objects.filter(
                            ape_nom__icontains = termino_busqueda
                      ).order_by('id_cliente')
                      if not clientes_encontrados:
                          messages.error(request, 'No se encontraron registros...')
                
                total_registros = len(clientes_encontrados)

                if total_registros > 0:
                    messages.success(request, f'Se encontraron {total_registros} registro(s)')

            else:
                messages.error(request, 'Ingrese un término de búsqueda...')
        elif 'eliminar' in request.POST:
            dni_eliminar = request.POST.get('dni_eliminar')
            if dni_eliminar:
                try:
                    cliente = Cliente.objects.get(id_cliente = dni_eliminar)
                    cliente.delete()
                    messages.success(request, f'Cliente con DNI {dni_eliminar} fue eliminado con exito...')

                    tipo_busqueda = request.POST.get('tipo_busqueda_actual','dni')
                    termino_busqueda = request.POST.get('termino_busqueda_actual','')

                    if termino_busqueda:
                        if tipo_busqueda == 'dni':                                                            
                                clientes_encontrados = []
                        elif tipo_busqueda == 'nombre':
                            clientes_encontrados = Cliente.objects.filter(
                                    ape_nom__icontains = termino_busqueda
                            ).order_by('id_cliente')                           
                        
                        total_registros = len(clientes_encontrados)                        

                except Cliente.DoesNotExist:
                        messages.error(request, 'Cliente no encontrado...')
    context = {
        'clientes_encontrados': clientes_encontrados,
        'total_registros': total_registros,
        'tipo_busqueda': tipo_busqueda,
        'termino_busqueda': termino_busqueda
    }

    return render(request, 'venta/borrar_cliente.html', context)

###End Clientes


#### Productos

@login_required
def consulta_productos(request):
    productos = Producto.objects.all().order_by('-id_producto')[:20]  # Limitando a los últimos 10 productos
    context = {
        'productos': productos,
        'titulo': 'Lista de Productos'
    }
    return render(request, 'venta/lista_productos.html',context)

@login_required
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

@login_required
def borrar_producto( request ):
    productos_encontrados = []
    tipo_busqueda = 'nombre'
    termino_busqueda = '' #dentro de las cajas
    total_registros = 0

    if request.method == 'POST':
        if 'consultar' in request.POST:
            tipo_busqueda = request.POST.get('tipo_busqueda','nombre')
            termino_busqueda = request.POST.get('termino_busqueda','nombre').strip()

            if termino_busqueda:
                if tipo_busqueda == 'nombre':
                    try:
                        productos_encontrados = Producto.objects.filter(nom_prod = termino_busqueda).order_by('id_producto')
                        #productos_encontrados = [producto]
                        if not productos_encontrados:
                          messages.error(request, 'No se encontraron registros.')
                    except Producto.DoesNotExist:
                        messages.error(request, 'No se encontro el producto para el término ingresado.')
                elif tipo_busqueda == 'descripcion':
                      productos_encontrados = Producto.objects.filter(
                            des_prod__icontains = termino_busqueda
                      ).order_by('id_producto')
                      if not productos_encontrados:
                          messages.error(request, 'No se encontraron registros.')
                
                total_registros = len(productos_encontrados)

                if total_registros > 0:
                    messages.success(request, f'Se encontraron {total_registros} registro(s)')

            else:
                messages.error(request, 'Ingrese un término de búsqueda...')
        elif 'eliminar' in request.POST:
            producto_eliminar = request.POST.get('producto_eliminar')
            if producto_eliminar:
                try:
                    producto = Producto.objects.get(id_producto = producto_eliminar)
                    nombre_producto = producto.nom_prod
                    producto.delete()
                    messages.success(request, f'El Producto con Nombre {nombre_producto} fue eliminado con exito...')

                    tipo_busqueda = request.POST.get('tipo_busqueda_actual','nombre')
                    termino_busqueda = request.POST.get('termino_busqueda_actual','')

                    if termino_busqueda:
                        if tipo_busqueda == 'nombre':                                                            
                                productos_encontrados = []
                        elif tipo_busqueda == 'descripcion':
                            productos_encontrados = Producto.objects.filter(
                                    nom_prod__icontains = termino_busqueda
                            ).order_by('id_producto')                           
                        
                        total_registros = len(productos_encontrados)                        

                except Producto.DoesNotExist:
                        messages.error(request, 'Producto no encontrado.')
    context = {
        'productos_encontrados': productos_encontrados,
        'total_registros': total_registros,
        'tipo_busqueda': tipo_busqueda,
        'termino_busqueda': termino_busqueda
    }

    return render(request, 'venta/borrar_producto.html', context)

### End Productos

### Ventas
def crear_venta(request):
    _productos = Producto.objects.all()
    if request.method == 'POST':
        form = VentaCreateForm(request.POST)
        id_cliente = None        
        
        if form.is_valid():
            
            id_cliente = request.POST.get('id_cliente', '').strip()           
            productos = request.POST.getlist('producto[]')
            cantidades = request.POST.getlist('cantidad[]')
            
            if not id_cliente:
                messages.error(request, 'Debe seleccionar un cliente para la venta.')                
                return render(request, 'venta/crear_venta.html', {'form': form, 'titulo': 'Crear Venta', 'productos': _productos})
            
            if productos.__len__() <= 1 or cantidades.__len__() <= 1:
                messages.error(request, 'Debe agregar al menos un producto.')                
                return render(request, 'venta/crear_venta.html', {'form': form, 'titulo': 'Crear Venta', 'productos': _productos})
            
            venta = form.save(commit=False)
            venta.total = 0  # lo calculamos abajo
            venta.save()
            total = 0
            
            #print("aqui")
            #for producto in productos:
                #print(producto)
            #return render(request, 'venta/crear_venta.html', {'form': form, 'titulo': 'Crear Venta', 'productos': _productos})
        
            for i in range(len(productos)):
                producto_id = productos[i]            
                cantidad = cantidades[i]
                if producto_id and cantidad:                                                        
                    producto = Producto.objects.get(id_producto=producto_id)   
                    #return render(request, 'venta/crear_venta.html', {'form': form, 'titulo': 'Crear Venta', 'productos': _productos})                 
                    detalle = VentaDetalle(
                        id_venta = venta,
                        id_producto = producto,
                        cantidad = cantidad,
                        precio_unitario = producto.precio,  # asumimos que `precio` está en el modelo Producto
                    )                    
                    detalle.save()
                    
                    total += detalle.subtotal

            venta.total = total
            venta.save()

            messages.success(request, 'Venta registrada exitosamente.')
            return redirect('lista_ventas')
    else:
        form = VentaCreateForm()    

    context = {
        'form': form,
        'titulo': 'Crear Venta',
        'productos': _productos
    }
    return render(request, 'venta/crear_venta.html', context)

def consulta_ventas(request):
    ventas = Venta.objects.filter(total__gt=0.0).order_by('-fecha_reg')[:20]  # Limitando a los últimos 10 productos
    context = {
        'ventas': ventas,
        'titulo': 'Lista de Ventas'
    }
    return render(request, 'venta/lista_ventas.html',context)

def consulta_detalle(request, id):
    detalles = VentaDetalle.objects.filter(id_venta = id).order_by('-id_venta_detalle')[:20]  # Limitando a los últimos 10 productos
    context = {
        'detalles': detalles,
        'titulo': 'Lista de Productos Vendidos'
    }
    return render(request, 'venta/lista_venta_detalle.html',context)
### End