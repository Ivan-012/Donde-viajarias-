import json
import os
import random
import time
import unicodedata
from pathlib import Path

import requests
from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from datos import DESTINOS

API = "https://api.restcountries.com/countries/v5"
CAMPOS = "names,codes.alpha_2,codes.alpha_3,capitals,region,subregion,population,flag,languages,currencies"
NIVELES = ["bajo", "medio", "alto"]
TTL = 24 * 3600  # los datos de países casi no cambian: cuidamos tu cuota de la API
ARCHIVO_CACHE = Path(__file__).with_name("cache_paises.json")

app = Flask(__name__)
_cache = {"t": 0, "paises": []}


class ApiError(Exception):
    """Problema al consultar REST Countries (clave faltante, cuota, etc.)."""


def normalizar(texto):
    """Minúsculas y sin tildes, para buscar sin importar acentos."""
    s = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def leer_clave():
    """La clave puede estar en la variable de entorno o en el archivo .env."""
    clave = os.environ.get("RESTCOUNTRIES_API_KEY", "").strip()
    env = Path(__file__).with_name(".env")
    if not clave and env.exists():
        for linea in env.read_text(encoding="utf-8-sig").splitlines():
            k, _, v = linea.partition("=")
            if k.strip() == "RESTCOUNTRIES_API_KEY":
                clave = v.strip().strip("\"'")
    return clave


_CODIGO = ("iso", "bcp", "code", "alpha", "tag", "numeric", "id", "symbol", "native")


def _hojas(x, ruta=""):
    """Todos los textos de una estructura anidada, junto con su ruta (ej. 'name.english')."""
    if isinstance(x, str):
        yield ruta.lower(), x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from _hojas(v, f"{ruta}.{k}" if ruta else str(k))
    elif isinstance(x, list):
        for v in x:
            yield from _hojas(v, ruta)


def _elegir(x, claves):
    """Elige el texto más parecido a un nombre, sin importar cómo venga anidado."""
    hojas = list(_hojas(x))
    for clave in claves:
        for ruta, t in hojas:
            if clave in ruta and t.strip():
                return t
    for ruta, t in hojas:
        if not any(e in ruta for e in _CODIGO) and len(t) > 3:
            return t
    return ""


def _idiomas(l):
    items = list(l.values()) if isinstance(l, dict) else (l or [])
    nombres = [_elegir(i, ["english", "name"]) for i in items]
    return list(dict.fromkeys(n for n in nombres if n))


def _monedas(c):
    if isinstance(c, dict) and c and all(len(str(k)) == 3 and str(k).isalpha() for k in c):
        items = list(c.items())  # formato {"ARS": {...}}
    elif isinstance(c, dict):
        items = [("", c)]
    else:
        items = [("", v) for v in (c or [])]
    salida = []
    for codigo, v in items:
        hojas = list(_hojas(v))
        if isinstance(v, str):
            nombre, codigo = "", codigo or v
        else:
            nombre = _elegir(v, ["english", "name"])
            codigo = codigo or next((t for r, t in hojas if any(k in r for k in ("code", "iso", "alpha"))), "")
        simbolo = next((t for r, t in hojas if "symbol" in r), "")
        extra = ", ".join(x for x in (codigo, simbolo if simbolo != codigo else "") if x)
        texto = f"{nombre} ({extra})" if nombre and extra else (nombre or extra or next((t for _, t in hojas), ""))
        if texto:
            salida.append(texto)
    return list(dict.fromkeys(salida))


def formatear(o):
    """Convierte un país de REST Countries v5 al formato que usa nuestra web."""
    nombres = o.get("names") or {}
    spa = (nombres.get("translations") or {}).get("spa")
    spa = spa if isinstance(spa, dict) else {}
    caps = [c.get("name") if isinstance(c, dict) else c for c in o.get("capitals") or []]
    codigos = o.get("codes") or {}
    flag = o.get("flag") or {}
    a2 = (codigos.get("alpha_2") or "").lower()
    bandera = flag.get("url_svg") or flag.get("url_png") or (
        f"https://flags.restcountries.com/v5/w320/{a2}.png" if a2 else "")
    return {
        "codigo": codigos.get("alpha_3", ""),
        "nombre": spa.get("common") or nombres.get("common", ""),
        "nombre_en": nombres.get("common", ""),
        "capital": ", ".join(c for c in caps if c) or "Sin capital oficial",
        "region": o.get("subregion") or o.get("region") or "",
        "poblacion": o.get("population") or 0,
        "bandera": bandera,
        "idiomas": _idiomas(o.get("languages")),
        "monedas": _monedas(o.get("currencies")),
    }


def descargar():
    """Pide los ~250 países a la API v5, de a 100 por página (límite del plan gratis)."""
    clave = leer_clave()
    if not clave:
        raise ApiError("Falta la API key de REST Countries. Creala gratis y guardala en el archivo .env (ver README).")
    paises, offset = [], 0
    for _ in range(10):
        r = requests.get(API, headers={"Authorization": f"Bearer {clave}"}, timeout=20,
                         params={"limit": 100, "offset": offset, "response_fields": CAMPOS})
        try:
            cuerpo = r.json()
        except ValueError:
            cuerpo = {}
        if r.status_code != 200 or not isinstance(cuerpo, dict) or "data" not in cuerpo:
            errores = cuerpo.get("errors") if isinstance(cuerpo, dict) else None
            msg = errores[0].get("message") if errores else f"HTTP {r.status_code}"
            raise ApiError(f"REST Countries respondió: {msg}")
        datos = cuerpo["data"]
        paises += [formatear(o) for o in datos.get("objects", [])]
        if not (datos.get("meta") or {}).get("more"):
            break
        offset += 100
    return paises


def _con_info(paises):
    for p in paises:
        p["info"] = DESTINOS.get(p["codigo"])
    return paises


def cargar_paises():
    """Devuelve los países desde memoria, desde el archivo de caché o desde la API."""
    ahora = time.time()
    if _cache["paises"] and ahora - _cache["t"] < TTL:
        return _cache["paises"]
    if not _cache["paises"] and ARCHIVO_CACHE.exists():
        try:
            guardado = json.loads(ARCHIVO_CACHE.read_text(encoding="utf-8"))
            if guardado.get("v") == 2 and ahora - guardado["t"] < TTL and guardado["paises"]:
                _cache.update(t=guardado["t"], paises=_con_info(guardado["paises"]))
                return _cache["paises"]
        except (ValueError, KeyError, OSError):
            pass
    try:
        paises = descargar()
    except (requests.RequestException, ApiError):
        if _cache["paises"]:  # si falla la API, usamos la copia anterior
            return _cache["paises"]
        raise
    if not paises:
        raise ApiError("REST Countries no devolvió países. Revisá tu API key.")
    try:
        ARCHIVO_CACHE.write_text(json.dumps({"v": 2, "t": ahora, "paises": paises}), encoding="utf-8")
    except OSError:
        pass
    _cache.update(t=ahora, paises=_con_info(paises))
    return _cache["paises"]


@app.errorhandler(ApiError)
def error_clave(e):
    return jsonify(error=str(e)), 503


@app.errorhandler(requests.RequestException)
def error_api(_):
    return jsonify(error="No pudimos conectar con REST Countries."), 503


@app.errorhandler(Exception)
def error_general(e):
    """Las rutas /api siempre responden JSON, nunca una página HTML de error."""
    if not request.path.startswith("/api/"):
        if isinstance(e, HTTPException):
            return e
        raise e
    app.logger.exception("Error en %s", request.path)
    codigo = e.code if isinstance(e, HTTPException) else 500
    return jsonify(error=f"Error del servidor: {e}"), codigo


@app.get("/")
def inicio():
    return render_template("index.html")


@app.get("/api/recomendar")
def recomendar():
    tipo = request.args.get("tipo", "cualquiera")
    clima = request.args.get("clima", "cualquiera")
    pres = request.args.get("presupuesto", "cualquiera")
    resultados = []
    for p in cargar_paises():
        d = p["info"]
        if not d:
            continue
        puntos, razones = 0, []
        if tipo == "cualquiera" or tipo in d["tipos"]:
            puntos += 40
            if tipo != "cualquiera":
                razones.append(f"Ideal para {tipo}")
        if clima == "cualquiera" or clima in d["clima"]:
            puntos += 35
            if clima != "cualquiera":
                razones.append(f"Clima {clima}")
        if pres == "cualquiera":
            puntos += 25
        else:
            dif = abs(NIVELES.index(pres) - NIVELES.index(d["presupuesto"]))
            puntos += {0: 25, 1: 10}.get(dif, 0)
            if dif == 0:
                razones.append(f"Presupuesto {pres}")
        if puntos >= 65:  # al menos dos criterios en común
            resultados.append({**p, "puntaje": puntos, "razones": razones})
    random.shuffle(resultados)  # variedad entre destinos con igual puntaje
    resultados.sort(key=lambda x: -x["puntaje"])
    return jsonify(paises=resultados[:9])


@app.get("/api/buscar")
def buscar():
    q = normalizar(request.args.get("q", "").strip())
    if len(q) < 2:
        return jsonify(paises=[])
    hallados = [p for p in cargar_paises()
                if q in normalizar(p["nombre"]) or q in normalizar(p["nombre_en"])
                or q in normalizar(p["capital"])]
    hallados.sort(key=lambda p: p["nombre"])
    return jsonify(paises=hallados[:12])


@app.get("/api/debug")
def debug():
    """Muestra cómo manda la API los idiomas y monedas (útil si algo sale vacío)."""
    r = requests.get(API, headers={"Authorization": f"Bearer {leer_clave()}"}, timeout=20,
                     params={"limit": 1, "response_fields": "names.common,languages,currencies"})
    return jsonify(r.json())


@app.get("/api/aleatorio")
def aleatorio():
    return jsonify(paises=[random.choice(cargar_paises())])


if __name__ == "__main__":
    app.run(debug=True)
