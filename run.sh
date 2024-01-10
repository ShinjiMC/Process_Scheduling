#!/bin/bash

# Ejecuta el comando make para compilar
make

# Comprueba si la compilación fue exitosa antes de ejecutar el programa
if [ $? -eq 0 ]; then
    # Ejecuta el programa generado (main)
    ./bin/main
else
    echo "Error al compilar. Por favor, revisa los errores."
fi
