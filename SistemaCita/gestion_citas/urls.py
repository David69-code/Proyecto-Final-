# archivo de enrutamiento de la aplicación productos
from django.urls import path

# importando las vistas
from .views import (
    #Especialidad
    EspecialidadListView,
    EspecialidadCreateView,
    EspecialidadUpdateView,
    EspecialidadDeleteView,

    #Paciente
    PacienteListView,
    PacienteCreateView,
    PacienteUpdateView,
    PacienteDeleteView,

    #Medico
    MedicoListView,
    MedicoCreateView,
    MedicoUpdateView,
    MedicoDeleteView,

    #Cita
    CitaListView,
    CitaCreateView,
    CitaUpdateView,
    CitaDeleteView,


)

# agregar un identificador de enrutamiento
app_name = "gestion_citas"

# enrutamiento
urlpatterns = [
    #especialidades
    path('especialidades/', EspecialidadListView.as_view(), name="especialidad-list"),
    path('especialidades/nueva', EspecialidadCreateView.as_view(), name="especialidad-create"),
    path('especialidades/editar/<int:pk>/', EspecialidadUpdateView.as_view(), name='especialidad-update'),
    path('especialidades/eliminar/<int:pk>/', EspecialidadDeleteView.as_view(), name='especialidad-delete'),
    #pacientes
    path('pacientes/', PacienteListView.as_view(), name="paciente-list"),
    path('pacientes/nueva', PacienteCreateView.as_view(), name="paciente-create"),
    path('pacientes/editar/<int:pk>/', PacienteUpdateView.as_view(), name='paciente-update'),
    path('pacientes/eliminar/<int:pk>/', PacienteDeleteView.as_view(), name='paciente-delete'),
   
    #medicos
    path('medicos/', MedicoListView.as_view(), name="medico-list"),
    path('medicos/nueva', MedicoCreateView.as_view(), name="medico-create"),
    path('medicos/editar/<int:pk>/', MedicoUpdateView.as_view(), name='medico-update'),
    path('medicos/eliminar/<int:pk>/', MedicoDeleteView.as_view(), name='medico-delete'),
     
    #citas
    path('citas/', CitaListView.as_view(), name="cita-list"),
    path('citas/nueva', CitaCreateView.as_view(), name="cita-create"),
    path('citas/editar/<int:pk>/', CitaUpdateView.as_view(), name='cita-update'),
    path('citas/eliminar/<int:pk>/', CitaDeleteView.as_view(), name='cita-delete'),

]
