from django import forms
from tecnicos_vendedores.models import Tecnico, Vendedor
from clientes.models import Cliente  # Importa el modelo personalizado
from django.contrib.auth.forms import UserCreationForm

# Actualizar UserCreationForm para usar el modelo Cliente
class UserCreationFormCustom(UserCreationForm):
    class Meta:
        model = Cliente  # Usar Cliente, el modelo de usuario personalizado
        fields = ['username', 'email', 'password1', 'password2']

# Formulario para técnicos que incluye campos del usuario y campos específicos del técnico
class TecnicoUserForm(UserCreationFormCustom):
    class Meta(UserCreationFormCustom.Meta):
        fields = UserCreationFormCustom.Meta.fields  # Heredar los campos del formulario personalizado

class TecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnico
        fields = ['nombre', 'especialidad', 'experiencia']

# Formulario para vendedores que incluye campos del usuario y campos específicos del vendedor
class VendedorUserForm(UserCreationFormCustom):
    class Meta(UserCreationFormCustom.Meta):
        fields = UserCreationFormCustom.Meta.fields  # Heredar los campos del formulario personalizado

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = ['nombre', 'fecha_contratacion']