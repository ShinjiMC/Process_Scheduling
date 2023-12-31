#!/bin/bash

# Crear entorno virtual myenv
python3 -m venv myenv

# Activar entorno virtual y instalar matplotlib
source myenv/bin/activate
pip install matplotlib

# Ejecutar Makefile
if make; then
    # Ejecutar el programa generado (main)
    ./bin/main
else
    echo "Error al compilar. Por favor, revisa los errores."
fi

# Ejecutar graph.py con el entorno virtual activado
python graph.py

# Desactivar entorno virtual
deactivate
