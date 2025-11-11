from django.contrib.auth.models import AbstractUser  # Modelo base de usuario de Django
from django.db import models  # Para definir modelos de Django


# ==============================
# Modelo de usuario personalizado
# ==============================
class Usuario(AbstractUser):
    # 🔹 Definición de roles posibles
    ROLES = [
        ('admin', 'Administrador'),  # Valor interno, Valor mostrado
        ('medico', 'Médico'),
        ('paciente', 'Paciente'),
    ]

    # 🔹 Campo adicional para almacenar el rol del usuario
    rol = models.CharField(
        max_length=20,      # Tamaño máximo del campo
        choices=ROLES,      # Opciones definidas arriba
        default='paciente'  # Rol por defecto al crear un usuario
    )

    # 🔹 Representación en texto del objeto
    def __str__(self):
        # Muestra username y rol en formato legible
        return f"{self.username} ({self.get_rol_display()})"