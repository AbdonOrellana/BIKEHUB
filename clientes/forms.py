from django.utils import timezone
from django.utils.timezone import now
from django import forms
import datetime
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Arriendo, Reparacion
from tecnicos_vendedores.models import ReservaTecnico


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ('email', 'first_name', 'last_name', 'apellido_materno', 'telefono', 'direccion', 'password1', 'password2')
        widgets = {
            'email': forms.TextInput(attrs={'placeholder':'ejemplo@gmail.com'}),
            'direccion': forms.Textarea(attrs={'rows': 1}),
            'telefono': forms.TextInput(attrs={'placeholder': '12345678901'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Cliente.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("El nombre solo puede contener letras.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("El apellido paterno solo puede contener letras.")
        return last_name

    def clean_apellido_materno(self):
        apellido_materno = self.cleaned_data.get('apellido_materno')
        if not apellido_materno.isalpha():
            raise ValidationError("El apellido materno solo puede contener letras.")
        return apellido_materno

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if len(telefono) != 11 or not telefono.isdigit():
            raise ValidationError("El número de teléfono debe contener 11 dígitos y solo números.")
        return telefono

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        try:
            validate_password(password1, self.instance)
        except ValidationError as e:
            self.add_error('password1', e)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data



class ArriendoForm(forms.ModelForm):
    class Meta:
        model = Arriendo
        fields = ['bicicleta', 'fecha_inicio', 'fecha_fin', 'forma_pago', 'costo_arriendo', 'deposito_garantia', 'costo_total']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'forma_pago': forms.Select(attrs={'class': 'form-control'}),
            'costo_arriendo': forms.NumberInput(attrs={'class': 'form-control'}),
            'deposito_garantia': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        # Convertir datetime.datetime a datetime.date si es necesario
        if isinstance(fecha_inicio, datetime.datetime):
            fecha_inicio = fecha_inicio.date()
        if isinstance(fecha_fin, datetime.datetime):
            fecha_fin = fecha_fin.date()

        today = timezone.localdate()  # Asegurarse de que 'today' es un objeto date

        if fecha_inicio and fecha_fin:
            if fecha_inicio < today:
                raise ValidationError("La fecha de inicio no puede ser en el pasado.")
            if fecha_fin <= fecha_inicio:
                raise ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    

class ReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields = ['marca_bicicleta', 'tipo_bicicleta', 'descripcion_problema', 'reserva_tecnico']
        widgets = {
            'marca_bicicleta': forms.TextInput(attrs={'class': 'input bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}),
            'tipo_bicicleta': forms.Select(attrs={'class': 'form-select block w-full mt-1'}),
            'descripcion_problema': forms.Textarea(attrs={'class': 'textarea bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}),
            'reserva_tecnico': forms.Select(attrs={'class': 'form-select block w-full mt-1'})
        }

    def __init__(self, *args, **kwargs):
        super(ReparacionForm, self).__init__(*args, **kwargs)
        # Filtra los horarios de técnicos (esto ya estaba bien)
        self.fields['reserva_tecnico'].queryset = ReservaTecnico.objects.filter(esta_disponible=True, fecha_inicio__gte=now()).order_by('fecha_inicio')
        self.fields['reserva_tecnico'].label = "Horario del Técnico"
        
        # --- LÍNEA AÑADIDA ---
        # Añade una opción vacía al principio del menú de tipo de bicicleta.
        choices = list(self.fields['tipo_bicicleta'].choices)
        choices.insert(0, ('', 'Seleccione un tipo de bicicleta'))
        self.fields['tipo_bicicleta'].choices = choices

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50',
        'placeholder': 'nombre@ejemplo.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50',
        'placeholder': '••••••••'
    }))