from django import forms
from .models import Inventario, Venta, VentaDetalle
from clientes.models import Bicicleta
from django.forms import inlineformset_factory

class BicicletaForm(forms.ModelForm):
    class Meta:
        model = Bicicleta
        fields = ['tipo', 'marca', 'modelo', 'descripcion', 'imagen', 'precio_por_dia', 'precio_venta', 'stock', 'disponible_para_venta', 'disponible_para_arriendo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'disponible_para_venta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'disponible_para_arriendo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'precio_por_dia': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        error_messages = {
            'precio_por_dia': {'min_value': 'El precio por día debe ser mayor que cero.'},
            'precio_venta': {'min_value': 'El precio de venta debe ser mayor que cero.'},
        }

    def clean(self):
        cleaned_data = super().clean()
        disponible_para_venta = cleaned_data.get('disponible_para_venta')
        disponible_para_arriendo = cleaned_data.get('disponible_para_arriendo')
        precio_venta = cleaned_data.get('precio_venta')
        precio_por_dia = cleaned_data.get('precio_por_dia')

        if disponible_para_venta and not precio_venta:
            self.add_error('precio_venta', 'Debe especificar un precio de venta.')

        if disponible_para_arriendo and not precio_por_dia:
            self.add_error('precio_por_dia', 'Debe especificar un precio por día para arriendo.')

        return cleaned_data
    
class InventarioForm(forms.ModelForm):
    bicicleta = forms.ModelChoiceField(
        queryset=Bicicleta.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cantidad = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        error_messages={'min_value': 'La cantidad debe ser al menos 1.'}
    )

    class Meta:
        model = Inventario
        fields = ['bicicleta', 'cantidad']

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad < 1:
            raise forms.ValidationError("La cantidad debe ser al menos 1.")
        return cantidad
    

class VentaForm(forms.ModelForm):
    cliente_rut = forms.CharField(
        max_length=12,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT Cliente (opcional)'}),
        help_text='Ingrese RUT del cliente si está disponible.'
    )
    class Meta:
        model = Venta
        fields = ['vendedor', 'cliente_rut']
        widgets = {
            'vendedor': forms.Select(attrs={'class': 'form-control'}),
        }
class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = VentaDetalle
        fields = ['bicicleta', 'cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super(VentaDetalleForm, self).__init__(*args, **kwargs)
        # Filtrar solo bicicletas con stock disponible
        self.fields['bicicleta'].queryset = Bicicleta.objects.filter(stock__gt=0)

VentaDetalleFormSet = inlineformset_factory(
    parent_model=Venta,
    model=VentaDetalle,
    form=VentaDetalleForm,  # Usar el formulario personalizado
    fields=('bicicleta', 'cantidad'),
    extra=1,
    can_delete=True,
    widgets={
        'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
    }
)