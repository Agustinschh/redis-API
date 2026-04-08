# Cosas de Redis para el alquiler (reserva 4 min, alquiler 24 hs).
# Claves: mando:cap:N:reserva y mando:cap:N:alquiler

from .redis_con import get_connection

RESERVA_SEG = 4 * 60  # 4 minutos
ALQUILER_SEG = 24 * 60 * 60  # 24 horas


def _key_reserva(num):
    return f"mando:cap:{num}:reserva"


def _key_alquiler(num):
    return f"mando:cap:{num}:alquiler"


def estado_capitulo(num):
    """Devuelve (estado, segundos_restantes). estado = disponible | reservado | alquilado."""
    r = get_connection()
    if r.exists(_key_alquiler(num)):
        return "alquilado", r.ttl(_key_alquiler(num))
    if r.exists(_key_reserva(num)):
        return "reservado", r.ttl(_key_reserva(num))
    return "disponible", None


def reservar_capitulo(num):
    r = get_connection()
    if r.exists(_key_alquiler(num)):
        return False, "Ese capítulo ya está alquilado por alguien."
    if r.exists(_key_reserva(num)):
        return False, "Ya está reservado (esperá que venza o confirmen el pago)."
    r.set(_key_reserva(num), "1", ex=RESERVA_SEG)
    return True, "Listo, quedó reservado por 4 minutos. Confirmá el pago."


def confirmar_pago(num, precio_texto):
    r = get_connection()
    if not r.exists(_key_reserva(num)):
        return False, "No hay reserva activa (venció o nunca reservaste este capítulo)."
    try:
        precio = float(precio_texto)
    except (TypeError, ValueError):
        return False, "El precio tiene que ser un número."
    if precio < 0:
        return False, "El precio no puede ser negativo."

    pipe = r.pipeline()
    pipe.delete(_key_reserva(num))
    # guardamos el precio en el valor por si después querés mostrarlo
    pipe.set(_key_alquiler(num), str(precio), ex=ALQUILER_SEG)
    pipe.execute()
    return True, f"Pago confirmado. Alquilado por 24 hs (precio registrado: {precio})."


def filas_para_listado():
    """Une la lista fija de capítulos con el estado actual en Redis."""
    from .data import CAPITULOS

    out = []
    for c in CAPITULOS:
        num = c["numero"]
        estado, seg = estado_capitulo(num)
        out.append(
            {
                "numero": num,
                "temporada": c["temporada"],
                "titulo": c["titulo"],
                "estado": estado,
                "segundos_restantes": seg if seg and seg > 0 else None,
            }
        )
    return out
