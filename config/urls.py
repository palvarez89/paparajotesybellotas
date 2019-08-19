from django.conf import settings
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from allauth.account import views as account_views

from paparajotes_y_bellotas.views import (
    location_view,
    homepage_view,
)

urlpatterns = i18n_patterns(
    path(
        "",
        view=homepage_view,
        name="home",
    ),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "location/",
        view=location_view,
        name="location",
    ),
    path(
        "tips/",
        TemplateView.as_view(template_name="pages/tips.html"),
        name="tips",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path(
        "users/",
        include("paparajotes_y_bellotas.users.urls", namespace="users"),
    ),
    path("accounts/login/", account_views.login, name="account_login"),
    path("accounts/login/", account_views.login, name="account_signup"),
    path("accounts/logout/", account_views.logout, name="account_logout"),
    # Your stuff: custom urls includes go here
) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
