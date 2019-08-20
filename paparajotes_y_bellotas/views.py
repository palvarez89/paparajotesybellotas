import os
import random
import urllib
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.messages import get_messages
from django.shortcuts import render

from paparajotes_y_bellotas.users import models

def location_view(request):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    base_images_path = "images/venue/"
    images_path = os.path.join(dirpath, "static", base_images_path)
    storage = get_messages(request)

    all_images = sorted(os.listdir(images_path))
    all_images_full = [urllib.parse.urljoin(base_images_path, img) for img in all_images]

    return render(request, 'pages/location.html', {'venue_images': all_images_full, 'messages': storage})

def homepage_view(request):
    query_results = models.User.objects.all()
    storage = get_messages(request)

    quotes = [{'mensaje': u.mensaje, 'firma': u.firma} for u in query_results if len(u.mensaje) > 4]

    random.shuffle(quotes)
    return render(request, 'pages/home.html', {'quotes': quotes, 'messages': storage})
