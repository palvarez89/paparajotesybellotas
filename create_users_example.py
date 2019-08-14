import django
import os
import yaml

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.contrib.auth.hashers import make_password
from paparajotes_y_bellotas.users import models

with open("users.yaml", 'r') as f:
    try:
        file_contents = yaml.safe_load(f)
    except Exception as e:
        print("Failed to load yaml: %s" % e)
        exit(1)

users = file_contents['users']
for user in users:
    new_user = models.User(
        username=user['username'],
        email='none@none.co.uk',
        password=make_password(user['password']),
        is_active=True,
    )
    new_user.save()

    for invitado in user['invitados']:
        inv = models.Invitado()
        inv.nombre = invitado['nombre']
        inv.user = new_user
        inv.save()
