# -*- coding: utf-8 -*-
"""Modelo de datos del plan de reinicio R1-R5 para la app movil.

Arranque el 20 de agosto de 2026 y cierre el 28 de octubre: 70 dias en cinco
bloques de catorce.

Tres ejes que pidio Pelayo y como se han metido sin saltarse el protocolo:

1. VELOCIDAD (arrancada y aceleracion). Es su fuerte. Entra en R3 en forma de
   aceleracion progresiva, se hace protagonista en R4 con arrancadas desde
   parado y velocidad lanzada, y en R5 queda como sprint de calidad. Nunca
   antes de R3: el sprint carga el complejo recto abdominal-aductor en cada
   zancada y necesita el aductor con fuerza real por debajo.

2. GOLPEO Y BALON PARADO (faltas y corners, lo suyo). Aqui esta el riesgo
   mayor de toda la readaptacion. El golpeo con empeine es EL gesto de la
   pubalgia atletica: extension de cadera, rotacion de pelvis y frenada del
   recto abdominal, todo a la vez y a maxima velocidad. Por eso la progresion
   es larga: pases en R3, golpeo raso y medio al final de R3, golpeo alto en
   R4, y el balon parado (faltas y corners) SOLO en la segunda semana de R4 y
   en R5, en series cortas y contadas. El dia siguiente manda.

3. TREN SUPERIOR. Cuatro sesiones semanales en R1 y R2 y no se abandona en
   ningun bloque: espalda, pecho, hombro y brazo con volumen de verdad. Es lo
   que se puede cargar sin tocar la ingle, asi que es donde se gana masa
   mientras la pelvis se recupera.
"""

BLOQUES = [
    dict(id="R1", nombre="Descarga y control", desde="2026-08-20", dias=14,
         lema="Bajar la irritación del tejido y volver a tolerar carga isométrica, sin perder masa por el camino.",
         fuera=["Balón", "Golpeo", "Sprint", "Arrancadas", "Cambios de dirección",
                "Pliometría", "Copenhagen", "Sentadilla", "Zancada",
                "Aductores en máquina", "Braza"],
         puerta=["Dolor en reposo 0-1 durante cinco días seguidos",
                 "Tos y estornudo sin dolor",
                 "Squeeze máximo 2 o menos",
                 "Isométrico al 80 % sin reacción al día siguiente",
                 "Siete días seguidos de registro completo"]),
    dict(id="R2", nombre="Base y fuerza", desde="2026-09-03", dias=14,
         lema="El aductor empieza a coger fuerza de verdad y el pie vuelve a golpear el suelo, todavía solo en recta.",
         fuera=["Balón", "Golpeo", "Sprint", "Arrancadas", "Cambios de dirección",
                "Pliometría"],
         puerta=["Copenhagen corto 3 × 10 por lado sin reacción",
                 "Carrera continua 20 min sin reacción",
                 "Squeeze máximo 0-1",
                 "Split squat y RDL sin molestia inguinal",
                 "Progresivos al 70 % sin notar la ingle"]),
    dict(id="R3", nombre="Construcción y velocidad", desde="2026-09-17", dias=14,
         lema="Aceleras por primera vez y recuperas el balón. El golpeo se queda raso y nada de balón quieto.",
         fuera=["Sprint máximo", "Balón parado", "Faltas y córners", "Golpeo alto",
                "COD de 135 y 180°", "Oposición"],
         puerta=["Copenhagen largo 3 × 6-8 por lado sin reacción",
                 "Aceleración de 20 m al 85 % sin dolor",
                 "Cambio de dirección de 90° sin protegerte",
                 "Golpeo raso al 60 % sin reacción a 24 h",
                 "Dos sesiones de campo en una semana sin peaje"]),
    dict(id="R4", nombre="Específica: velocidad y golpeo", desde="2026-10-01", dias=14,
         lema="Arrancas desde parado, corres lanzado y golpeas con empeine. Las faltas llegan en la segunda semana.",
         fuera=["Partido", "Contacto real", "Series largas de faltas"],
         puerta=["Checklist pre-competición completo",
                 "Arrancada y sprint al 95 % sin dolor",
                 "COD de 45, 90, 135 y 180° sin protegerte",
                 "Ocho faltas seguidas al 80 % sin reacción a 24-48 h",
                 "Tres sesiones de campo en una semana sin empeorar"]),
    dict(id="R5", nombre="Competitiva", desde="2026-10-15", dias=14,
         lema="Minutos de partido y golpeo sin freno, aunque las faltas se siguen contando una a una.",
         fuera=["Partido completo antes de cerrar el checklist",
                "Más de 12 faltas seguidas"],
         puerta=["Minutos superados sin reacción al día siguiente en cada escalón",
                 "Partido completo sin peaje 48 h después"]),
]

from fichas_app import EJ  # noqa: E402

# ── movilidad y activación ───────────────────────────────────────────
MOV_BASE = [
    ("90-90-cadera", "90/90 de cadera", "2 min / lado", ""),
    ("adductor-rockback", "Adductor rockback", "2 × 10 / lado", ""),
    ("movilidad-cadera-pie", "Cadera activa de pie", "2 min", ""),
    ("brace-respiracion", "Brace con respiración 360°", "3 × 8", ""),
    ("isometrico-aductor", "Aducción isométrica", "5 × 30 s", "CLAVE"),
    ("puente-gluteo", "Puente de glúteo", "2 × 15", ""),
    ("pallof-press", "Pallof press", "2 × 10 / lado", ""),
]
MOV_CORTA = MOV_BASE[:2] + MOV_BASE[3:6]
MOV_LARGA = MOV_BASE + [
    ("dead-bug", "Dead bug lento", "3 × 8 / lado", ""),
    ("plancha-lateral", "Plancha lateral corta", "3 × 25 s / lado", ""),
]
# calentamiento previo a velocidad o golpeo: mas largo y mas activo
CALIENTA_CAMPO = [
    ("movilidad-cadera-pie", "Movilidad activa de cadera", "3 min", ""),
    ("trote-progresivo", "Trote progresivo", "8 min", ""),
    ("skipping-tecnica", "Skipping, talones y zancada lateral", "3 × 20 m", ""),
    ("isometrico-aductor", "Aducción isométrica de activación", "3 × 20 s", "CLAVE"),
    ("progresivos-40m", "Progresivos de 40 m", "4 al 60, 70, 80 y 85 %", ""),
]

# ── gimnasio: espalda, pecho, hombro y brazo con volumen ─────────────
PLAN_A = [   # empuje
    ("press-pecho-maquina", "Press de pecho en máquina", "4 × 8-10", ""),
    ("press-inclinado-mancuernas", "Press inclinado con mancuernas", "4 × 8-10", ""),
    ("aperturas", "Aperturas en máquina o con mancuernas", "3 × 12", ""),
    ("press-militar-maquina", "Press militar en máquina", "4 × 8-10", ""),
    ("elevaciones-laterales", "Elevaciones laterales", "4 × 12-15", ""),
    ("fondos-asistidos", "Fondos en paralelas asistidos", "3 × 8-10", ""),
    ("triceps-polea", "Extensión de tríceps en polea", "3 × 12-15", ""),
    ("triceps-sobre-cabeza", "Extensión de tríceps sobre la cabeza", "3 × 12", ""),
    ("curl-femoral", "Curl femoral en máquina", "3 × 12", ""),
    ("extension-cuadriceps", "Extensión de cuádriceps", "3 × 12", ""),
]
PLAN_B = [   # tirón
    ("jalon-al-pecho", "Jalón al pecho agarre amplio", "4 × 8-10", ""),
    ("remo-maquina-neutro", "Remo en máquina agarre neutro", "4 × 8-10", ""),
    ("remo-mancuerna", "Remo con mancuerna a una mano", "3 × 10-12", ""),
    ("pullover-polea", "Pullover en polea alta", "3 × 12", ""),
    ("face-pull", "Face pull en polea", "3 × 15", ""),
    ("elevaciones-posteriores", "Elevaciones posteriores de hombro", "3 × 15", ""),
    ("curl-biceps-inclinado", "Curl de bíceps en banco inclinado", "3 × 10", ""),
    ("curl-martillo", "Curl martillo alterno", "3 × 12", ""),
    ("curl-predicador", "Curl en banco predicador", "3 × 12", ""),
    ("gemelo-de-pie", "Gemelo de pie", "3 × 15", ""),
]
PLAN_D = [   # upper extra, día de acumular volumen arriba
    ("press-militar-maquina", "Press militar en máquina", "4 × 10-12", ""),
    ("elevaciones-laterales", "Elevaciones laterales", "4 × 15", ""),
    ("elevaciones-posteriores", "Elevaciones posteriores de hombro", "3 × 15", ""),
    ("face-pull", "Face pull alto", "3 × 15", ""),
    ("encogimientos-trapecio", "Encogimientos de trapecio", "3 × 15", ""),
    ("triceps-polea", "Extensión de tríceps en polea", "3 × 15", ""),
    ("curl-martillo", "Curl martillo alterno", "3 × 12", ""),
    ("curl-muneca", "Curl de muñeca y antebrazo", "3 × 15", ""),
    ("gemelo-de-pie", "Gemelo de pie", "4 × 15", ""),
]
PLAN_C = [   # pierna, desde R2
    ("prensa-pies-altos", "Prensa 45° con pies altos", "4 × 10-12", ""),
    ("peso-muerto-rumano", "Peso muerto rumano con mancuernas", "4 × 8-10", ""),
    ("split-squat", "Split squat corto", "3 × 8 / lado", ""),
    ("curl-femoral", "Curl femoral en máquina", "3 × 12", ""),
    ("hip-thrust", "Hip thrust", "3 × 12", ""),
    ("gemelo-de-pie", "Gemelo de pie", "4 × 15", ""),
    ("pallof-press", "Pallof press", "3 × 12 / lado", ""),
]
PLAN_C_POT = [   # pierna con potencia, desde R4
    ("prensa-pies-altos", "Prensa 45° explosiva en la subida", "4 × 6", ""),
    ("peso-muerto-rumano", "Peso muerto rumano", "4 × 6-8", ""),
    ("step-up-alto", "Step-up alto con impulso", "3 × 8 / lado", ""),
    ("nordic-hamstring", "Nordic hamstring asistido", "3 × 5", ""),
    ("hip-thrust", "Hip thrust pesado", "4 × 8", ""),
    ("gemelo-de-pie", "Gemelo de pie", "4 × 12", ""),
]

# ── agua y aparatos ─────────────────────────────────────────────────
PISCINA_25 = ["5 min nado espalda suave.",
              "10 min aqua running lento en agua profunda. Deberías poder hablar.",
              "5 min marching alto en agua a la cadera.",
              "5 min flotación pasiva y respiración."]
PISCINA_35 = ["5 min nado espalda de calentamiento.",
              "15 min agua profunda: aqua running y rodillas al pecho.",
              "10 min agua media: marching y aducciones suaves con flotador.",
              "5 min flotación pasiva."]
PISCINA_40 = ["5 min nado espalda.",
              "15 min agua profunda: aqua running, cross country, tijeras.",
              "15 min agua media: marching, aducciones, sentadilla acuática.",
              "5 min nado espalda de vuelta a la calma."]
PISTOLA = ["Dorsal y trapecio inferior, que es lo que acabas de trabajar.",
           "Cuádriceps, barrido lento de rodilla hacia arriba.",
           "Isquiosurales, de rodilla a glúteo.",
           "Glúteo mayor y medio, puntos densos sin clavar.",
           "Aductor solo en la mitad del muslo. Nunca los últimos 3-4 cm hacia el pubis."]
EMS_REC = ["Recuperación activa 3-9 Hz sobre aductores y glúteos, 20 min.",
           "Intensidad: contracción visible, sin dolor.",
           "Electrodos nunca sobre pubis, ingle ni genitales."]
CIERRE = ["Movilidad suave de cadera, 5 min.",
          "Máquina de masaje de espalda, 5-10 min en dorsal y lumbar.",
          "Shiatsu de pies si apetece."]

FISIO_VAL = [("Valoración, no solo masaje",
              "Palpación de inserción y sínfisis, test de squeeze, descarte de hernia y su criterio sobre imagen."),
             ("Manual en cadena posterior", "Glúteo medio y TFL. Descargan el aductor sin irritarlo."),
             ("Su criterio de carga", "¿Ve bien los isométricos? ¿Cuándo metería Copenhagen corto?")]
FISIO_LOC = [("Zona local, con presión suave",
              "Aductor y abdominal bajo. Máximo dos veces por semana."),
             ("Cadena posterior", "Glúteo medio, TFL, cuadrado lumbar, psoas."),
             ("Registrar la reacción", "Si mañana duele más que hoy, la dosis fue excesiva.")]
FISIO_DES = [("Descarga general post-gimnasio", "Cadena posterior y lo que hayas trabajado."),
             ("Sin zona local hoy", "Se reserva para el día de rehab larga.")]
FISIO_VEL = [("Antes de velocidad, solo activación",
              "Movilización suave y activación. El masaje profundo antes de correr deja el músculo sin tono."),
             ("Después, descarga de aductor y psoas",
              "Es lo que más acusa la arrancada."),
             ("Preguntar por el golpeo",
              "Que te palpe la inserción del recto abdominal después de un día de golpeo.")]



# ── core: tres niveles segun el bloque ───────────────────────────────
CORE_BASE = [        # R1: nada que cargue la insercion
    ("brace-respiracion", "Brace con respiración 360°", "3 × 8", ""),
    ("bicho-muerto-cruzado", "Dead bug isométrico con presión", "5 × 10 s", "SEGURO"),
    ("bird-dog", "Bird dog", "3 × 10 / lado", ""),
    ("plancha-lateral", "Plancha lateral corta", "3 × 25 s / lado", ""),
    ("plancha-frontal", "Plancha frontal", "3 × 25 s", ""),
]
CORE_MEDIO = [       # R2 y R3
    ("dead-bug", "Dead bug lento", "3 × 8 / lado", ""),
    ("dead-bug-banda", "Dead bug con banda", "3 × 8 / lado", "NUEVO"),
    ("plancha-hombro", "Plancha con toque de hombro", "3 × 8 / lado", ""),
    ("plancha-lateral-pie", "Plancha lateral con piernas estiradas", "3 × 30 s / lado", ""),
    ("pallof-rotacion", "Pallof de rodillas", "3 × 10 / lado", ""),
    ("elevacion-piernas", "Bajada de piernas controlada", "3 × 8", ""),
]
CORE_FUERTE = [      # R4 y R5
    ("hollow-hold", "Hollow hold", "3 × 25 s", ""),
    ("rueda-abdominal", "Rueda abdominal de rodillas", "3 × 6", "EXIGENTE"),
    ("elevacion-piernas", "Bajada de piernas controlada", "3 × 10", ""),
    ("plancha-hombro", "Plancha con toque de hombro", "3 × 10 / lado", ""),
    ("pallof-rotacion", "Pallof de rodillas", "3 × 12 / lado", ""),
]

# ── aductor y pubis: progresion por bloque ───────────────────────────
PUBIS_R1 = [
    ("squeeze-45", "Squeeze a 45 grados", "5 × 30 s", "CLAVE"),
    ("puente-una-pierna", "Puente a una pierna", "3 × 10 / lado", ""),
    ("adductor-rockback-banda", "Rockback con banda", "2 × 10 / lado", ""),
]
PUBIS_R2 = [
    ("squeeze-45", "Squeeze a 45 grados", "5 × 40 s", "CLAVE"),
    ("squeeze-90", "Squeeze a 90 grados", "4 × 30 s", "NUEVO"),
    ("copenhagen-corto", "Copenhagen corto", "3 × 8 / lado", ""),
    ("aductor-maquina", "Aductor en máquina", "3 × 12", "NUEVO"),
    ("marcha-puente", "Marcha en puente", "3 × 8 / lado", ""),
]
PUBIS_R3 = [
    ("squeeze-90", "Squeeze a 90 grados", "4 × 40 s", ""),
    ("squeeze-piernas-rectas", "Squeeze con piernas rectas", "4 × 30 s", "NUEVO"),
    ("copenhagen-largo", "Copenhagen largo", "3 × 6 / lado", ""),
    ("aductor-excentrico", "Aductor excéntrico con banda", "3 × 8 / lado", ""),
    ("deslizamiento-lateral", "Deslizamiento lateral con disco", "3 × 8 / lado", "NUEVO"),
]
PUBIS_MANT = [
    ("squeeze-piernas-rectas", "Squeeze con piernas rectas", "3 × 40 s", ""),
    ("copenhagen-largo", "Copenhagen largo", "3 × 8 / lado", ""),
    ("aductor-maquina", "Aductor en máquina", "3 × 15", ""),
    ("deslizamiento-lateral", "Deslizamiento lateral con disco", "3 × 10 / lado", ""),
]

# ── estiramientos: lo que tira de la pelvis, no el aductor ───────────
ESTIRA_BASE = [
    ("estiramiento-gato-camello", "Gato y camello", "10 ciclos", ""),
    ("estiramiento-psoas", "Estiramiento de psoas", "2 × 30 s / lado", "EL MÁS IMPORTANTE"),
    ("estiramiento-piramidal", "Estiramiento de piramidal", "30 s / lado", ""),
    ("estiramiento-cuadrado-lumbar", "Estiramiento de cuadrado lumbar", "30 s / lado", ""),
    ("respiracion-90-90", "Respiración 90/90", "5 min", ""),
]
ESTIRA_COMPLETO = [
    ("estiramiento-gato-camello", "Gato y camello", "10 ciclos", ""),
    ("estiramiento-psoas", "Estiramiento de psoas", "2 × 30 s / lado", "EL MÁS IMPORTANTE"),
    ("estiramiento-recto-femoral", "Estiramiento de recto femoral", "30 s / lado", ""),
    ("estiramiento-isquios", "Estiramiento de isquios", "30 s / lado", ""),
    ("estiramiento-piramidal", "Estiramiento de piramidal", "30 s / lado", ""),
    ("estiramiento-cuadrado-lumbar", "Estiramiento de cuadrado lumbar", "30 s / lado", ""),
    ("estiramiento-aductor-suave", "Estiramiento suave de aductor", "2 × 30 s", "SOLO SI DOLOR 0-2"),
    ("respiracion-90-90", "Respiración 90/90", "5 min", ""),
]

# ── futbol: tecnica por bloque ───────────────────────────────────────
FUTBOL_R3A = [
    ("control-orientado", "Control orientado", "10 min", ""),
    ("pase-interior", "Pase con el interior", "10 min", ""),
    ("conduccion-conos", "Conducción entre conos", "10 min", ""),
]
FUTBOL_R3B = [
    ("control-orientado", "Control orientado", "8 min", ""),
    ("pase-interior", "Pase con el interior", "8 min", ""),
    ("pase-largo", "Pase largo raso", "12-15 golpeos al 50-60 %", "NUEVO"),
]
FUTBOL_R4A = [
    ("conduccion-conos", "Conducción rápida entre conos", "10 min", ""),
    ("pase-largo", "Pase largo", "12 golpeos al 70 %", ""),
    ("golpeo-empeine", "Golpeo con empeine", "12-15 al 70-80 %", "NUEVO"),
]
FUTBOL_R4B = [
    ("falta-balon-parado", "Falta con balón parado", "6-8 al 70-80 %", "TECHO 16"),
    ("centro-banda", "Centro desde banda", "6-8 centros", "NUEVO"),
    ("remate-cabeza", "Remate de cabeza", "6 remates", "NUEVO"),
]
FUTBOL_R5 = [
    ("falta-balon-parado", "Falta con balón parado", "10-12 libres", "TECHO 12"),
    ("centro-banda", "Córner y centro", "8-10", ""),
    ("golpeo-empeine", "Finalización", "10 disparos al 100 %", ""),
]


def sesion(titulo, regla, secciones):
    return dict(titulo=titulo, regla=regla, secciones=secciones)


def sec(n, titulo, meta, tipo, items, fotos=None):
    """fotos: slugs que se pintan como tira de miniaturas encima del contenido.
    Sirve para las secciones de texto (piscina, aparatos, fisio, comida), que
    tenian foto en el manual pero no la ensenaban en la sesion del dia."""
    return dict(n=n, titulo=titulo, meta=meta, tipo=tipo, items=items,
                fotos=fotos or [])


FOTOS_PISCINA = ["nado-espalda", "aqua-running", "marching-agua", "flotacion-pasiva"]
FOTOS_PISTOLA = ["pistola-cuadriceps", "pistola-aductor"]
FOTOS_EMS = ["ems-aductores", "ems-gluteos"]
FOTOS_FISIO = ["fisio-gluteo-medio"]
FOTOS_CIERRE = ["movilidad-nocturna", "masaje-espalda-maquina"]
FOTOS_COMIDA = ["plato-modelo", "post-entreno"]


MICRO = {}

# El dia 1 de R1 no sigue el microciclo: caiga en el dia de la semana que caiga,
# es el dia de la linea base y de la valoracion del fisio. Sin esos numeros el
# semaforo del protocolo no tiene con que decidir el resto del bloque.
APERTURA = sesion(
    "Línea base y arranque",
    "Lo que cuenta hoy no es el peso que muevas, son los cuatro números que dejes escritos "
    "antes de empezar. Llevas ocho semanas sin ellos.",
    [sec("01", "Línea base", "10 min · antes de nada", "test", []),
     sec("02", "Movilidad y activación", "20 min", "tabla", MOV_BASE),
     sec("03", "Gimnasio · Plan A empuje", "45 min · RIR 3", "tabla", PLAN_A[:7]),
     sec("04", "Piscina", "25 min", "lista", PISCINA_25, FOTOS_PISCINA),
     sec("05", "Fisioterapia · valoración", "la sesión más importante del bloque",
         "pasos", FISIO_VAL, FOTOS_FISIO),
     sec("06", "Electroestimulación", "20 min · tarde", "lista", EMS_REC, FOTOS_EMS)])

# ══ R1 · descarga y control ═════════════════════════════════════════
MICRO["R1"] = {
 0: sesion("Empuje + agua",
           "Diez días parado se pagan la primera semana. RIR 3, cargas al 60-70 %, y ni un kilo de más por encontrarte bien.",
           [sec("02", "Movilidad y activación", "20 min", "tabla", MOV_BASE),
            sec("03", "Gimnasio · Plan A empuje", "50 min · RIR 3", "tabla", PLAN_A),
            sec("04", "Piscina", "25 min", "lista", PISCINA_25, FOTOS_PISCINA),
            sec("05", "Fisioterapia", "sesión de hoy", "pasos", FISIO_VAL, FOTOS_FISIO),
            sec("06", "Electroestimulación", "20 min · tarde", "lista", EMS_REC, FOTOS_EMS)]),
 1: sesion("Tirón + descarga con pistola",
           "Compara el número de esta mañana con el de ayer. Eso te dice más que todas las series juntas.",
           [sec("02", "Movilidad y activación", "18 min", "tabla",
                MOV_BASE + [("dead-bug", "Dead bug lento", "2 × 8 / lado", "")]),
            sec("03", "Gimnasio · Plan B tirón", "50 min · RIR 3", "tabla", PLAN_B),
            sec("04", "Pistola de masaje", "10 min · post-gym", "lista", PISTOLA, FOTOS_PISTOLA),
            sec("06", "Cierre del día", "10 min", "lista", CIERRE, FOTOS_CIERRE)]),
 2: sesion("Rehab larga + agua + fisio local",
           "Hoy se junta todo lo específico: cuarenta minutos de rehab, treinta y cinco de agua y el fisio tocando la zona. Si un día vas justo de tiempo, que no sea este.",
           [sec("02", "Rehab de aductor y core", "40 min", "tabla", MOV_LARGA),
            sec("04", "Piscina", "35 min", "lista", PISCINA_35, FOTOS_PISCINA),
            sec("05", "Fisioterapia · zona local", "una de las dos de la semana", "pasos", FISIO_LOC, FOTOS_FISIO),
            sec("06", "EMS y shiatsu", "30 min · tarde", "lista",
                EMS_REC + ["Shiatsu lumbar y dorsal 15 min."], FOTOS_EMS + FOTOS_CIERRE[1:])]),
 3: sesion("Upper extra",
           "Hombro, brazo y trapecio. Nada de esto pasa cerca de la ingle, así que hoy puedes apretar sin mirar de reojo.",
           [sec("02", "Movilidad y activación", "15 min", "tabla", MOV_CORTA),
            sec("03", "Gimnasio · Plan D upper extra", "45 min · RIR 2-3", "tabla", PLAN_D),
            sec("04", "Pistola de masaje", "8 min", "lista", PISTOLA, FOTOS_PISTOLA)]),
 4: sesion("Empuje o tirón + agua",
           "Coge el plan que menos hayas repetido esta semana y mantén el RIR de siempre.",
           [sec("02", "Movilidad y activación", "18 min", "tabla", MOV_BASE),
            sec("03", "Gimnasio · Plan A o B", "50 min · RIR 3", "tabla", PLAN_A),
            sec("04", "Piscina", "25 min", "lista", PISCINA_25, FOTOS_PISCINA),
            sec("05", "Fisioterapia · descarga", "post-gimnasio", "pasos", FISIO_DES, FOTOS_FISIO),
            sec("06", "Electroestimulación", "20 min", "lista", EMS_REC, FOTOS_EMS)]),
 5: sesion("Agua larga + brazo",
           "Cuarenta minutos de agua, que es donde más volumen entra sin que te lo cobren mañana. El brazo, al salir.",
           [sec("02", "Movilidad y activación", "20 min", "tabla", MOV_BASE),
            sec("04", "Piscina", "40 min", "lista", PISCINA_40, FOTOS_PISCINA),
            sec("03", "Gimnasio · brazo y hombro", "25 min", "tabla", PLAN_D[:5]),
            sec("06", "Shiatsu completo", "30 min · noche", "lista",
                ["Cervical, dorsal y lumbar, 30 min.", "Shiatsu de pies.", "Hidratar después."])]),
 6: sesion("Descanso y test semanal",
           "Hoy no se entrena. Se rellena el test y con eso se decide si la semana que viene sube, mantiene o baja.",
           [sec("02", "Movilidad suave", "15 min", "tabla", MOV_CORTA),
            sec("09", "Test semanal", "rellenar", "test", [])]),
}

# ══ R2 · base y fuerza ══════════════════════════════════════════════
MICRO["R2"] = {
 0: sesion("Pierna completa + empuje",
           "La pierna regresa al gimnasio después de dos semanas. Rango completo y técnica limpia antes que cargar la barra.",
           [sec("02", "Movilidad y activación", "18 min", "tabla", MOV_BASE),
            sec("03", "Gimnasio · Plan C pierna", "45 min · RIR 2", "tabla", PLAN_C),
            sec("03b", "Gimnasio · empuje corto", "20 min", "tabla", PLAN_A[:4]),
            sec("06", "Electroestimulación", "20 min", "lista", EMS_REC, FOTOS_EMS)]),
 1: sesion("Tirón + carrera lineal",
           "Hoy corres por primera vez desde junio. Solo recta, sin cambios de ritmo y sin acelerones.",
           [sec("02", "Movilidad y activación", "18 min", "tabla", MOV_BASE),
            sec("03", "Gimnasio · Plan B tirón", "50 min · RIR 2", "tabla", PLAN_B),
            sec("07", "Campo · carrera lineal", "parque · 25 min", "lista",
                ["Calentamiento 8 min de trote muy suave.",
                 "8 × 60 m al 60 %, andando la vuelta.",
                 "Nada de arrancar fuerte: se entra progresivo en cada recta.",
                 "Vuelta a la calma 5 min y movilidad."])]),
 2: sesion("Copenhagen + core + agua",
           "Llega el Copenhagen. Empieza por el corto y no pases al largo hasta encadenar tres semanas con el día siguiente limpio.",
           [sec("02", "Rehab de aductor y core", "35 min", "tabla",
                MOV_BASE + [("copenhagen-corto", "Copenhagen corto", "2 × 6 / lado", "NUEVO"),
                            ("aductor-banda", "Aductor con banda", "3 × 12 / lado", "")]),
            sec("04", "Piscina", "25 min", "lista", PISCINA_25, FOTOS_PISCINA),
            sec("05", "Fisioterapia · zona local", "una de las dos de la semana", "pasos", FISIO_LOC, FOTOS_FISIO)]),
 3: sesion("Upper extra + carrera continua",
           "Trabajo largo de tren superior y una carrera que puedas hacer hablando. Los progresivos aún no.",
           [sec("02", "Movilidad y activación", "15 min", "tabla", MOV_CORTA),
            sec("03", "Gimnasio · Plan D upper extra", "45 min", "tabla", PLAN_D),
            sec("07", "Campo · carrera continua", "parque", "lista",
                ["12-20 min a ritmo cómodo, hablando sin ahogarte.",
                 "Terreno liso. Nada de cuestas ni cambios de ritmo."])]),
 4: sesion("Pierna ligera + Copenhagen + agua",
           "Segunda dosis de Copenhagen, con la pierna en volumen bajo para que llegue fresca.",
           [sec("02", "Rehab de aductor y core", "30 min", "tabla",
                MOV_BASE + [("copenhagen-corto", "Copenhagen corto", "2 × 8 / lado", "")]),
            sec("03", "Gimnasio · Plan C ligero", "30 min · RIR 3", "tabla", PLAN_C[:4]),
            sec("04", "Piscina", "25 min", "lista", PISCINA_25, FOTOS_PISCINA)]),
 5: sesion("Carrera con progresivos + tirón corto",
           "Te acercas a la velocidad por primera vez. Progresivos suaves y sin pasar del 70 %.",
           [sec("02", "Movilidad y activación", "20 min", "tabla", MOV_BASE),
            sec("07", "Campo · progresivos", "parque · 30 min", "lista",
                ["15-20 min de carrera continua.",
                 "6 progresivos de 60 m: se entra suave y se acaba al 70 %.",
                 "Andando la vuelta entera. Si la ingle avisa, se corta el bloque."]),
            sec("03", "Gimnasio · tirón corto", "25 min", "tabla", PLAN_B[:5]),
            sec("06", "Pistola y shiatsu", "20 min", "lista", PISTOLA, FOTOS_PISTOLA)]),
 6: sesion("Descanso y test semanal",
           "Día libre y test. Si la puerta del bloque anda cerca, hoy se repasan los criterios uno por uno.",
           [sec("02", "Movilidad suave", "15 min", "tabla", MOV_CORTA),
            sec("09", "Test semanal", "rellenar", "test", [])]),
}

# ══ R3 · construcción y velocidad ═══════════════════════════════════
MICRO["R3"] = {
 0: sesion("Fuerza pesada + Copenhagen largo",
           "El Copenhagen pasa a palanca larga. De este ejercicio dependen la arrancada y el golpeo, así que no hay prisa por subirlo.",
           [sec("02", "Movilidad y activación", "18 min", "tabla", MOV_BASE),
            sec("03", "Gimnasio · Plan C pierna", "45 min · RIR 2", "tabla", PLAN_C),
            sec("03b", "Gimnasio · empuje", "25 min", "tabla", PLAN_A[:5]),
            sec("08", "Aductor específico", "15 min", "tabla",
                [("copenhagen-largo", "Copenhagen largo", "3 × 6 / lado", "NUEVO"),
                 ("aductor-excentrico", "Aductor excéntrico con banda", "3 × 8 / lado", "")])]),
 1: sesion("Balón: control y pase",
           "Hoy tocas balón otra vez. Solo control y pase, y el golpeo empieza raso y corto.",
           [sec("02", "Movilidad y activación", "15 min", "tabla", MOV_CORTA),
            sec("07", "Campo · técnica y pase", "40 min", "lista",
                ["Carrera tempo 15 min a ritmo moderado.",
                 "Pases contra pared con interior, las dos piernas, 10 min.",
                 "Control orientado y primer toque, 10 min.",
                 "Conducción amplia entre conos, sin cambios bruscos.",
                 "Golpeo raso al 40 %, 10-12 golpeos. Nada de empeine alto."]),
            sec("03", "Gimnasio · tirón corto", "25 min", "tabla", PLAN_B[:5])]),
 2: sesion("Aductor y core + agua",
           "Sesión de mantenimiento entre los dos días de campo. Poco vistosa y de las que más sostienen.",
           [sec("02", "Rehab de aductor y core", "35 min", "tabla",
                MOV_LARGA + [("copenhagen-largo", "Copenhagen largo", "3 × 6 / lado", "")]),
            sec("04", "Piscina", "25 min", "lista", PISCINA_25, FOTOS_PISCINA),
            sec("05", "Fisioterapia · zona local", "una de las dos de la semana", "pasos", FISIO_LOC, FOTOS_FISIO)]),
 3: sesion("Aceleración y frenada",
           "Hoy aceleras de verdad por primera vez. Se entra progresivo en cada recta y se frena en tres o cuatro pasos, nunca en seco.",
           [sec("02", "Calentamiento de campo", "20 min", "tabla", CALIENTA_CAMPO),
            sec("07", "Campo · aceleración", "35 min", "lista",
                ["6-8 × 10 m al 70-80 %, saliendo de pie y sin explosión.",
                 "4-6 × 20 m al 75-85 %, entrando progresivo.",
                 "6 frenadas desde 15 m, parando en 3-4 pasos, nunca en seco.",
                 "Cambios de dirección de 45°, ocho por lado.",
                 "Andando la vuelta siempre. Recuperación completa entre series."]),
            sec("05", "Fisioterapia", "descarga de aductor y psoas", "pasos", FISIO_VEL, FOTOS_FISIO)]),
 4: sesion("Upper extra + golpeo raso",
           "Tren superior largo y segunda tanda de golpeo, todavía raso y a media distancia.",
           [sec("02", "Movilidad y activación", "15 min", "tabla", MOV_CORTA),
            sec("03", "Gimnasio · Plan D upper extra", "45 min", "tabla", PLAN_D),
            sec("07", "Campo · golpeo raso", "25 min", "lista",
                ["Calentamiento 10 min con movilidad de cadera.",
                 "Pases largos rasos, 12-15 golpeos al 50-60 %.",
                 "Interior y empeine bajo. Sin balón parado y sin buscar altura.",
                 "Cortar si el dolor pasa de 2 o si notas tirón en el abdominal bajo."])]),
 5: sesion("Campo: agilidad y conducción",
           "Cambios de dirección de 45 y luego de 90 grados, con balón y sin nadie enfrente.",
           [sec("02", "Calentamiento de campo", "20 min", "tabla", CALIENTA_CAMPO),
            sec("07", "Campo · agilidad", "40 min", "lista",
                ["Cambios de dirección de 45° y luego 90°, ocho por lado.",
                 "Conducción con cambios de ritmo suaves, 10 min.",
                 "Regate en espacio amplio, sin duelo y sin oposición.",
                 "Sin sprint máximo y sin 135 ni 180°."])]),
 6: sesion("Descanso y test semanal",
           "Día libre y test semanal.",
           [sec("02", "Movilidad suave", "15 min", "tabla", MOV_CORTA),
            sec("09", "Test semanal", "rellenar", "test", [])]),
}

# ══ R4 · específica: velocidad y golpeo ═════════════════════════════
MICRO["R4"] = {
 0: sesion("Potencia + arrancada",
           "Fuerza explosiva arriba y abajo, y arrancadas cortas al final. En fresco, que es la única forma de entrenar una salida.",
           [sec("02", "Movilidad y activación", "18 min", "tabla", MOV_BASE),
            sec("03", "Gimnasio · pierna con potencia", "45 min · RIR 2", "tabla", PLAN_C_POT),
            sec("03b", "Gimnasio · empuje", "25 min", "tabla", PLAN_A[:5]),
            sec("07", "Campo · arrancada", "20 min", "lista",
                ["6-8 salidas de 10 m desde parado, al 85-90 %.",
                 "Salida de pie, tronco adelantado y tres primeros apoyos cortos.",
                 "Recuperación completa: la arrancada solo se entrena en fresco."])]),
 1: sesion("Velocidad lanzada + habilidad",
           "La sesión más rápida de la semana. Solo una novedad cada siete días: o subes metros o cierras ángulo, nunca las dos cosas juntas.",
           [sec("02", "Calentamiento de campo", "22 min", "tabla", CALIENTA_CAMPO),
            sec("07", "Campo · velocidad", "40 min", "lista",
                ["4-6 × 30 m al 90-95 %, entrando lanzado.",
                 "3-4 × 50-60 m de velocidad lanzada, sin salida explosiva.",
                 "Recuperación de 2-3 min entre series. Calidad, no cantidad.",
                 "Habilidad al final: conducción rápida, pared y primer toque, 10 min."]),
            sec("05", "Fisioterapia", "post-velocidad", "pasos", FISIO_VEL, FOTOS_FISIO)]),
 2: sesion("Aductor y core + agua",
           "El trabajo específico no se abandona aunque el campo empiece a mandar. Hoy toca sostenerlo.",
           [sec("02", "Rehab de aductor y core", "30 min", "tabla",
                MOV_LARGA + [("copenhagen-largo", "Copenhagen largo", "3 × 8 / lado", "")]),
            sec("04", "Piscina", "25 min", "lista", PISCINA_25, FOTOS_PISCINA),
            sec("05", "Fisioterapia", "descarga", "pasos", FISIO_DES, FOTOS_FISIO)]),
 3: sesion("COD cerrado + golpeo alto",
           "Ángulos cerrados y, al final, el primer golpeo con empeine alto desde que empezaste.",
           [sec("02", "Calentamiento de campo", "22 min", "tabla", CALIENTA_CAMPO),
            sec("07", "Campo · agilidad y golpeo", "45 min", "lista",
                ["Cambios de dirección de 90° y 135°, seis por lado.",
                 "180° controlado solo si los anteriores salieron limpios.",
                 "Pliometría reactiva baja, 3 × 8 saltos laterales.",
                 "Golpeo con empeine al 70-80 %, 12-15 golpeos, balón en movimiento.",
                 "Todavía NO hay balón parado: eso es la semana que viene."]),
            sec("06", "Pistola y EMS", "20 min · noche", "lista", PISTOLA, FOTOS_PISTOLA)]),
 4: sesion("Upper extra + balón parado",
           "Hoy vuelven las faltas y los córners. En series cortas y contadas, y con el número de mañana decidiendo si repites.",
           [sec("02", "Calentamiento de campo", "22 min", "tabla", CALIENTA_CAMPO),
            sec("07", "Campo · balón parado", "30 min", "lista",
                ["Solo a partir del día 8 del bloque, no antes.",
                 "6-8 faltas al 70-80 %, con carrera de dos o tres pasos.",
                 "6-8 córners con interior y empeine, sin buscar el máximo.",
                 "Entre serie y serie, un minuto andando y un chequeo de la ingle.",
                 "Máximo 16 golpeos parados en la sesión. Se para si el dolor pasa de 2."]),
            sec("03", "Gimnasio · Plan D upper extra", "40 min", "tabla", PLAN_D)]),
 5: sesion("Fútbol específico",
           "Rondos, posesión y finalización. Todo lo del partido menos la exigencia del partido.",
           [sec("02", "Calentamiento de campo", "20 min", "tabla", CALIENTA_CAMPO),
            sec("07", "Campo · fútbol", "50 min", "lista",
                ["Rondos y posesión en espacio reducido, 15 min.",
                 "Conducción rápida, regate y reacción, 10 min.",
                 "Finalización al 80-90 %, 15 disparos, balón en movimiento.",
                 "Sin contacto real y sin duelos todavía."])]),
 6: sesion("Descanso y test semanal",
           "Día libre, test semanal y, si toca puerta, el checklist entero antes de competir.",
           [sec("02", "Movilidad suave", "15 min", "tabla", MOV_CORTA),
            sec("09", "Test semanal", "rellenar", "test", [])]),
}

# ══ R5 · competitiva ════════════════════════════════════════════════
MICRO["R5"] = {
 0: sesion("Mantenimiento de fuerza",
           "Volumen bajo para conservar lo ganado. Lo que importa esta semana es llegar entero al sábado.",
           [sec("02", "Movilidad y activación", "18 min", "tabla", MOV_BASE),
            sec("03", "Gimnasio · pierna de mantenimiento", "35 min · RIR 3", "tabla", PLAN_C_POT[:4]),
            sec("03b", "Gimnasio · empuje y tirón", "30 min", "tabla", PLAN_A[:4] + PLAN_B[:4])]),
 1: sesion("Velocidad de calidad + habilidad",
           "Poca cantidad y mucha calidad: series cortas al 95 % con recuperación entera entre una y otra.",
           [sec("02", "Calentamiento de campo", "22 min", "tabla", CALIENTA_CAMPO),
            sec("07", "Campo · velocidad", "35 min", "lista",
                ["4 arrancadas de 10 m al 95 %.",
                 "4-6 × 40-60 m al 95 %, recuperación completa.",
                 "Habilidad con balón 10 min: conducción, pared y regate."])]),
 2: sesion("Aductor y core",
           "Mantenimiento específico. El Copenhagen no se retira cuando vuelvas a jugar: una o dos veces por semana, indefinidamente.",
           [sec("02", "Rehab de aductor y core", "25 min", "tabla",
                MOV_BASE + [("copenhagen-largo", "Copenhagen largo", "3 × 8 / lado", "")]),
            sec("04", "Piscina", "20 min", "lista", PISCINA_25[:3], FOTOS_PISCINA),
            sec("05", "Fisioterapia", "descarga", "pasos", FISIO_DES, FOTOS_FISIO)]),
 3: sesion("Golpeo y balón parado",
           "Faltas y córners a la intensidad que quieras, con las series contadas. Es tu gesto y también el que más castiga el pubis.",
           [sec("02", "Calentamiento de campo", "22 min", "tabla", CALIENTA_CAMPO),
            sec("07", "Campo · balón parado", "35 min", "lista",
                ["10-12 faltas a intensidad libre, con carrera completa.",
                 "8-10 córners a las dos alturas.",
                 "Finalización al 100 %, 10 disparos.",
                 "Techo de la sesión: 12 faltas. Más no da rendimiento y sí riesgo."]),
            sec("05", "Fisioterapia", "post-golpeo", "pasos", FISIO_VEL, FOTOS_FISIO)]),
 4: sesion("Activación previa al partido",
           "Víspera de partido. Activar sin cansar y llegar mañana con las piernas enteras.",
           [sec("02", "Movilidad y activación", "18 min", "tabla", MOV_CORTA),
            sec("03", "Gimnasio · activación", "25 min · RIR 4", "tabla", PLAN_D[:4]),
            sec("07", "Campo", "20 min", "lista",
                ["Técnica suave y cuatro progresivos de 40 m.",
                 "Seis golpeos cómodos. Nada de faltas hoy."])]),
 5: sesion("Partido con minutos controlados",
           "Vas subiendo minutos por escalones: 20-30, luego 45, luego 60-75 y al final el partido entero. Cada escalón se gana con un día siguiente limpio.",
           [sec("02", "Calentamiento de partido", "22 min", "tabla", CALIENTA_CAMPO),
            sec("07", "Partido", "minutos según escalón", "lista",
                ["Primer escalón: 20-30 min.",
                 "Segundo escalón: 45 min.",
                 "Tercer escalón: 60-75 min.",
                 "Partido completo solo con el checklist cerrado y sin reacción en el escalón anterior.",
                 "Las faltas del partido cuentan dentro del techo semanal de golpeos."])]),
 6: sesion("Descanso y test semanal",
           "Día libre y test. Los números de mañana, después del partido, son los que dicen si esto ha funcionado.",
           [sec("02", "Movilidad suave", "15 min", "tabla", MOV_CORTA),
            sec("09", "Test semanal", "rellenar", "test", [])]),
}

# ── nutrición: día de la semana -> comidas ──────────────────────────
NUTRICION = {
 0: ["Avena con leche, plátano, miel y nueces. Café.", "Yogur natural con fruta y almendras.",
     "Pollo, arroz integral y verduras salteadas.", "Leche, plátano y whey 25 g.",
     "Tostada integral con crema de cacahuete y plátano.", "Salmón al horno con patata y brócoli."],
 1: ["Tortilla de 3 claras y 1 huevo con espinacas, tostada y tomate.", "Fruta y queso fresco batido.",
     "Ternera magra con quinoa y ensalada.", "Batido de proteína con leche y plátano.",
     "Yogur natural con miel y avena.", "Merluza al vapor con arroz basmati y calabacín."],
 2: ["Yogur griego con avena, frutos rojos y miel.", "Tortita de arroz con aguacate y pavo.",
     "Lentejas estofadas con verduras y huevo cocido.", "Batido de plátano, avena y canela.",
     "Fruta y un puñado de nueces.", "Pollo con boniato asado y ensalada verde."],
 3: ["Avena nocturna con leche, chía, plátano y cacao.", "Fruta y un puñado de nueces.",
     "Salmón a la plancha con cuscús integral y espárragos.", "Yogur natural con miel y avena.",
     "Tostada integral con queso fresco.", "Tortilla francesa con champiñones y ensalada."],
 4: ["Tostadas integrales con aguacate y huevo pochado.", "Batido de proteína y una fruta.",
     "Pollo al curry con arroz integral y verduras.", "Leche, plátano y whey 25 g.",
     "Requesón con fruta y canela.", "Atún a la plancha con patata cocida y ensalada."],
 5: ["Porridge de avena con plátano, canela y nueces.", "Yogur natural con granola sin azúcar.",
     "Pasta integral con tomate natural y pavo.", "Batido de proteína.",
     "Tostada integral con queso fresco y tomate.", "Revuelto de huevos con espinacas y champiñones."],
 6: ["Huevos revueltos con tomate natural y pan integral.", "Fruta y almendras.",
     "Paella casera de pollo y verduras.", "Batido de proteína con leche y plátano.",
     "Yogur con fruta.", "Crema de calabaza con pavo y ensalada."],
}
MOMENTOS = ["Desayuno", "Media mañana", "Comida", "Post-entreno", "Merienda", "Cena"]

# Progresion del isometrico de aductor.
# R1 es el bloque que RECUPERA la tolerancia: sube de 50 a 80 en sus 14 dias.
# De R2 en adelante el trabajo pesado pasa al Copenhagen y a la fuerza, asi que
# el isometrico se queda en 80 como activacion y mantenimiento. Reiniciarlo a 50
# en cada bloque seria un retroceso.
ISO = [50, 50, 50, 60, 60, 60, 60, 70, 70, 70, 70, 80, 80, 80]
ISO_MANT = [80] * 21

for _b in BLOQUES:
    _b["iso"] = ISO if _b["id"] == "R1" else ISO_MANT



# ── reparto semanal: mitades que rotan, sin dias de tres horas ───────
# core y pubis NUNCA caen el mismo dia. Los estiramientos completos van en los
# dos dias ligeros (jueves y domingo) y el resto de dias llevan la version corta.
def _mitades(lista):
    """Parte una rutina en dos mitades alternas, sin perder el ejercicio clave."""
    clave = [x for x in lista if x[3]]
    resto = [x for x in lista if not x[3]]
    a = clave + resto[0::2]
    b = clave + resto[1::2]
    return a, b


CORE_POR = {"R1": CORE_BASE, "R2": CORE_MEDIO, "R3": CORE_MEDIO,
            "R4": CORE_FUERTE, "R5": CORE_FUERTE}
PUBIS_POR = {"R1": PUBIS_R1, "R2": PUBIS_R2, "R3": PUBIS_R3,
             "R4": PUBIS_MANT, "R5": PUBIS_MANT}
ESTIRA_POR = {"R1": ESTIRA_BASE, "R2": ESTIRA_COMPLETO, "R3": ESTIRA_COMPLETO,
              "R4": ESTIRA_COMPLETO, "R5": ESTIRA_COMPLETO}
FUTBOL_POR = {"R3": {1: FUTBOL_R3A, 4: FUTBOL_R3B, 5: FUTBOL_R3A},
              "R4": {1: FUTBOL_R4A, 4: FUTBOL_R4B, 5: FUTBOL_R4A},
              "R5": {1: FUTBOL_R5, 3: FUTBOL_R5}}

ESTIRA_CORTO = {k: [x for x in v if x[3]] + [x for x in v if not x[3]][:3]
                for k, v in ESTIRA_POR.items()}

# dia de la semana -> que rutina extra lleva
#   0 lunes, 1 martes, 2 miercoles, 3 jueves, 4 viernes, 5 sabado, 6 domingo
PLAN_EXTRA = {
    0: ("core", "a"),      # tras el gimnasio pesado
    1: ("pubis", "a"),
    2: ("pubis", "b"),     # el dia de rehab larga, pubis completo
    3: ("core", "b"),      # dia ligero
    4: ("pubis", "a"),
    5: ("core", "a"),
    6: (None, None),       # descanso: solo estiramientos largos
}
DIAS_ESTIRA_LARGO = (3, 6)

for _bid, _dias in MICRO.items():
    _ca, _cb = _mitades(CORE_POR[_bid])
    _pa, _pb = _mitades(PUBIS_POR[_bid])
    for _d, _ses in _dias.items():
        _que, _mitad = PLAN_EXTRA[_d]
        if _que == "core":
            _ses["secciones"].append(
                sec("10", "Core y abdominales", "10 min · puede ir por la noche",
                    "tabla", _ca if _mitad == "a" else _cb))
        elif _que == "pubis":
            _lista = _pa if _mitad == "a" else PUBIS_POR[_bid]
            _ses["secciones"].append(
                sec("12", "Aductor y pubis", "12 min · el trabajo que cura",
                    "tabla", _lista))
        if _bid in FUTBOL_POR and _d in FUTBOL_POR[_bid]:
            _ses["secciones"].append(
                sec("07b", "Fútbol · técnica", "según el escalón del bloque",
                    "tabla", FUTBOL_POR[_bid][_d]))
        _largo = _d in DIAS_ESTIRA_LARGO
        _ses["secciones"].append(
            sec("11", "Estiramientos",
                ("15 min · sesión larga" if _largo else "8 min · al terminar o por la noche"),
                "tabla", ESTIRA_POR[_bid] if _largo else ESTIRA_CORTO[_bid]))

APERTURA["secciones"].append(
    sec("11", "Estiramientos", "12 min · al terminar", "tabla", ESTIRA_BASE))
