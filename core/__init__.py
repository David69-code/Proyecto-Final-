# Le indica a Django que use CoreConfig como la configuración por defecto de la app "core"
# Esto permite que se ejecute el método ready() al iniciar la app, creando el admin automáticamente
default_app_config = 'core.apps.CoreConfig'