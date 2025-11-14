from django.apps import AppConfig  # Importa la clase base para configurar apps


class CoreConfig(AppConfig):
    # 🔹 Define la configuración para la app "core"
    default_auto_field = 'django.db.models.BigAutoField'  # Tipo de campo por defecto para IDs
    name = 'core'  # Nombre de la app

    def ready(self):
        """
        Este método se ejecuta cuando Django carga la app.
        Ideal para inicializaciones que necesitan el ORM cargado.
        """
        # 🔹 Importa la función crear_admin desde utils
        # Esto se hace aquí y no al inicio para evitar problemas de importación circular
        from .utils import crear_admin
        # 🔹 Crea automáticamente un usuario admin si no existe
        crear_admin()