import django
import os
import yaml
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.contrib.auth.hashers import make_password
from paparajotes_y_bellotas.users import models

args = sys.argv
nargs = len(args)

if (nargs != 2):
    print("create_users_example.py <yamlfile>")
    sys.exit(2)

print(args)

with open(args[1], 'r') as f:
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
