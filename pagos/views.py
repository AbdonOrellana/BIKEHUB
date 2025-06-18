from django.shortcuts import render
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pago
from Carro.models import ItemCarro, Orden
import logging
from clientes.models import Arriendo

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

@login_required
def procesar_pago(request):
    items_carro = ItemCarro.objects.filter(usuario=request.user)
    if not items_carro.exists():
        return redirect('carro')
    
    monto_total = sum(item.bicicleta.precio_venta * item.cantidad for item in items_carro)
    
    context = {
        'items_carro': items_carro,
        'monto_total': monto_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'pagos/pago.html', context)

@login_required
def crear_pago(request):
    items_carro = ItemCarro.objects.filter(usuario=request.user)
    if not items_carro.exists():
        return redirect('carro')
    
    monto_total = sum(item.bicicleta.precio_venta * item.cantidad for item in items_carro)
    
    try:
        # Crear la orden antes del pago
        orden = Orden.objects.create(
            usuario=request.user,
            estado='Pendiente de Pago',
            total=monto_total
        )
        for item in items_carro:
            orden.items.create(
                bicicleta=item.bicicleta,
                precio=item.bicicleta.precio_venta,
                cantidad=item.cantidad
            )
        # Crear el intento de pago en Stripe
        intent = stripe.PaymentIntent.create(
            amount=int(monto_total * 100),  # Stripe usa centavos
            currency='mxn',
            metadata={'user_id': request.user.id, 'orden_id': orden.id}
        )
        # Crear el registro de pago en nuestra base de datos
        pago = Pago.objects.create(
            usuario=request.user,
            monto_total=monto_total,
            stripe_payment_id=intent.id,
            orden=orden
        )
        pago.items_carro.set(items_carro)
        return JsonResponse({
            'clientSecret': intent.client_secret,
            'pago_id': pago.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def exito(request):
    return render(request, 'pagos/exito.html')

@csrf_exempt
def webhook_stripe(request):
    logger = logging.getLogger(__name__)

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    if not sig_header:
        logger.error("No se recibió HTTP_STRIPE_SIGNATURE")
        return JsonResponse({'error': 'No signature header'}, status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Payload inválido: {e}")
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Firma inválida: {e}")
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    logger.info(f"Webhook recibido: {event['type']}")

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        logger.info(f"payment_intent recibido: {payment_intent['id']}")
        logger.info(f"Metadata del payment_intent: {payment_intent.get('metadata', {})}")
        
        try:
            pago = Pago.objects.get(stripe_payment_id=payment_intent['id'])
            pago.estado = 'completado'
            pago.save()
            logger.info(f"Pago {pago.id} actualizado a completado")
            
            # Verificar si es un pago de arriendo o compra
            metadata = payment_intent.get('metadata', {})
            tipo_pago = metadata.get('tipo')
            logger.info(f"Tipo de pago: {tipo_pago}")
            
            if tipo_pago == 'arriendo':
                # Actualizar el arriendo
                arriendo_id = metadata.get('arriendo_id')
                if arriendo_id:
                    try:
                        arriendo = Arriendo.objects.get(id=arriendo_id)
                        arriendo.estado = 'completado'
                        arriendo.save()
                        logger.info(f"Arriendo {arriendo_id} actualizado a completado")
                    except Arriendo.DoesNotExist:
                        logger.error(f"No se encontró Arriendo con id={arriendo_id}")
            else:
                # Actualizar la orden asociada (pago de compra)
                if pago.orden:
                    pago.orden.estado = 'Pedido Confirmado'
                    pago.orden.save()
                    pago.items_carro.all().delete()
                    logger.info(f"Orden {pago.orden.id} confirmada")
            
            logger.info(f"Pago {pago.id} actualizado a completado")
        except Pago.DoesNotExist:
            logger.error(f"No se encontró Pago con stripe_payment_id={payment_intent['id']}")
            return JsonResponse({'error': 'Pago no encontrado'}, status=404)
        except Exception as e:
            logger.error(f"Error actualizando el pago: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'status': 'success'})

@login_required
@csrf_exempt
def crear_pago_arriendo(request):
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_method_id = data.get('payment_method_id')
        # Buscar el arriendo pendiente del usuario
        arriendo = Arriendo.objects.filter(cliente=request.user, estado='pendiente').order_by('-id').first()
        if not arriendo:
            return JsonResponse({'error': 'No hay arriendo pendiente para pagar.'}, status=400)
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(arriendo.costo_total * 100),  # Stripe usa centavos
                currency='mxn',
                payment_method=payment_method_id,
                metadata={'user_id': request.user.id, 'arriendo_id': arriendo.id, 'tipo': 'arriendo'},
                automatic_payment_methods={
                    "enabled": True,
                    "allow_redirects": "never"
                }
            )
            
            # Crear registro de pago para arriendo
            pago = Pago.objects.create(
                usuario=request.user,
                monto_total=arriendo.costo_total,
                stripe_payment_id=intent.id,
                estado='pendiente'
            )
            
            return JsonResponse({'clientSecret': intent.client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def confirmar_pago_exitoso(request):
    """Vista para confirmar pagos exitosos desde el frontend"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        payment_intent_id = data.get('payment_intent_id')
        
        try:
            pago = Pago.objects.get(stripe_payment_id=payment_intent_id)
            pago.estado = 'completado'
            pago.save()
            
            # Verificar si es un pago de arriendo o compra
            if pago.orden:
                # Es un pago de compra
                pago.orden.estado = 'Pedido Confirmado'
                pago.orden.save()
                pago.items_carro.all().delete()
            else:
                # Es un pago de arriendo - buscar en metadata
                try:
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                    metadata = payment_intent.get('metadata', {})
                    arriendo_id = metadata.get('arriendo_id')
                    if arriendo_id:
                        arriendo = Arriendo.objects.get(id=arriendo_id)
                        arriendo.estado = 'completado'
                        arriendo.save()
                except Exception as e:
                    pass  # Si no se puede actualizar el arriendo, continuar
            
            return JsonResponse({'success': True})
        except Pago.DoesNotExist:
            return JsonResponse({'error': 'Pago no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
