from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, ArriendoForm, ReparacionForm
from .models import Cliente, Arriendo, Bicicleta, Reparacion
from itertools import chain
from django.contrib.auth.decorators import login_required
from Carro.models import Orden as OrdenCompra
from django.db.models import Q
from django.contrib import messages
from django.conf import settings


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            
            # Logear al usuario luego del registro
            login(request, user) 
            # Redirije al page Home
            return redirect('home') 

    else:
        form = CustomUserCreationForm()

    return render(request, 'clientes/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Cambiamos el nombre de la variable para que sea más claro
            username_ingresado = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password')
            
            # Usamos el parámetro 'username', como lo espera el modelo
            user = authenticate(username=username_ingresado, password=password) 
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Correo electrónico o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'clientes/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def arriendo(request):
    bicicletas = Bicicleta.objects.filter(disponible_para_arriendo=True)
    if request.method == 'POST':
        form = ArriendoForm(request.POST)
        if form.is_valid():
            arriendo = form.save(commit=False)
            arriendo.cliente = request.user
            arriendo.save()
            # Redirigir a la nueva vista de pago de arriendo
            return redirect('pagar_arriendo', arriendo_id=arriendo.id)
        else:
            print(form.errors)
            return render(request, 'clientes/arriendo.html', {'form': form, 'bicicletas': bicicletas, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})
    else:
        form = ArriendoForm()
    return render(request, 'clientes/arriendo.html', {'form': form, 'bicicletas': bicicletas, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

@login_required
def pagar_arriendo(request, arriendo_id):
    arriendo = get_object_or_404(Arriendo, id=arriendo_id, cliente=request.user)
    return render(request, 'clientes/pagar_arriendo.html', {'arriendo': arriendo, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

@login_required
def orden_arriendo(request, orden_id):
    orden = get_object_or_404(Arriendo, id=orden_id)
    return render(request, 'clientes/orden_arriendo.html', {'orden': orden})

@login_required
def reparacion(request):
    if request.method == 'POST':
        form = ReparacionForm(request.POST)
        if form.is_valid():
            reparacion = form.save(commit=False)
            reparacion.cliente = request.user
            reparacion.save()
            reserva = form.cleaned_data['reserva_tecnico']
            reserva.esta_disponible = False
            reserva.save()
            return redirect('reparacion_exito')
    else:
        form = ReparacionForm()
    print(form.fields['reserva_tecnico'].queryset)
    return render(request, 'clientes/reparacion.html', {'form': form})

def reparacion_exito(request):
    return render(request, 'clientes/home.html')
    
def home(request):
    bicicletas = Bicicleta.objects.all()
    return render(request, 'clientes/home.html', {'bicicletas': bicicletas  })

def catalogo_bicicletas(request):
    bicicletas = Bicicleta.objects.filter(disponible_para_venta=True, stock__gt=0)
    
    # Filtro por tipo
    tipo = request.GET.get('tipo')
    if tipo:
        bicicletas = bicicletas.filter(tipo=tipo)
    
    # Filtro por rango de precio
    precio_range = request.GET.get('precio')
    if precio_range:
        if precio_range == '0-200000':
            bicicletas = bicicletas.filter(precio_venta__lte=200000)
        elif precio_range == '200000-500000':
            bicicletas = bicicletas.filter(precio_venta__gt=200000, precio_venta__lte=500000)
        elif precio_range == '500000+':
            bicicletas = bicicletas.filter(precio_venta__gt=500000)
    
    # Filtro por marca
    marca = request.GET.get('marca')
    if marca:
        bicicletas = bicicletas.filter(marca__iexact=marca)
    
    # Ordenamiento
    orden = request.GET.get('orden')
    if orden:
        if orden == 'precio_asc':
            bicicletas = bicicletas.order_by('precio_venta')
        elif orden == 'precio_desc':
            bicicletas = bicicletas.order_by('-precio_venta')
        elif orden == 'nombre_asc':
            bicicletas = bicicletas.order_by('marca', 'modelo')
        elif orden == 'nombre_desc':
            bicicletas = bicicletas.order_by('-marca', '-modelo')
    
    # Obtener marcas únicas para el filtro
    marcas = Bicicleta.objects.values_list('marca', flat=True).distinct()
    
    context = {
        'bicicletas': bicicletas,
        'marcas': marcas,
        'tipos': Bicicleta.TIPO_CHOICES,
        'filtros_actuales': {
            'tipo': tipo,
            'precio': precio_range,
            'marca': marca,
            'orden': orden
        }
    }
    
    return render(request, 'clientes/catalogo_bicicletas.html', context)

def detalles_bicicleta(request, id):
    bicicleta = get_object_or_404(Bicicleta, pk=id)
    return render(request, 'clientes/detalle_bicicletas.html', {'bicicleta': bicicleta})

def buscar_bicicletas(request):
    query = request.GET.get('search')
    if query:
        resultados = Bicicleta.objects.filter(
            Q(modelo__icontains=query) | 
            Q(tipo__icontains=query) | 
            Q(marca__icontains=query),
            Q(disponible_para_venta=True) | Q(disponible_para_arriendo=True),
            stock__gt=0
        )
    else:
        resultados = Bicicleta.objects.none()

    return render(request, 'clientes/resultados_busqueda.html', {'resultados': resultados})

@login_required
def ver_todas_ordenes(request):
    ordenes = OrdenCompra.objects.filter(usuario=request.user).prefetch_related('items').order_by('-fecha_creacion')
    ordenes_compra = OrdenCompra.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    reparaciones = Reparacion.objects.filter(cliente=request.user).order_by('-fecha_creacion')
    arriendos = Arriendo.objects.filter(cliente=request.user).order_by('-fecha_inicio')
    
    context = {
        'ordenes': ordenes,
        'ordenes_compra': ordenes_compra,
        'reparaciones': reparaciones,
        'arriendos': arriendos
    }
    
    return render(request, 'Clientes/ordenes.html', context)