from django.shortcuts import render

from .redis_con import get_connection

KEY = "personajes"
DEFAULT_ITEMS = ["luke", "han", "leia", "chewbacca"]


def index(request):
    db = get_connection()
    if db.llen(KEY) == 0:
        db.rpush(KEY, *DEFAULT_ITEMS)
    datos = db.lrange(KEY, 0, -1)
    return render(request, "personajes/index.html", {"datos": datos})
