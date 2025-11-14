# Importa funciones para renderizar templates, redirigir URLs y obtener objetos o devolver 404 si no existe
from django.shortcuts import render, redirect, get_object_or_404
# Permite iniciar sesión de un usuario
from django.contrib.auth import login
# Permite generar URLs inversas usando nombres de rutas, útil en redirecciones
from django.urls import reverse_lazy
# Decorador para requerir que un usuario esté logueado para acceder a una vista
from django.contrib.auth.decorators import login_required
# Clases genéricas de Django para manejo de login y logout
from django.contrib.auth.views import LoginView, LogoutView
# Clases genéricas de vistas de Django para listar, crear, actualizar o eliminar objetos
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# Decorador para requerir que una vista solo acepte solicitudes POST
from django.views.decorators.http import require_POST
# IMPORTACIÓN CLAVE: Decorador para evitar que la página se guarde en caché.
from django.views.decorators.cache import never_cache 
# Proporciona utilidades para trabajar con fechas y horas considerando la zona horaria
from django.utils import timezone 
# Para devolver respuestas en formato JSON
# Para devolver una respuesta HTTP de “prohibido” (403)
from django.http import JsonResponse, HttpResponseForbidden
# Permite crear diccionarios con valores por defecto para cada clave
from collections import defaultdict

# Formularios importados
from .forms import RegistroForm, PacienteCitaForm
from gestion_citas.forms import PacientePerfilForm
from django.contrib import messages
from .forms import MedicoRegistroForm

# Modelos
from gestion_citas.models import Medico, Paciente, Cita

# Decoradores de rol
from .decorators import admin_required, medico_required, paciente_required

# Mixins para vistas basadas en clases
from .mixins import RolRequiredMixin

# ==========================================================
# 🏠 NUEVA PÁGINA PRINCIPAL (LANDING PAGE) 
# ==========================================================
def landing_page(request):
    # Si el usuario ya está autenticado, lo redirigimos a su dashboard
    if request.user.is_authenticated:
        return redirect('home') 
        
    # Si NO está autenticado, mostramos la página principal con los botones de login
    return render(request, 'core/home.html')

# ==========================================================
# 🔹 LOGIN Y LOGOUT PERSONALIZADOS
# ==========================================================
class CustomLoginView(LoginView):
    template_name = "core/login.html" 
    redirect_authenticated_user = True 


class CustomLogoutView(LogoutView):
    # CAMBIO CLAVE: Redirige a la landing page (home.html) después del logout.
    next_page = reverse_lazy('landing_page')


# ==========================================================
# 🔹 REGISTRO DE USUARIO
# ==========================================================
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST) 
        if form.is_valid(): 
            user = form.save() 
            login(request, user) 
            # Redirige a completar perfil de paciente
            return redirect('completar_perfil_paciente') 
    else:
        form = RegistroForm() 
    return render(request, 'core/registro.html', {'form': form})


# ==========================================================
# 🔹 VISTAS SEGÚN ROL
# ==========================================================
@never_cache # <-- CLAVE: Evita la caché en la redirección inicial
@login_required
def home_page(request):
    usuario = request.user
    # Redirige según rol del usuario
    if usuario.rol == 'admin':
        return redirect('admin_dashboard')
    elif usuario.rol == 'medico':
        return redirect('medico_agenda')
    else:
        return redirect('paciente_cita_list')


@never_cache # <-- CLAVE: Evita la caché del navegador
@login_required
@admin_required
def admin_dashboard(request):
    # Renderiza la plantilla del dashboard
    response = render(request, 'admin/panel_admin.html', {})
    # SOLUCIÓN DE SEGURIDAD: Fuerza al navegador a no guardar esta página en el historial de caché.
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@never_cache # <-- CLAVE: Evita la caché del navegador
@medico_required
def agenda_medico(request):
    # Obtiene el médico logueado
    try:
        medico = Medico.objects.get(usuario=request.user)
    except Medico.DoesNotExist:
        return HttpResponseForbidden("No tienes permisos de médico para ver esta página.")

    # Obtiene las citas del médico
    citas = Cita.objects.filter(medico=medico).order_by('fecha_hora')

    # Agrupa citas por día
    dias = defaultdict(list)
    for c in citas:
        dia = c.fecha_hora.date() if c.fecha_hora else None
        dias[dia].append(c)

    # Ordena los días (None al final)
    dias_ordenados = sorted(dias.items(), key=lambda x: (x[0] is None, x[0]))

    context = {
        'medico': medico,
        'dias_ordenados': dias_ordenados,
        'now': timezone.now(),
    }
    
    # Renderiza y aplica el control de caché
    response = render(request, 'medico/agenda_medico.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@never_cache # <-- CLAVE: Evita la caché del navegador
@paciente_required
def paciente_cita_list(request):
    # NOTA: Esta vista funcional solo pasa 'now', el listado de citas
    # debe ser manejado por la PacienteCitaListView, que es la vista principal.
    context = {
        'now': timezone.now(), 
    }
    
    # Renderiza y aplica el control de caché
    response = render(request, 'paciente/paciente_cita_list.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

# ==========================================================
# 🔹 VISTAS DEL PERFIL DEL MÉDICO
# ==========================================================
@login_required
def medico_perfil(request):
    """
    Muestra la información del perfil del médico actual.
    """
    # Intentamos obtener el objeto Medico asociado al usuario logueado.
    try:
        medico = Medico.objects.get(usuario=request.user)
    except Medico.DoesNotExist:
        # Manejo de error si el usuario no tiene un perfil de Medico asociado
        # Podrías redirigir a una página de error o a completar perfil si es necesario.
        return redirect('home') 

    context = {
        'medico': medico,
        'now': timezone.now(),  # Usamos la zona horaria actual para la fecha
    }
    # Renderizamos el template que creamos anteriormente
    return render(request, 'medico/medico_perfil.html', context)


@login_required
def medico_perfil_edit(request):
    """
    Permite al médico editar su perfil. Por ahora, es una vista de marcador de posición.
    """
    # Obtener el objeto Medico actual
    medico = get_object_or_404(Medico, usuario=request.user)

    # Lógica de manejo del formulario de edición (placeholder)
    if request.method == 'POST':
        # Aquí iría la lógica para procesar el formulario de edición
        # Por ejemplo: form = MedicoPerfilForm(request.POST, instance=medico)
        # if form.is_valid(): form.save(); return redirect('medico_perfil')
        pass 
        
    context = {
        'medico': medico,
        'now': timezone.now(),
        # 'form': form, # Si se usa un formulario
    }
    
    # Renderizar un template de edición de perfil (necesitarás crear este HTML)
    return render(request, 'medico/medico_perfil_edit.html', context)


# ==========================================================
# 🔹 VISTAS DEL PERFIL DEL PACIENTE (NUEVA)
# ==========================================================
@login_required
@paciente_required
def paciente_perfil(request):
    """
    Muestra la información del perfil del paciente actual.
    """
    try:
        # Intentamos obtener el objeto Paciente asociado al usuario logueado.
        paciente = Paciente.objects.get(usuario=request.user)
    except Paciente.DoesNotExist:
        # Si el usuario es paciente pero no ha completado el perfil, redirigir
        return redirect('completar_perfil_paciente') 
        
    context = {
        'paciente': paciente,
        'now': timezone.now(),  # Usamos la zona horaria actual para la fecha
    }
    # Renderizamos el template que creamos
    return render(request, 'paciente/paciente_perfil.html', context)


# ==========================================================
# 🔹 COMPLETAR PERFIL DE PACIENTE
# ==========================================================
def completar_perfil_paciente(request):
    user = request.user
    form = PacientePerfilForm(request.POST or None) 

    if request.method == 'POST' and form.is_valid():
        paciente = form.save(commit=False) 
        paciente.usuario = user 
        paciente.save() 
        return redirect('home')

    return render(request, 'core/completar_perfil.html', {
        'form': form,
        'tipo': 'Paciente'
    })


# ==========================================================
# 🔹 CRUD DE CITAS DEL PACIENTE
# ==========================================================
class PacienteCitaListView(RolRequiredMixin, ListView):
    model = Cita
    rol_permitido = 'paciente' 
    template_name = 'paciente/paciente_cita_list.html'
    context_object_name = 'citas'

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'paciente':
            return Cita.objects.filter(paciente__usuario=user).order_by('-fecha_hora')
        return Cita.objects.none()

    # CORRECCIÓN PARA PASAR 'now' a la VBC, resolviendo el error de la fecha
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class PacienteCitaCreateView(RolRequiredMixin, CreateView):
    model = Cita
    rol_permitido = 'paciente'
    form_class = PacienteCitaForm
    template_name = 'paciente/paciente_cita_form.html'
    success_url = reverse_lazy('paciente_cita_list')

    def form_valid(self, form):
        # Asigna paciente automáticamente al crear cita
        form.instance.paciente = self.request.user.paciente
        return super().form_valid(form)


class PacienteCitaUpdateView(RolRequiredMixin, UpdateView):
    model = Cita
    rol_permitido = 'paciente'
    form_class = PacienteCitaForm
    template_name = 'paciente/paciente_cita_form.html'
    success_url = reverse_lazy('paciente_cita_list')

    def get_queryset(self):
        # Solo permite actualizar citas del paciente logueado
        return Cita.objects.filter(paciente__usuario=self.request.user)


class PacienteCitaDeleteView(RolRequiredMixin, DeleteView):
    model = Cita
    rol_permitido = 'paciente'
    template_name = 'paciente/paciente_cita_delete.html'
    success_url = reverse_lazy('paciente_cita_list')

    def get_queryset(self):
        # Solo permite eliminar citas del paciente logueado
        return Cita.objects.filter(paciente__usuario=self.request.user)


# ==========================================================
# 🔹 AJAX: ACTUALIZAR ESTADO DE CITA
# ==========================================================
@login_required
@require_POST
def actualizar_estado_cita(request):
    # Verifica que sea médico
    try:
        medico = Medico.objects.get(usuario=request.user)
    except Medico.DoesNotExist:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    # Obtiene datos del POST
    cita_id = request.POST.get('cita_id')
    nuevo_estado = request.POST.get('estado')
    if not cita_id or not nuevo_estado:
        return JsonResponse({'error': 'Datos incompletos'}, status=400)

    # Obtiene la cita
    cita = get_object_or_404(Cita, pk=cita_id)
    if cita.medico != medico:
        return JsonResponse({'error': 'No autorizado a modificar esta cita'}, status=403)

    # Actualiza estado y guarda
    cita.estado = nuevo_estado
    cita.save()
    return JsonResponse({
        'ok': True,
        'cita_id': cita_id,
        'nuevo_estado': nuevo_estado,
    })


# ==========================================================
# 🔹 REGISTRAR MÉDICO (ADMIN)
# ==========================================================
@login_required
@admin_required
def registrar_medico(request):
    # Verifica que sea admin
    if not request.user.rol == 'admin':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')

    if request.method == 'POST':
        form = MedicoRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico registrado correctamente.")
            return redirect('gestion_citas:medico-list') 
    else:
        form = MedicoRegistroForm()

    return render(request, 'admin/registrar_medico.html', {'form': form})