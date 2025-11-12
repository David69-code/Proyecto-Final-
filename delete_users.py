import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SistemaCitas.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.all().delete()
print("Todos los usuarios han sido eliminados.")
