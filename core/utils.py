from django.contrib.auth import get_user_model  # Permite obtener el modelo de usuario activo
from django.contrib.auth.models import Group  # Para manejar grupos de usuarios


def crear_admin():
    # Obtiene el modelo de usuario actual (puede ser personalizado)
    User = get_user_model()

    # 🔹 Crear grupos si no existen
    grupos = {}
    for nombre in ["Administrador", "Medico", "Paciente"]:
        # get_or_create: obtiene el grupo si existe, o lo crea si no
        grupo, _ = Group.objects.get_or_create(name=nombre)
        grupos[nombre] = grupo  # Guarda referencia al grupo en un diccionario

    # 🔹 Crear usuario admin si no existe
    if not User.objects.filter(username="admin").exists():
        # Crea un nuevo usuario
        admin = User(username="admin", email="admin@midominio.com")
        admin.set_password("admin123")  # Define la contraseña
        admin.is_superuser = True  # Marca como superusuario
        admin.is_staff = True      # Puede entrar al admin
        admin.is_active = True     # Usuario activo
        admin.rol = "admin"        # Asigna rol personalizado
        admin.save()               # Guarda en la base de datos
        admin.groups.add(grupos["Administrador"])  # Añade al grupo Administrador
        print("✅ Usuario admin creado automáticamente")
    else:
        print("⚠ Usuario admin ya existe")  # Mensaje si ya está creado