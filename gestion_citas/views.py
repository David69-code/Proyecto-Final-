from django.shortcuts import render # Permite renderizar plantillas HTML y devolverlas como respuesta HTTP
from django.views.generic import ListView, CreateView, UpdateView, DeleteView # Vistas genéricas de Django para listar, crear, actualizar y eliminar registros
from .models import Paciente, Medico, Cita, Especialidad # Importa los modelos definidos en el mismo módulo para ser usados en las vistas
from django.contrib import messages # Sistema de mensajes de Django (usado para mostrar notificaciones al usuario)
from django.db.models import Q # Permite construir consultas complejas con operadores lógicos

from django.urls import reverse_lazy # Genera URLs de forma perezosa, útil para evitar dependencias circulares


from .forms import PacienteForm # Formulario del modelo Paciente
from .forms import MedicoForm # Formulario del modelo Medico
from .forms import CitaForm # Formulario del modelo Cita
from .forms import EspecialidadForm # Formulario del modelo Especialidad
from core.mixins import RolRequiredMixin # Mixin personalizado para restringir acceso según el rol del usuario


# ===============================
# VISTAS PARA ESPECIALIDAD
# ===============================


class EspecialidadListView(RolRequiredMixin, ListView): # Muestra la lista de especialidades disponibles
 model = Especialidad # Especifica el modelo que se listará
 rol_permitido = 'admin' # Solo los usuarios con rol 'admin' pueden acceder a esta vista
 template_name = 'especialidad/especialidad-list.html' # Plantilla HTML a utilizar
 context_object_name = 'especialidades' # Nombre de la variable que contendrá los datos en la plantilla
 def get_queryset(self):
        qs = super().get_queryset()
        filtro = self.request.GET.get('buscar', '')
        if filtro:
            qs = qs.filter(nombre__icontains=filtro)
        return qs

 def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro'] = self.request.GET.get('buscar', '')
        return context


class EspecialidadCreateView(RolRequiredMixin, CreateView): # Permite crear una nueva especialidad
 model = Especialidad # Modelo al que pertenece el formulario
 rol_permitido = 'admin' # Solo los administradores pueden crear especialidades
 form_class = EspecialidadForm # Usa el formulario definido en forms.py
 template_name = 'especialidad/especialidad-form.html' # Plantilla HTML del formulario
 success_url = reverse_lazy('gestion_citas:especialidad-list') # Redirección después de crear con éxito


class EspecialidadUpdateView(RolRequiredMixin, UpdateView): # Permite editar una especialidad existente
 model = Especialidad # Modelo a editar
 rol_permitido = 'admin' # Solo los administradores pueden modificar
 fields = ['nombre'] # Campos que se pueden editar
 template_name = "especialidad/especialidad-form.html" # Reutiliza la plantilla de creación
 success_url = reverse_lazy('gestion_citas:especialidad-list') # Redirección al listado tras actualizar


class EspecialidadDeleteView(RolRequiredMixin, DeleteView): # Permite eliminar una especialidad
 model = Especialidad # Modelo que se eliminará
 rol_permitido = 'admin' # Solo los administradores pueden eliminar
 template_name = "especialidad/especialidad-delete.html" # Plantilla de confirmación de eliminación
 success_url = reverse_lazy('gestion_citas:especialidad-list') # Redirección tras la eliminación


# ===============================
# VISTAS PARA PACIENTE
# ===============================


class PacienteListView(RolRequiredMixin, ListView): # Muestra todos los pacientes registrados
 model = Paciente # Modelo a listar
 rol_permitido = 'admin' # Solo administradores pueden acceder
 template_name = 'paciente/paciente-list.html' # Plantilla de la lista de pacientes
 context_object_name = 'pacientes' # Variable de contexto accesible en la plantilla
 def get_queryset(self):
        qs = super().get_queryset()
        filtro = self.request.GET.get('buscar', '')
        if filtro:
            qs = qs.filter(usuario_first_nameicontains=filtro) | qs.filter(usuariolast_name_icontains=filtro)
        return qs

 def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro'] = self.request.GET.get('buscar', '')
        return context


class PacienteCreateView(RolRequiredMixin, CreateView): # Permite crear un nuevo paciente
 model = Paciente # Modelo asociado
 rol_permitido = 'admin' # Solo admin puede crear pacientes
 form_class = PacienteForm # Formulario para la creación
 template_name = 'paciente/paciente-form.html' # Plantilla HTML del formulario
 success_url = reverse_lazy('gestion_citas:paciente-list') # Redirección tras creación


class PacienteUpdateView(RolRequiredMixin, UpdateView): # Permite modificar un paciente existente
 model = Paciente # Modelo asociado
 rol_permitido = 'admin' # Solo admin puede modificar
 form_class = PacienteForm # Formulario para la edición
 template_name = 'paciente/paciente-form.html' # Plantilla reutilizada
 success_url = reverse_lazy('gestion_citas:paciente-list') # Redirección al listado tras editar


class PacienteDeleteView(RolRequiredMixin, DeleteView): # Permite eliminar un paciente
 model = Paciente # Modelo asociado
 rol_permitido = 'admin' # Solo admin puede eliminar
 template_name = 'paciente/paciente-delete.html' # Plantilla de confirmación de eliminación
 success_url = reverse_lazy('gestion_citas:paciente-list') # Redirección tras eliminar


# ===============================
# VISTAS PARA MÉDICO
# ===============================


class MedicoListView(RolRequiredMixin, ListView): # Muestra la lista de médicos registrados
 model = Medico # Modelo a listar
 rol_permitido = 'admin' # Solo admin puede acceder
 template_name = 'medico/medico-list.html' # Plantilla HTML con la lista
 context_object_name = 'medicos' # Nombre de la variable de contexto en la plantilla
def get_queryset(self):  
    queryset = super().get_queryset()  # Obtiene todos los registros del modelo  
    filtro = self.request.GET.get('buscar', '')  # Captura el texto ingresado en el buscador  

    if filtro:  # Si hay texto para filtrar  
        queryset = queryset.filter(  # Filtra por nombre, apellido o especialidad del médico  
            Q(usuario__first_name__icontains=filtro) |
            Q(usuario__last_name__icontains=filtro) |
            Q(especialidades__nombre__icontains=filtro)
        )

    return queryset  # Devuelve la lista filtrada  


def get_context_data(self, **kwargs):  
    context = super().get_context_data(**kwargs)  # Obtiene el contexto base  
    context['filtro'] = self.request.GET.get('buscar', '')  # Mantiene el valor del buscador activo  
    return context  # Devuelve el contexto actualizado  

class MedicoCreateView(RolRequiredMixin, CreateView): # Permite registrar un nuevo médico
 model = Medico # Modelo asociado
 rol_permitido = 'admin' # Solo admin puede crear médicos
 form_class = MedicoForm # Formulario para la creación
 template_name = 'medico/medico-form.html' # Plantilla HTML del formulario
 success_url = reverse_lazy('gestion_citas:medico-list') # Redirección tras creación
 
class MedicoUpdateView(RolRequiredMixin, UpdateView): # Permite actualizar datos de un médico
 model = Medico # Modelo asociado
 rol_permitido = 'admin' # Solo admin puede modificar
 form_class = MedicoForm # Formulario usado para la edición
 template_name = 'medico/medico-form.html' # Plantilla HTML del formulario
 success_url = reverse_lazy('gestion_citas:medico-list') # Redirección tras actualizar


class MedicoDeleteView(RolRequiredMixin, DeleteView): # Permite eliminar un médico
 model = Medico # Modelo a eliminar
 rol_permitido = 'admin' # Solo admin puede eliminar
 template_name = 'medico/medico-delete.html' # Plantilla para confirmar eliminación
 success_url = reverse_lazy('gestion_citas:medico-list') # Redirección tras eliminar


# ===============================
# VISTAS PARA CITA
# ===============================


class CitaListView(RolRequiredMixin, ListView): # Muestra la lista de citas disponibles según el rol
 model = Cita # Modelo a listar
 template_name = 'cita/cita-list.html' # Plantilla HTML donde se muestran las citas
 context_object_name = 'citas' # Nombre de la variable que contendrá las citas en la plantilla
 


 rol_permitido = 'admin' # Solo ciertos roles pueden acceder a esta vista ('admin', 'medico', 'paciente')


def get_queryset(self): # Método que filtra las citas según el rol del usuario autenticado
 user = self.request.user # Obtiene el usuario actual de la solicitud


 if user.rol == 'admin': # Si el usuario es administrador
  return Cita.objects.all() # Devuelve todas las citas
 elif user.rol == 'medico': # Si el usuario es médico
  return Cita.objects.filter(medico__usuario=user) # Muestra solo las citas del médico actual
 elif user.rol == 'paciente': # Si el usuario es paciente
  return Cita.objects.filter(paciente__usuario=user) # Muestra solo las citas del paciente actual
 else:
  return Cita.objects.none() # Si el rol no es válido, no devuelve resultados
 
def get_queryset(self):  
    from django.db.models import Q  # Permite usar filtros con condiciones OR  
    qs = super().get_queryset()  # Obtiene todos los registros del modelo  
    filtro = self.request.GET.get('buscar', '')  # Captura el valor del buscador  

    if filtro:  # Si hay texto de búsqueda  
        qs = qs.filter(  # Filtra por fecha, médico o paciente  
            Q(fecha_hora__icontains=filtro) |
            Q(medico__usuario__first_name__icontains=filtro) |
            Q(paciente__usuario__first_name__icontains=filtro)
        )
    return qs  # Devuelve los resultados filtrados  


def get_context_data(self, **kwargs):  
    context = super().get_context_data(**kwargs)  # Obtiene el contexto base  
    context['filtro'] = self.request.GET.get('buscar', '')  # Mantiene el texto del buscador  
    return context  # Devuelve el contexto actualizado  



class CitaCreateView(RolRequiredMixin, CreateView): # Permite crear una nueva cita médica
 model = Cita # Modelo asociado
 rol_permitido = 'admin' # Solo el admin puede crear citas manualmente
 form_class = CitaForm # Formulario usado para la creación
 template_name = 'cita/cita-form.html' # Plantilla HTML del formulario
 success_url = reverse_lazy('gestion_citas:cita-list') # Redirección al listado de citas tras crear


class CitaUpdateView(RolRequiredMixin, UpdateView): # Permite modificar una cita existente
 model = Cita # Modelo asociado
 rol_permitido = 'admin' # Solo admin puede modificar
 form_class = CitaForm # Formulario para la edición
 template_name = 'cita/cita-form.html' # Plantilla reutilizada
 success_url = reverse_lazy('gestion_citas:cita-list') # Redirección tras editar


class CitaDeleteView(RolRequiredMixin, DeleteView): # Permite eliminar una cita médica
 model = Cita # Modelo asociado
 rol_permitido = 'admin' # Solo admin puede eliminar
 template_name = 'cita/cita-delete.html' # Plantilla HTML para confirmar la eliminación
 success_url = reverse_lazy('gestion_citas:cita-list') # Redirección al listado tras eliminar