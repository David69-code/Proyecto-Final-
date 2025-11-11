from functools import wraps  # Para mantener metadata de la función original
from django.shortcuts import redirect  # Para redirigir a otra página
from django.contrib import messages  # Para mostrar mensajes al usuario


# ==============================
# DECORADOR: Solo admin
# ==============================
def admin_required(view_func):
    """Permite solo a usuarios con rol=admin"""
    @wraps(view_func)  # Mantiene el nombre y docstring de la función original
    def wrapper(request, *args, **kwargs):
        # 🔹 Verifica si el usuario está autenticado
        if not request.user.is_authenticated:
            return redirect('login')
        # 🔹 Verifica si el rol del usuario es 'admin'
        if getattr(request.user, 'rol', None) != 'admin':
            messages.error(request, "No tienes permiso para acceder al panel de administrador.")
            return redirect('home')  # Redirige a home si no es admin
        # 🔹 Si pasa la validación, ejecuta la función original
        return view_func(request, *args, **kwargs)
    return wrapper


# ==============================
# DECORADOR: Solo médico
# ==============================
def medico_required(view_func):
    """Permite solo a usuarios con rol=medico"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if getattr(request.user, 'rol', None) != 'medico':
            messages.error(request, "No tienes permiso para acceder al panel de médico.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ==============================
# DECORADOR: Solo paciente
# ==============================
def paciente_required(view_func):
    """Permite solo a usuarios con rol=paciente"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if getattr(request.user, 'rol', None) != 'paciente':
            messages.error(request, "No tienes permiso para acceder al panel de paciente.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper