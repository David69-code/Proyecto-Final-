from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, CustomLogoutView, landing_page # Importamos la nueva vista


urlpatterns = [
    # PÁGINA PRINCIPAL / LANDING PAGE (Esta es la raíz '/')
    # Muestra los recuadros que redirigen al login.
    path('', landing_page, name='landing_page'),
    # -------------------------------------------------------------------

    # Redirección de Dashboard Post-Login (home.html)
    # Se accede solo después de iniciar sesión.
    path('dashboard/', views.home_page, name='home'),

    # Autenticación
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),

    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    #Paciente URLs Citas
    path('paciente/citas/', views.PacienteCitaListView.as_view(), name='paciente_cita_list'),
    path('paciente/citas/nueva/', views.PacienteCitaCreateView.as_view(), name='paciente_cita_create'),
    path('paciente/citas/<int:pk>/editar/', views.PacienteCitaUpdateView.as_view(), name='paciente_cita_edit'),
    path('paciente/citas/<int:pk>/eliminar/', views.PacienteCitaDeleteView.as_view(), name='paciente_cita_delete'),
    
    # NUEVA URL DE PERFIL DEL PACIENTE
    path('paciente/perfil/', views.paciente_perfil, name='paciente_perfil'),
    
    # Completar perfil paciente
    path('completar-perfil/paciente/', views.completar_perfil_paciente, name='completar_perfil_paciente'),
    
    # Médico URLs
    path('medico/agenda/', views.agenda_medico, name='medico_agenda'),
    path('medico/actualizar-estado/', views.actualizar_estado_cita, name='medico-actualizar-estado'),
    
    # URLs de Perfil del Médico
    path('medico/perfil/', views.medico_perfil, name='medico_perfil'),
    path('medico/perfil/editar/', views.medico_perfil_edit, name='medico_perfil_edit'),
    
    # Registrar medico
    path('admin/registrar_medico/', views.registrar_medico, name='registrar_medico'),

     # Listado de pacientes en Medico
    path('medico/pacientes/', views.pacientes_medico, name='pacientes_medico'),
]