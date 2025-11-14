# core/signals.py (ARCHIVO NUEVO)

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .utils import crear_admin # Importamos tu función original

@receiver(post_migrate)
def inicializar_datos(sender, **kwargs):
    """
    Función que se ejecuta después de que las migraciones han corrido.
    Solo se ejecuta una vez al inicio del despliegue.
    """
    # Verificamos que la señal sea de la app 'core' para evitar ejecuciones duplicadas
    # La tupla de apps en kwargs solo está disponible si se usa `migrate` con un nombre de app.
    # Para mayor seguridad en Render, verificamos el nombre del sender.
    if sender.name == 'core':
        crear_admin() 
        print("🚀 Inicialización de grupos y admin completada.")