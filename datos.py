"""Datos complementarios (curados a mano) para las recomendaciones.
REST Countries no informa clima, tipo de viaje ni costo, así que se definen acá.
Para sumar un país, agregá una línea con su código ISO de 3 letras."""

def d(clima, tipos, presupuesto, nota):
    return {"clima": clima, "tipos": tipos, "presupuesto": presupuesto, "nota": nota}

DESTINOS = {
    "ARG": d(["templado", "frio"], ["naturaleza", "aventura", "gastronomia", "ciudad"], "medio", "Glaciares, vinos y asado de punta a punta."),
    "BRA": d(["tropical"], ["playa", "naturaleza", "ciudad"], "medio", "Playas infinitas y la selva amazónica."),
    "CHL": d(["templado", "seco", "frio"], ["aventura", "naturaleza", "gastronomia"], "medio", "Del desierto de Atacama a la Patagonia."),
    "PER": d(["seco", "templado", "tropical"], ["cultura", "aventura", "gastronomia"], "bajo", "Machu Picchu y una cocina de fama mundial."),
    "COL": d(["tropical", "templado"], ["naturaleza", "playa", "ciudad", "gastronomia"], "bajo", "Caribe, café y ciudades llenas de color."),
    "MEX": d(["tropical", "seco"], ["playa", "cultura", "gastronomia"], "medio", "Ruinas mayas, cenotes y tacos."),
    "CRI": d(["tropical"], ["naturaleza", "playa", "aventura"], "medio", "Volcanes, selva y vida silvestre."),
    "CUB": d(["tropical"], ["playa", "cultura"], "bajo", "Música, autos clásicos y mar turquesa."),
    "URY": d(["templado"], ["playa", "ciudad", "gastronomia"], "medio", "Punta del Este y Colonia del Sacramento."),
    "BOL": d(["seco", "frio"], ["aventura", "cultura", "naturaleza"], "bajo", "El salar de Uyuni y paisajes de altura."),
    "ECU": d(["tropical", "templado"], ["naturaleza", "aventura"], "bajo", "Galápagos, Andes y Amazonia."),
    "ESP": d(["templado", "seco"], ["cultura", "playa", "gastronomia", "ciudad"], "medio", "Tapas, arquitectura y costas soleadas."),
    "ITA": d(["templado"], ["cultura", "gastronomia", "ciudad"], "medio", "Arte, historia y pasta en cada esquina."),
    "FRA": d(["templado"], ["cultura", "gastronomia", "ciudad"], "alto", "París, castillos y viñedos."),
    "PRT": d(["templado"], ["playa", "gastronomia", "cultura"], "medio", "Lisboa, Oporto y el Algarve."),
    "GRC": d(["templado", "seco"], ["playa", "cultura"], "medio", "Islas blancas y ruinas milenarias."),
    "DEU": d(["templado"], ["ciudad", "cultura"], "medio", "Historia, cerveza y mercados navideños."),
    "GBR": d(["templado"], ["ciudad", "cultura"], "alto", "Londres, castillos y campiña verde."),
    "ISL": d(["frio"], ["naturaleza", "aventura"], "alto", "Auroras, geiseres y cascadas."),
    "NOR": d(["frio"], ["naturaleza", "aventura"], "alto", "Fiordos y sol de medianoche."),
    "CHE": d(["frio", "templado"], ["naturaleza", "aventura", "ciudad"], "alto", "Alpes, lagos y trenes panorámicos."),
    "HRV": d(["templado"], ["playa", "cultura"], "medio", "Costa adriática y murallas medievales."),
    "TUR": d(["templado", "seco"], ["cultura", "gastronomia", "playa"], "bajo", "Estambul, Capadocia y la costa turquesa."),
    "EGY": d(["seco"], ["cultura", "aventura"], "bajo", "Pirámides, templos y el río Nilo."),
    "MAR": d(["seco", "templado"], ["cultura", "gastronomia", "aventura"], "bajo", "Zocos, desierto y ciudades de colores."),
    "ZAF": d(["templado"], ["naturaleza", "aventura", "playa"], "medio", "Safaris, viñedos y Ciudad del Cabo."),
    "KEN": d(["tropical"], ["naturaleza", "aventura"], "medio", "Safari y la gran migración."),
    "JPN": d(["templado"], ["cultura", "gastronomia", "ciudad"], "alto", "Templos, tecnología y sushi."),
    "THA": d(["tropical"], ["playa", "gastronomia", "cultura"], "bajo", "Islas paradisíacas y comida callejera."),
    "VNM": d(["tropical"], ["gastronomia", "naturaleza", "cultura"], "bajo", "Bahía de Ha Long y ciudades vibrantes."),
    "IND": d(["tropical", "seco"], ["cultura", "gastronomia", "aventura"], "bajo", "Palacios, especias y el Taj Mahal."),
    "IDN": d(["tropical"], ["playa", "naturaleza", "aventura"], "bajo", "Bali, volcanes y arrozales."),
    "ARE": d(["seco"], ["ciudad", "playa"], "alto", "Rascacielos, desierto y lujo."),
    "AUS": d(["templado", "tropical", "seco"], ["playa", "naturaleza", "aventura", "ciudad"], "alto", "Gran Barrera de Coral y el outback."),
    "NZL": d(["templado", "frio"], ["naturaleza", "aventura"], "alto", "Paisajes de película y deportes extremos."),
    "CAN": d(["frio"], ["naturaleza", "ciudad", "aventura"], "alto", "Montañas Rocosas, lagos y Toronto."),
    "USA": d(["templado"], ["ciudad", "naturaleza", "aventura"], "alto", "Nueva York, parques nacionales y rutas épicas."),
    "MDV": d(["tropical"], ["playa"], "alto", "Bungalós sobre aguas cristalinas."),
}
