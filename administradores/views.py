from django.db.models import Q, Sum, Case, When, IntegerField
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta
from clientes.models import Arriendo
from Carro.models import Orden
from django.utils.safestring import mark_safe
import plotly.express as px
import plotly.io as pio
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from clientes.models import Arriendo, Reparacion
from tecnicos_vendedores.models import ReservaTecnico, Venta
from django.db.models import Prefetch
from .forms import TecnicoUserForm, TecnicoForm, VendedorUserForm, VendedorForm
from django.contrib.auth import get_user_model
User = get_user_model()

def es_admin(user):
    return user.groups.filter(name='Administradores').exists()

@login_required
@user_passes_test(es_admin)
def ganancias_semanales(request):
    hoy = timezone.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    
    ventas = Orden.objects.filter(
        fecha_creacion__date__range=[inicio_semana, fin_semana]
    ).aggregate(total_ventas=Sum('total'))['total_ventas'] or 0
    
    arriendos = Arriendo.objects.filter(
        Q(fecha_inicio__date__lte=fin_semana, fecha_fin__date__gte=inicio_semana),
        estado='completado'
    ).aggregate(total_arriendos=Sum('costo_arriendo'))['total_arriendos'] or 0
    
    total = ventas + arriendos
    
    fig = px.bar(
        x=['Ventas', 'Arriendos', 'Total'],
        y=[ventas, arriendos, total],
        labels={'x': 'Categoría', 'y': 'Total'},
        title='Ganancias Semanales'
    )
    grafico = mark_safe(pio.to_html(fig, full_html=False))
    
    return render(request, 'administradores/ganancias_semanales.html', {
        'grafico': grafico,
        'ventas': ventas,
        'arriendos': arriendos,
        'total': total
    })


@login_required
@user_passes_test(es_admin)
def ganancias_mensuales(request):
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    fin_mes = (inicio_mes + timedelta(days=44)).replace(day=1) - timedelta(days=1)
    
    ventas = Orden.objects.filter(
        fecha_creacion__date__range=[inicio_mes, fin_mes]
    ).aggregate(total_ventas=Sum('total'))['total_ventas'] or 0
    
    arriendos = Arriendo.objects.filter(
        Q(fecha_inicio__date__lte=fin_mes, fecha_fin__date__gte=inicio_mes),
        estado='completado'
    ).aggregate(total_arriendos=Sum('costo_arriendo'))['total_arriendos'] or 0
    
    total = ventas + arriendos
    
    fig = px.bar(
        x=['Ventas', 'Arriendos', 'Total'],
        y=[ventas, arriendos, total],
        labels={'x': 'Categoría', 'y': 'Total'},
        title='Ganancias Mensuales'
    )
    grafico = mark_safe(pio.to_html(fig, full_html=False))
    
    return render(request, 'administradores/ganancias_mensuales.html', {
        'grafico': grafico,
        'ventas': ventas,
        'arriendos': arriendos,
        'total': total
    })

@login_required
@user_passes_test(es_admin)
def dashboard(request):
    # Asumiendo que los modelos tienen relaciones y campos necesarios para mostrar detalles completos
    compras_recientes = Orden.objects.prefetch_related('items').order_by('-fecha_creacion')[:10]
    for orden in compras_recientes:
        for item in orden.items.all():
            item.subtotal = item.precio * item.cantidad  # Calcula el subtotal y lo asigna como atributo
    ventas_recientes = Venta.objects.prefetch_related('detalles').select_related('vendedor').order_by('-fecha')[:10]
    arriendos_recientes = Arriendo.objects.select_related('cliente', 'bicicleta').order_by('-fecha_inicio')[:10]
    reparaciones_recientes = Reparacion.objects.select_related('cliente').prefetch_related(
        Prefetch('reserva_tecnico', queryset=ReservaTecnico.objects.select_related('tecnico'))
    ).order_by('-fecha_creacion')[:10]
    context = {
        'compras_recientes': compras_recientes,
        'ventas_recientes': ventas_recientes,
        'arriendos_recientes': arriendos_recientes,
        'reparaciones_recientes': reparaciones_recientes,
    }
    return render(request, 'administradores/admin_dashboard.html', context)

@login_required
@user_passes_test(es_admin)
def registrar_tecnico(request):
    if request.method == 'POST':
        user_form = TecnicoUserForm(request.POST)
        tecnico_form = TecnicoForm(request.POST)
        if user_form.is_valid() and tecnico_form.is_valid():
            user = user_form.save()  # Guarda el usuario y lo retorna
            tecnico = tecnico_form.save(commit=False)  # Crea una instancia de Tecnico pero no la guarda aún
            tecnico.usuario = user  # Asigna el usuario recién creado al técnico
            tecnico.save()  # Ahora guarda el técnico con el usuario asociado
            return redirect('administradores/admin_dashboard')  # Redirecciona a 'index' tras el éxito
    else:
        user_form = TecnicoUserForm()  # Formulario para datos del usuario
        tecnico_form = TecnicoForm()  # Formulario para datos específicos del técnico

    return render(request, 'administradores/registrar_tecnicos.html', {
        'user_form': user_form,
        'tecnico_form': tecnico_form
    })

def registrar_vendedor(request):
    if request.method == 'POST':
        user_form = VendedorUserForm(request.POST)
        vendedor_form = VendedorForm(request.POST)
        if user_form.is_valid() and vendedor_form.is_valid():
            user = user_form.save()  # Guarda el usuario
            vendedor = vendedor_form.save(commit=False)  # Crea una instancia de Vendedor pero no la guarda aún
            vendedor.usuario = user  # Asocia el usuario recién creado con el vendedor
            vendedor.save()  # Guarda el vendedor con el usuario asociado
            return redirect('administradores/admin_dashboard') # Redirecciona a 'index' tras el éxito
    else:
        user_form = VendedorUserForm()  # Formulario para datos del usuario
        vendedor_form = VendedorForm()  # Formulario para datos específicos del vendedor

    return render(request, 'administradores/registrar_vendedores.html', {
        'user_form': user_form,
        'vendedor_form': vendedor_form
    })