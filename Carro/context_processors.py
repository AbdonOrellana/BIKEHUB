from .models import ItemCarro

def carrito(request):
    if request.user.is_authenticated:
        carrito_items = ItemCarro.objects.filter(usuario=request.user)
        total_carrito = sum(item.bicicleta.precio_venta * item.cantidad for item in carrito_items)
    else:
        carrito_items = []
        total_carrito = 0

    return {
        'carrito_items': carrito_items,
        'total_carrito': total_carrito
    }
