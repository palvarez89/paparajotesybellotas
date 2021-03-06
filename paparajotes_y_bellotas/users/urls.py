from django.urls import path

from paparajotes_y_bellotas.users.views import (
    user_list_view,
    user_list_view_csv,
    user_redirect_view,
    user_update_view,
    user_detail_view,
)

app_name = "users"
urlpatterns = [
    path("list/", view=user_list_view, name="list"),
    path("listcsv/", view=user_list_view_csv, name="list_csv"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
