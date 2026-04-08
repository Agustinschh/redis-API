from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista_capitulos, name="lista_capitulos"),
    path("api/capitulos/", views.api_lista_capitulos, name="api_lista_capitulos"),
    path("capitulos/<int:numero>/reservar/", views.reservar, name="reservar"),
    path(
        "capitulos/<int:numero>/confirmar-pago/",
        views.confirmar_pago_view,
        name="confirmar_pago",
    ),
]
