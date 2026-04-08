#!/usr/bin/env python
"""Punto de entrada de Django para tareas de administración."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appNSQL.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Instalaste las dependencias? "
            "pip install -r requirements.txt"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
