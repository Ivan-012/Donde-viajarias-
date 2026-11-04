
- **Backend:** Python con Flask. Procesa los datos y se conecta a la API.
- **Frontend:** HTML, CSS y JavaScript.
- **Datos:** [REST Countries API v5](https://restcountries.com) (bandera, capital, población, idiomas y moneda).

---

## Requisitos


| Python | Versión 3.9 o superior ([python.org](https://www.python.org/downloads/)).
| Internet | Necesaria al menos la primera vez, para descargar los países. |
| API key | Gratuita, de REST Countries. |

Para comprobar Python, abrí una terminal y escribí `python --version` (en Mac o Linux puede ser `python3 --version`).

---

## Instalación paso a paso

### 1. Descargar el proyecto
Copiá la carpeta del proyecto a tu computadora. Debe verse así:

```
donde-viajarias/
├── app.py
├── datos.py
├── requirements.txt
├── .env.example
├── construir.bat
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```


###  Conseguir tu API key (gratis)
1. Creá una cuenta en [restcountries.com](https://restcountries.com) y copiá tu API key.
2. Copiá el archivo `.env.example` y renombrá la copia a **`.env`** (con el punto al principio y sin otra extensión).
3. Abrilo y pegá tu clave después del signo igual:
   ```
   RESTCOUNTRIES_API_KEY=tu_clave_real
   ```

> En Windows, si el Bloc de notas lo guarda como `.env.txt`, activá "Mostrar extensiones de archivo" y quitale el `.txt`.



**/ Linux**
```
python3 -m venv venv
source venv/bin/activate
```
Cuando está activo, la terminal muestra `(venv)` al inicio.

### 5. Instalar las dependencias
```
pip install -r requirements.txt
```
Instala Flask y Requests.

### 6. Ejecutar
```
python app.py
```
(En Mac o Linux, si no funciona: `python3 app.py`.)

Se abre el navegador en **http://127.0.0.1:5000**. Si no se abre solo, escribí esa dirección a mano. Para detener el servidor, presioná `Ctrl + C` en la terminal.

---

## Cómo se usa

1. **Recomendaciones:** elegí tipo de viaje, clima y presupuesto, y apretá **Ver destinos**. Cada tarjeta muestra el porcentaje de afinidad y por qué encaja. Podés dejar cualquier opción en "Cualquiera".
2. **Buscador:** escribí un país o una capital (sin importar tildes o mayúsculas).
3. **Sorpresa:** el botón elige un país al azar entre todos los disponibles.








