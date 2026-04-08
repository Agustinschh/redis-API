from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .data import CAPITULOS
from .rental_redis import confirmar_pago, filas_para_listado, reservar_capitulo


def lista_capitulos(request):
    """Pantalla principal: tabla/cards con estado de cada capítulo."""
    filas = filas_para_listado()
    return render(request, "personajes/lista.html", {"filas": filas})


def api_lista_capitulos(request):
    """Misma info en JSON (para probar con el navegador o Postman)."""
    return JsonResponse(filas_para_listado(), safe=False)


def _numero_valido(num):
    ok = {c["numero"] for c in CAPITULOS}
    return num in ok


@require_POST
def reservar(request, numero):
    if not _numero_valido(numero):
        messages.error(request, "Número de capítulo inválido.")
        return redirect("lista_capitulos")
    ok, msg = reservar_capitulo(numero)
    if ok:
        messages.success(request, msg)
    else:
        messages.error(request, msg)
    return redirect("lista_capitulos")


@require_POST
def confirmar_pago_view(request, numero):
    if not _numero_valido(numero):
        messages.error(request, "Número de capítulo inválido.")
        return redirect("lista_capitulos")
    precio = request.POST.get("precio", "")
    ok, msg = confirmar_pago(numero, precio)
    if ok:
        messages.success(request, msg)
    else:
        messages.error(request, msg)
    return redirect("lista_capitulos")
