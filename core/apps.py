# core/apps.py (Modificado)

from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # 1. ELIMINAR la importación y llamada a crear_admin()
        # from .utils import crear_admin
        # crear_admin() 
        
        # 2. AÑADIR la importación del nuevo archivo de señales
        import core.signals 
        
        # ¡Todo lo demás queda limpio!
        pass
    