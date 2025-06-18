from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Venta
from .forms import InventarioForm, VentaDetalleFormSet, VentaForm, BicicletaForm

def gestion_bicicletas_view(request):
    return render(request, 'tecnicos_vendedores/gestion_bicicletas.html')

def agregar_bicicleta(request):
    if request.method == 'POST':
        form = BicicletaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bicicleta agregada correctamente.')
            return redirect('inventario_exito')  # Cambia esto por la URL a donde quieres redirigir tras el éxito
    else:
        form = BicicletaForm()

    return render(request, 'tecnicos_vendedores/agregar_bicicleta.html', {'form': form})

@login_required
def gestion_inventario(request):
    if request.method == 'POST':
        inventario_form = InventarioForm(request.POST)
        if inventario_form.is_valid():
            inventario_form.save()
            messages.success(request, "Inventario actualizado con éxito.")
            return redirect('inventario_exito')
        else:
            messages.error(request, "Por favor, corrija los errores en el formulario.")
    else:
        inventario_form = InventarioForm()

    return render(request, 'tecnicos_vendedores/gestion_inventario.html', {'inventario_form': inventario_form})

@login_required
def registrar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        formset = VentaDetalleFormSet(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)  # Crear la instancia de Venta, pero no guardarla aún

            formset = VentaDetalleFormSet(request.POST, instance=venta)
            if formset.is_valid():
                venta.save()  # Guardar la Venta primero para que tenga un ID y pueda asociarse con VentaDetalle
                formset.save()  # Guardar el formset ahora que Venta tiene un ID

                # Actualizar el stock de cada bicicleta vendida
                for form in formset.cleaned_data:
                    if form and not form.get('DELETE', False):  # Asegúrate de que el formulario no está marcado para eliminación
                        bicicleta = form['bicicleta']
                        cantidad = form['cantidad']
                        if bicicleta.stock >= cantidad:  # Verificar que hay suficiente stock
                            bicicleta.stock -= cantidad
                            bicicleta.save()
                        else:
                            messages.error(request, f"No hay suficiente stock para la bicicleta {bicicleta}")
                            venta.delete()  # Opción para eliminar la venta si no se puede cumplir con el stock
                            return redirect('registrar_venta')  # Redirigir para intentar de nuevo

                # Recalcular el total de la venta después de guardar los detalles
                venta.total = sum(item.subtotal for item in venta.detalles.all())
                venta.save()

                messages.success(request, "Venta registrada con éxito.")
                return redirect('venta_exito')  # Asegúrate de que 'venta_exito' es el nombre correcto de tu URL de éxito
            else:
                messages.error(request, "Por favor, corrija los errores en los detalles de la venta.")
        else:
            messages.error(request, "Por favor, corrija los errores en el formulario de venta.")
    else:
        form = VentaForm()
        formset = VentaDetalleFormSet(instance=Venta())

    return render(request, 'tecnicos_vendedores/registrar_venta.html', {'form': form, 'formset': formset})

def inventario_exito_view(request):
    return render(request, 'tecnicos_vendedores/inventario_exito.html')

def venta_exito_view(request):
    return render(request, 'tecnicos_vendedores/venta_exito.html')