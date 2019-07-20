import os
import urllib
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render_to_response

from paparajotes_y_bellotas.users import models

def location_view(request):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    base_images_path = "images/venue/"
    images_path = os.path.join(dirpath, "static", base_images_path)

    all_images = sorted(os.listdir(images_path))
    all_images_full = [urllib.parse.urljoin(base_images_path, img) for img in all_images]

    return render_to_response('pages/location.html', {'venue_images': all_images_full})

def homepage_view(request):
    query_results = models.User.objects.all()

    quotes = [{'mensaje': u.mensaje, 'firma': u.firma} for u in query_results if len(u.mensaje) > 4]

    return render_to_response('pages/home.html', {'quotes': quotes})
