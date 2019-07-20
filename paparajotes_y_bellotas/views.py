import os
import urllib
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render_to_response

def location_view(request):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    base_images_path = "images/venue/"
    images_path = os.path.join(dirpath, "static", base_images_path)

    all_images = sorted(os.listdir(images_path))
    all_images_full = [urllib.parse.urljoin(base_images_path, img) for img in all_images]

    return render_to_response('pages/location.html', {'venue_images': all_images_full})

def homepage_view(request):
    return render_to_response('pages/home.html')
