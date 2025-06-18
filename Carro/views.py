from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseBadRequest
from .models import Bicicleta, ItemCarro, Orden, OrdenItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

def agregar_a_carrito(request, bicicleta_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Asegúrate de tener una URL con el nombre 'login'

    bicicleta = get_object_or_404(Bicicleta, id=bicicleta_id)
    item, creado = ItemCarro.objects.get_or_create(
        bicicleta=bicicleta,
        usuario=request.user,
        defaults={'cantidad': 1}
    )
    if not creado:
        item.cantidad += 1
        item.save()
        messages.success(request, f'{bicicleta.modelo} cantidad incrementada en el carrito.')
    else:
        messages.success(request, f'{bicicleta.modelo} agregado al carrito.')

    return redirect('catalogo_bicicletas')

@login_required
def checkout(request):
    items = ItemCarro.objects.filter(usuario=request.user)
    if not items.exists():
        messages.error(request, "¡Debes agregar productos al carrito antes de proceder al pago!")
        return redirect('catalogo_bicicletas')
    items_data = []
    total_carrito = 0
    for item in items:
        total_price = item.bicicleta.precio_venta * item.cantidad
        total_carrito += total_price
        items_data.append({
            'id': item.id,  
            'bicicleta': item.bicicleta,
            'cantidad': item.cantidad,
            'total_price': total_price,
        })
    context = {
        'items': items_data,
        'items_count': len(items),
        'total_carrito': total_carrito,
        'total_final': total_carrito,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'Carro/checkout.html', context)

@login_required
def actualizar_carrito(request, item_id):
    item = get_object_or_404(ItemCarro, id=item_id, usuario=request.user)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'incrementar':
            item.cantidad += 1
        elif accion == 'decrementar':
            if item.cantidad > 1:
                item.cantidad -= 1
            else:
                item.delete()
                return redirect('Carro:checkout')
        item.save()
        return redirect('Carro:checkout')
    return HttpResponseBadRequest("Invalid request")

@login_required
def eliminar_de_carrito(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ItemCarro, id=item_id, usuario=request.user)
        item.delete()
        return redirect('Carro:checkout')
    return HttpResponseBadRequest("Invalid request")

@login_required
def procesar_pago(request):
    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        if metodo_pago not in ['debito', 'credito', 'transferencia']:
            return HttpResponseBadRequest("Método de pago inválido")

        items = ItemCarro.objects.filter(usuario=request.user)
        if not items:
            messages.error(request, "No hay artículos en el carrito.")
            return redirect('Carro:checkout')

        # Crea una nueva orden con el estado inicial 'Pendiente de Pago'
        orden = Orden.objects.create(
            usuario=request.user,
            estado='Pendiente de Pago'  # CAMBIO: Estado inicial actualizado
        )

        total = 0

        for item in items:
            bicicleta = item.bicicleta
            if bicicleta.stock < item.cantidad:
                messages.error(request, f"Stock insuficiente para {bicicleta.modelo}.")
                # (Opcional) Devolver los items al carrito si la orden falla no es trivial,
                # por ahora lo dejamos así y el usuario tendría que volver a añadir.
                orden.delete() # Borra la orden creada si falla
                return redirect('Carro:checkout')
            
            bicicleta.stock -= item.cantidad
            bicicleta.save()

            OrdenItem.objects.create(
                orden=orden,
                bicicleta=bicicleta,
                precio=bicicleta.precio_venta,
                cantidad=item.cantidad
            )
            total += item.bicicleta.precio_venta * item.cantidad
            
            item.delete()

        orden.total = total
        orden.save()

        # CAMBIO: Mensaje de éxito actualizado
        messages.success(request, '¡Pedido realizado con éxito! Tu orden está pendiente hasta que se confirme el pago.')
        
        # CAMBIO: Redirección a la página de inicio
        return redirect('home')
    
    return HttpResponseBadRequest("Invalid request")

# La siguiente vista ya no es necesaria, la puedes borrar o dejar comentada
# def procesando_compra(request):
#     return render(request, 'Carro/procesando_compra.html')