from django.contrib.auth.mixins import LoginRequiredMixin  # Para proteger vistas de clases
from django.shortcuts import redirect  # Para redirigir usuarios no autorizados


# ==============================
# Mixin para restringir vistas por rol
# ==============================
class RolRequiredMixin(LoginRequiredMixin):
    rol_permitido = None        # Para restringir a un solo rol específico
    roles_permitidos = []       # Para restringir a varios roles

    def dispatch(self, request, *args, **kwargs):
        # 🔹 Si el usuario no está autenticado, redirige al login
        if not request.user.is_authenticated:
            return redirect('login')

        # 🔹 Obtiene el rol del usuario (si existe)
        rol_usuario = getattr(request.user, 'rol', None)

        # 🔹 Verifica un solo rol permitido
        if self.rol_permitido and rol_usuario != self.rol_permitido:
            return redirect('home')  # Redirige a home si no coincide

        # 🔹 Verifica varios roles permitidos
        if self.roles_permitidos and rol_usuario not in self.roles_permitidos:
            return redirect('home')  # Redirige si el rol del usuario no está en la lista

        # 🔹 Si pasa todas las verificaciones, continua con la vista
        return super().dispatch(request, *args, **kwargs)