# Automate Aloha

Este repositorio contiene un programa de automatización escrito en Python para interactuar con el software Aloha 5.4.7. El objetivo del programa es ejecutar simulaciones y generar informes de resultados para diferentes casos de estudio.

## Requisitos

Antes de utilizar este programa, asegúrate de tener instalado lo siguiente:

- Python 3.x
- Las dependencias listadas en el archivo `requirements.txt`. Puedes instalarlas ejecutando el siguiente comando:

  ```bash
  pip install -r requirements.txt
  ```

Además, es necesario configurar algunas variables de entorno antes de ejecutar el programa:

- `ALOHA_PATH`: Ruta de instalación de Aloha 5.4.7.
- `ALOHA_CASE`: Número de caso de estudio a ejecutar.
- `ALOHA_DATA`: Ruta del archivo CSV que contiene los datos de entrada para las simulaciones.
Asegúrate de definir estas variables de entorno correctamente antes de ejecutar el programa.

Opcionalmente, puedes crear un entorno virtual para aislar las dependencias del proyecto. Sigue los siguientes pasos para crear y activar un entorno virtual:

1. Abre una terminal en la raíz del proyecto.

2. Ejecuta el siguiente comando para crear un nuevo entorno virtual:

    ```bash
    python -m venv env
    ```

3. Activa el entorno virtual. Dependiendo del sistema operativo, ejecuta uno de los siguientes comandos:

- En Windows:

  ```bash
  .\env\Scripts\activate
  ```

- En macOS/Linux:

  ```bash
  source env/bin/activate
  ```

Con el entorno virtual activado, puedes instalar las dependencias y ejecutar el programa sin afectar la instalación global de Python.

## Estructura del proyecto

El proyecto está organizado de la siguiente manera:

- `automate_aloha/__main__.py`: Punto de entrada del programa. Aquí se encuentra el código principal para ejecutar las simulaciones.
- `automate_aloha/config/__init__.py`: Archivo de configuración que carga las variables de entorno y las hace disponibles en el programa.
- `automate_aloha/aloha_bot/__init__.py`: Módulo que contiene la clase Aloha, encargada de interactuar con el software Aloha.
- `automate_aloha/aloha_bot/Aloha.py`: Implementación de la clase Aloha, que se encarga de iniciar, configurar y cerrar la aplicación Aloha, así como ejecutar las simulaciones.
- `automate_aloha/aloha_bot/cases`: Directorio que contiene las clases y estrategias para cada caso de estudio.
- `automate_aloha/aloha_bot/cases/Strategy.py`: Interfaz abstracta para las estrategias de casos de estudio.
- `automate_aloha/aloha_bot/cases/Context.py`: Clase Context que maneja la estrategia actual y permite ejecutar las simulaciones.
- `automate_aloha/aloha_bot/cases/Case_1.py` y `automate_aloha/aloha_bot/cases/Case_2.py`: Implementaciones de estrategias para los casos de estudio 1 y 2, respectivamente.

## Uso

Antes de ejecutar el programa, asegúrate de haber configurado correctamente las variables de entorno y haber proporcionado el archivo CSV de datos de entrada.

Para ejecutar el programa, utiliza el siguiente comando:

```bash
python -m automate_aloha
```

Durante la ejecución, el programa generará archivos de registro en la carpeta `automate_aloha/logs`, así como archivos de resultados en la carpeta `automate_aloha/out`.

Recuerda que el uso de un entorno virtual es opcional, pero puede ser útil para mantener las dependencias del proyecto aisladas del entorno global de Python.
