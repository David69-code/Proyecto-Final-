from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from gestion_citas.models import Paciente, Cita, Medico
from django.utils import timezone
import re

# ==============================
# FORMULARIO DE REGISTRO DE PACIENTE
# ==============================
class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Juan'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Pérez'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise forms.ValidationError("El nombre es obligatorio.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', first_name):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise forms.ValidationError("El apellido es obligatorio.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', last_name):
            raise forms.ValidationError("El apellido solo puede contener letras y espacios.")
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError("El nombre de usuario es obligatorio.")
        if len(username) < 4:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 4 caracteres.")
        if re.search(r'\s', username):
            raise forms.ValidationError("El nombre de usuario no puede contener espacios.")
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError("Ingrese un correo electrónico válido.")
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        if not password:
            raise forms.ValidationError("La contraseña es obligatoria.")
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.match(r'^[A-Za-z]+$', password):
            raise forms.ValidationError("La contraseña solo puede contener letras (mayúsculas y minúsculas).")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        for campo, valor in cleaned_data.items():
            if valor in [None, '']:
                self.add_error(campo, f"El campo '{campo}' es obligatorio.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'paciente'
        if commit:
            user.save()
            Paciente.objects.create(usuario=user)
        return user

# ==============================
# FORMULARIO DE REGISTRO DE MÉDICO
# ==============================
class MedicoRegistroForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError("El nombre de usuario solo puede contener letras, números y guiones bajos")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        for campo in ['username', 'first_name', 'last_name', 'email','password1','password2']:
            if not cleaned_data.get(campo):
                self.add_error(campo, 'Este campo es obligatorio')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.rol = 'medico'
        user.is_active = True
        if commit:
            user.save()
        return user

# ==============================
# FORMULARIO DE CITA PARA PACIENTE
# ==============================
class PacienteCitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['medico', 'fecha_hora', 'motivo']
        widgets = {
            'medico': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe el motivo de tu cita'}),
        }

    def clean_medico(self):
        medico = self.cleaned_data.get('medico')
        if not medico:
            raise forms.ValidationError("Debes seleccionar un médico.")
        return medico

    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data.get('fecha_hora')
        if not fecha_hora:
            raise forms.ValidationError("Debes seleccionar la fecha y hora de la cita.")
        if fecha_hora < timezone.now():
            raise forms.ValidationError("La fecha y hora no puede ser en el pasado.")
        return fecha_hora

    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo', '').strip()
        if not motivo:
            raise forms.ValidationError("Debes indicar el motivo de la cita.")
        if len(motivo) < 5:
            raise forms.ValidationError("El motivo debe tener al menos 5 caracteres.")
        return motivo
