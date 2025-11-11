# Importa el módulo de formularios de Django
from django import forms

# Importa el formulario de creación de usuarios que incluye validación de contraseña
from django.contrib.auth.forms import UserCreationForm

# Importa el modelo Usuario personalizado
from .models import Usuario

# Importa modelos de la app gestion_citas
from gestion_citas.models import Paciente, Cita, Medico

# Proporciona utilidades para trabajar con fechas y horas considerando zona horaria
from django.utils import timezone

# Permite lanzar errores de validación personalizados
from django.core.exceptions import ValidationError

# Permite validar contraseñas según las reglas de Django
from django.contrib.auth.password_validation import validate_password

# Módulo de expresiones regulares, útil para validar cadenas
import re


# ==============================
# FORMULARIO DE REGISTRO DE PACIENTE
# ==============================
class RegistroForm(UserCreationForm):  # Hereda de UserCreationForm para registrar usuarios
    # Campo para el nombre con placeholder y estilo Bootstrap
    first_name = forms.CharField(
        max_length=30,  # Longitud máxima 30
        required=False,  # Inicialmente no obligatorio (se valida después)
        label='Nombre',  # Etiqueta visible
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Juan'})  # Estilo y placeholder
    )
    # Campo para el apellido con placeholder y estilo Bootstrap
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Pérez'})
    )

    class Meta:  # Configuración interna del formulario
        model = Usuario  # Modelo asociado
        required = True
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']  # Campos visibles
        widgets = {  # Personalización de los inputs
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        }
        error_messages = {  # Mensajes de error personalizados
            'username': {'required': "El Usuario es obligatorio."}
        }

    # 🔹 Guarda el usuario y crea automáticamente el perfil de Paciente
    def save(self, commit=True):
        user = super().save(commit=False)  # Llama al save de UserCreationForm pero no lo guarda aún
        user.rol = 'paciente'  # Asigna el rol 'paciente' al usuario
        if commit:  # Si se indica guardar en la base de datos
            user.save()  # Guarda el usuario
            Paciente.objects.create(usuario=user)  # Crea automáticamente un perfil de Paciente
        return user  # Retorna el usuario guardado

    # ==============================
    # VALIDACIONES DE CAMPOS
    # ==============================
    def clean_first_name(self):  # Valida el campo nombre
        first_name = self.cleaned_data.get('first_name', '').strip()  # Obtiene el valor y elimina espacios
        if not first_name:  # Si está vacío
            raise forms.ValidationError("El nombre es obligatorio.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', first_name):  # Solo letras y espacios
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        if len(first_name) < 2:  # Mínimo 2 caracteres
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return first_name  # Retorna el valor limpio

    def clean_last_name(self):  # Valida el apellido
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise forms.ValidationError("El apellido es obligatorio.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', last_name):
            raise forms.ValidationError("El apellido solo puede contener letras y espacios.")
        if len(last_name) < 2:
            raise forms.ValidationError("El apellido debe tener al menos 2 caracteres.")
        return last_name

    def clean_username(self):  # Valida el nombre de usuario
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise forms.ValidationError("El nombre de usuario es obligatorio.")
        if len(username) < 4:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 4 caracteres.")
        if re.search(r'\s', username):  # No se permiten espacios
            raise forms.ValidationError("El nombre de usuario no puede contener espacios.")
        if Usuario.objects.filter(username=username).exists():  # Nombre de usuario único
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):  # Valida correo electrónico
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):  # Formato válido
            raise forms.ValidationError("Ingrese un correo electrónico válido.")
        if Usuario.objects.filter(email=email).exists():  # Email único
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_password1(self):  # Valida la contraseña
        password = self.cleaned_data.get('password1', '')
        if not password:
            raise forms.ValidationError("La contraseña es obligatoria.")
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password):  # Al menos una mayúscula
            raise forms.ValidationError("Debe contener al menos una letra mayúscula.")
        if not re.search(r'[a-z]', password):  # Al menos una minúscula
            raise forms.ValidationError("Debe contener al menos una letra minúscula.")
        if not re.search(r'\d', password):  # Al menos un número
            raise forms.ValidationError("Debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # Al menos un carácter especial
            raise forms.ValidationError("Debe contener al menos un carácter especial (!@#$...).")
        return password

    def clean(self):  # Validación general del formulario
        cleaned_data = super().clean()  # Llama al clean del padre
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Validación de coincidencia de contraseñas
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        # Validar que ningún campo quede vacío
        for campo, valor in cleaned_data.items():
            if valor in [None, '']:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data


# ==============================
# FORMULARIO DE CITA PARA PACIENTE
# ==============================
class PacienteCitaForm(forms.ModelForm):
    class Meta:
        model = Cita  # Modelo asociado
        required = True
        fields = ['medico', 'fecha_hora', 'motivo']  # Campos visibles (paciente y estado se asignan automáticamente)
        widgets = {  # Personalización de inputs
            'medico': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe el motivo de tu cita'}),
        }
        error_messages = {  # Mensajes de error
            'medico': {'required': 'Debes seleccionar un médico.'},
            'fecha_hora': {'required': 'Debes seleccionar la fecha y hora de la cita.'},
            'motivo': {'required': 'Debes indicar el motivo de la cita.'},
        }

    def clean_medico(self):  # Validación del campo médico
        medico = self.cleaned_data.get('medico')
        if not medico:
            raise forms.ValidationError("Debes seleccionar un médico.")
        return medico

    def clean_fecha_hora(self):  # Validación de fecha y hora
        fecha_hora = self.cleaned_data.get('fecha_hora')
        if not fecha_hora:
            raise forms.ValidationError("Debes seleccionar la fecha y hora de la cita.")
        if fecha_hora < timezone.now():  # No puede ser en el pasado
            raise forms.ValidationError("La fecha y hora de la cita no puede ser en el pasado.")
        return fecha_hora

    def clean_motivo(self):  # Validación de motivo
        motivo = self.cleaned_data.get('motivo', '').strip()
        if not motivo:
            raise forms.ValidationError("Debes indicar el motivo de la cita.")
        if len(motivo) < 5:
            raise forms.ValidationError("El motivo debe tener al menos 5 caracteres.")
        return motivo


# ==============================
# FORMULARIO DE REGISTRO DE MÉDICO
# ==============================
class MedicoRegistroForm(forms.ModelForm):
    # Campos de contraseña personalizados
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = Usuario  # Modelo asociado
        fields = ['username', 'first_name', 'last_name', 'email']  # Campos visibles
        labels = {  # Etiquetas de campos
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }
        widgets = {  # Personalización de inputs
            'username': forms.TextInput(attrs={'required': True}),
            'first_name': forms.TextInput(attrs={'required': False}),
            'last_name': forms.TextInput(attrs={'required': False}),
            'email': forms.EmailInput(attrs={'required': False}),
        }
        error_messages = {  # Mensajes de error
            'username': {'unique': 'Este nombre de usuario ya existe'},
            'email': {'invalid': 'Ingrese un correo válido'}
        }

    def clean_username(self):  # Valida que el username tenga solo caracteres válidos
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError("El nombre de usuario solo puede contener letras, números y guiones bajos")
        return username

    def clean_password2(self):  # Valida coincidencia de contraseñas
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def clean(self):  # Validación general de campos obligatorios
        cleaned_data = super().clean()
        campos_obligatorios = ['username', 'first_name', 'last_name', 'email','password1','password2']
        for campo in campos_obligatorios:
            valor = cleaned_data.get(campo)
            if not valor:
                self.add_error(campo, 'Este campo es obligatorio')
        return cleaned_data

    def save(self, commit=True):  # Guarda el médico
        user = super().save(commit=False)  # No guarda aún
        user.set_password(self.cleaned_data["password1"])  # Hashea la contraseña
        user.rol = 'medico'  # Fuerza el rol de médico
        user.is_active = True  # Activa el usuario
        if commit:  # Si commit=True
            user.save()  # Guarda en la base de datos
        return user  # Retorna el usuario guardado
