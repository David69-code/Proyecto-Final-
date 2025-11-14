from django import forms  # Importa el módulo de formularios de Django
from .models import Paciente  # Importa el modelo Paciente
from .models import Medico  # Importa el modelo Medico
from .models import Cita  # Importa el modelo Cita
from .models import Especialidad  # Importa el modelo Especialidad
from django.contrib.auth import get_user_model  # Permite obtener el modelo de usuario activo (personalizado o por defecto)
from django.utils import timezone  # Proporciona utilidades para manejar fechas y horas con zona horaria
import re  # Módulo para trabajar con expresiones regulares (validaciones)
from datetime import date  # Clase date para trabajar con fechas

# Obtiene el modelo de usuario activo (puede ser el modelo User por defecto o uno personalizado)
User = get_user_model()

# ==============================
# FORMULARIO PARA PACIENTE
# ==============================
class PacienteForm(forms.ModelForm):  # Formulario basado en el modelo Paciente
    class Meta:
        model = Paciente  # Modelo asociado al formulario
        fields = ['usuario', 'fecha_nacimiento', 'telefono', 'direccion']  # Campos visibles en el formulario
        # Widgets para personalizar los inputs HTML
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',  # Campo de tipo fecha
                'class': 'form-control',  # Clase Bootstrap
                'max': '9999-12-31',  # Límite máximo de fecha
                'required': False  # No obligatorio por defecto
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: 7777-7777',
                'required': False
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: Calle 5, San Salvador',
                'required': False
            }),
            'usuario': forms.Select(attrs={'class': 'form-select', 'required': False}),
        }
        # Mensajes personalizados de error
        error_messages = {
            'fecha_nacimiento': {'required': 'Debes agregar la fecha de nacimiento.'},
            'telefono': {'required': 'Debes agregar un número de teléfono.'},
            'direccion': {'required': 'Debes agregar la dirección.'},
            'usuario': {'required': 'Debes indicar el paciente.'},
        }

    def _init_(self, *args, **kwargs):  # Inicializador del formulario
        super()._init_(*args, **kwargs)
        # Muestra solo usuarios con rol paciente en el campo usuario
        self.fields['usuario'].queryset = User.objects.filter(rol='paciente')
        # Personaliza cómo se muestran los nombres en el select
        self.fields['usuario'].label_from_instance = lambda obj: f"{obj.username} ({obj.first_name} {obj.last_name})"

    def clean_fecha_nacimiento(self):  # Valida que la fecha no sea futura
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if fecha and fecha > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha

    def clean_telefono(self):  # Valida el formato del teléfono
        telefono = self.cleaned_data.get('telefono', '')
        if not re.match(r'^\d{4}-\d{4}$', telefono):
            raise forms.ValidationError("El teléfono debe tener el formato 0000-0000.")
        return telefono

    def clean_direccion(self):  # Valida la longitud mínima de la dirección
        direccion = self.cleaned_data.get('direccion', '').strip()
        if len(direccion) < 5:
            raise forms.ValidationError("La dirección debe tener al menos 5 caracteres.")
        return direccion

    def clean(self):  # Validación general de campos vacíos
        cleaned_data = super().clean()
        for field in ['usuario', 'fecha_nacimiento', 'telefono', 'direccion']:
            valor = cleaned_data.get(field)
            if not valor:
                self.add_error(field, f"El campo '{field}' no puede quedar vacío.")
        return cleaned_data

# ==============================
# FORMULARIO PARA MÉDICO
# ==============================
class MedicoForm(forms.ModelForm):  # Formulario para registrar o editar médicos
    class Meta:
        model = Medico
        required = True
        fields = ['usuario', 'matricula', 'telefono', 'especialidades']
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: M-12345'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 7777-7777'}),
            'especialidades': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
        }
        error_messages = {
            'matricula': {'required': 'Debes agregar el número de matrícula.'},
            'telefono': {'required': 'Debes agregar el número de teléfono.'},
            'especialidades': {'required': 'Debes indicar la especialidad.'},
            'usuario': {'required': 'Debes indicar el médico.'},
        }

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.filter(rol='medico')  # Muestra solo usuarios médicos
        self.fields['usuario'].label_from_instance = lambda obj: f"{obj.username} ({obj.first_name} {obj.last_name})"

    def clean_matricula(self):  # Valida formato de matrícula
        matricula = self.cleaned_data.get('matricula', '').strip()
        if not re.match(r'^[A-Za-z0-9\-]{4,15}$', matricula):
            raise forms.ValidationError("La matrícula debe tener entre 4 y 15 caracteres (letras, números o guiones).")
        return matricula

    def clean_telefono(self):  # Valida formato de teléfono
        telefono = self.cleaned_data.get('telefono', '')
        if not re.match(r'^\d{4}-\d{4}$', telefono):
            raise forms.ValidationError("El teléfono debe tener el formato 0000-0000.")
        return telefono

    def clean(self):  # Valida que no haya campos vacíos
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data

# ==============================
# FORMULARIO PARA CITA
# ==============================
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_hora', 'motivo', 'estado', 'paciente', 'medico']
        widgets = {
            'fecha_hora': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa brevemente el motivo de la cita'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'medico': forms.Select(attrs={'class': 'form-select'}),
        }
        error_messages = {
            'fecha_hora': {'required': 'Debes indicar la fecha y la hora.'},
            'motivo': {'required': 'Debes agregar el motivo.'},
            'estado': {'required': 'Debes indicar el estado de la cita.'},
            'paciente': {'required': 'Debes indicar el paciente.'},
            'medico': {'required': 'Debes indicar el médico.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].choices = [
            ('', '-- Seleccionar --'),
            ('pendiente', 'Pendiente'),
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada'),
            ('atendida', 'Atendida'),
        ]
        self.initial.pop('estado', None)


        # <-- ESTA ES LA PARTE QUE SOLUCIONA QUE SE MUESTRE LA FECHA AL EDITAR -->
       # ✅ Mostrar correctamente la fecha al editar
        if self.instance and self.instance.pk and self.instance.fecha_hora:
         fecha_local = timezone.localtime(self.instance.fecha_hora)
         self.fields['fecha_hora'].initial = fecha_local.strftime('%Y-%m-%dT%H:%M')

        self.fields['paciente'].queryset = Paciente.objects.select_related('usuario').all()  # Pacientes con sus usuarios
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.usuario.first_name} {obj.usuario.last_name}"
        self.fields['medico'].queryset = Medico.objects.select_related('usuario').all()  # Médicos con sus usuarios
        self.fields['medico'].label_from_instance = lambda obj: f"Dr(a). {obj.usuario.first_name} {obj.usuario.last_name}"

    def clean_fecha_hora(self):  # Valida que la fecha no sea pasada
        fecha_hora = self.cleaned_data.get('fecha_hora')
        if fecha_hora is None:
            raise forms.ValidationError("Debe ingresar una fecha y hora para la cita.")
        if fecha_hora < timezone.now():
            raise forms.ValidationError("No puedes registrar una cita en una fecha u hora pasada.")
        return fecha_hora
    
    # def clean_fecha_hora(self):
    #     fecha_hora = self.cleaned_data.get('fecha_hora')

    #     if fecha_hora is None:
    #         raise forms.ValidationError("Debe ingresar una fecha y hora para la cita.")

    #     ahora = timezone.now()

    # Si la fecha es antes del día actual → no permitir (ayer u antes)
        if fecha_hora.date() < ahora.date():
            raise forms.ValidationError("No puedes registrar una cita en días pasados.")

    # Si la fecha es hoy, pero la hora ya pasó → no permitir
        if fecha_hora.date() == ahora.date() and fecha_hora.time() <= ahora.time():
            raise forms.ValidationError("La hora ingresada ya ha pasado para el día de hoy.")

        return fecha_hora

    def clean_motivo(self):  # Valida que el motivo tenga longitud mínima
        motivo = self.cleaned_data.get('motivo', '').strip()
        if len(motivo) < 5:
            raise forms.ValidationError("El motivo de la cita debe tener al menos 5 caracteres.")
        return motivo

    def clean(self):  # Valida que no haya campos vacíos
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data

# ==============================
# FORMULARIO PARA ESPECIALIDAD
# ==============================
class EspecialidadForm(forms.ModelForm):  # Formulario para crear o modificar especialidades
    class Meta:
        model = Especialidad
        fields = ['nombre']
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Cardiología'})}
        error_messages = {'nombre': {'required': 'Debes agregar el nombre de la especialidad.'}}

    def clean_nombre(self):  # Valida nombre único y correcto
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        if not nombre.replace(" ", "").isalpha():
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        if Especialidad.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Ya existe una especialidad con este nombre.")
        return nombre

    def clean(self):  # Valida campos vacíos
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data

# ==============================
# FORMULARIO PARA PERFIL DE PACIENTE
# ==============================
class PacientePerfilForm(forms.ModelForm):  # Formulario para que el paciente edite su perfil
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Fecha de nacimiento')
    class Meta:
        model = Paciente
        fields = ['fecha_nacimiento', 'telefono', 'direccion']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 7777-7777'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Calle 5, San Salvador'}),
        }
        error_messages = {
            'fecha_nacimiento': {'required': 'Debes agregar la fecha de nacimiento.'},
            'telefono': {'required': 'Debes agregar el número de teléfono.'},
            'direccion': {'required': 'Debes agregar la dirección.'},
        }

    def clean_fecha_nacimiento(self):  # Valida que la fecha no sea futura
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if not fecha:
            raise forms.ValidationError("La fecha de nacimiento es obligatoria.")
        if fecha > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        return fecha

    def clean_telefono(self):  # Valida formato del teléfono
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not telefono:
            raise forms.ValidationError("El teléfono es obligatorio.")
        if not re.match(r'^\d{4}-\d{4}$', telefono):
            raise forms.ValidationError("El teléfono debe tener el formato 0000-0000.")
        return telefono

    def clean_direccion(self):  # Valida longitud de la dirección
        direccion = self.cleaned_data.get('direccion', '').strip()
        if not direccion:
            raise forms.ValidationError("La dirección no puede estar vacía.")
        if len(direccion) < 5:
            raise forms.ValidationError("La dirección debe tener al menos 5 caracteres.")
        return direccion

    def clean(self):  # Valida que no haya campos vacíos
        cleaned_data = super().clean()
        for campo, valor in cleaned_data.items():
            if not valor:
                raise forms.ValidationError(f"El campo '{campo}' no puede quedar vacío.")
        return cleaned_data