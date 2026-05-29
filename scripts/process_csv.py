#!/usr/bin/env python3
"""
Procesa registros-luma.csv → genera registros-master.csv.

Hace en una sola pasada (FASES 1 + 2 + 3 del CLAUDE.md):
- Limpieza: nombre Title Case, empresa Title Case, pregunta marcada [VACIO] si genérica.
- Segmentación por nivel de intención (HOT / WARM / COLD / NEUTRAL) por keyword matching.
- Generación de respuesta personalizada usando plantillas por categoría + datos del lead.

Output columns:
nombre, correo, telefono, empresa, rol, pregunta_formulario, utm_source, asistio,
nivel_intencion, respuesta_personalizada
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "registros-luma.csv"
OUT = ROOT / "registros-master.csv"

PRICE_PROMO = 1750
CUPOS_INICIAL = 15
CUPOS_RESTANTES = 3
CHECKOUT_URL = "https://checkout.oracle30x.co/checkout/aisales-discount"
CALENDLY_URL = "https://calendly.com/d/cxpx-kmb-ccy/30x-sales-ai-sales-admisiones"

QUESTION_COL = 'Qué preguntas tienes acerca del programa de 30X "AI Sales" (Ventas con IA)?'
EMPRESA_COL = "En qué empresa trabajas?"
ROL_COL = "Cuál es tu rol?"

# Keywords para detectar nivel de intención
HOT_KW = [
    "precio", "costo", "cuanto cuesta", "cuánto cuesta", "cuanto sale", "cuánto sale",
    "valor", "inversion", "inversión", "dolar", "dólar", "usd", "descuento",
    "financ", "pago", "cuotas", "promo", "beca", "reserva", "cupo",
    "fecha", "cuando empieza", "cuándo empieza", "inicio", "arranca", "próxima cohorte", "proxima cohorte",
    "certific", "factura", "empresa", "tarifa corporativ", "guardame", "guárdame", "guardar cupo",
    "quiero inscribir", "como aplico", "cómo aplico", "como me inscribo", "reservar cupo",
    "comprar", "inscribirme", "anotarme", "registr",
]
WARM_KW = [
    "n8n", "dapta", "gpt", "agente", "chatbot", "voz", "hubspot", "salesforce",
    "pipedrive", "outbound", "inbound", "conversational", "discovery", "follow up",
    "followup", "forecast", "revops", "pipeline", "agentes autón", "autonom",
    "sales coaching", "conversational intelligence", "social selling", "linkedin",
    "marca personal", "community", "comunidad", "template", "workflow",
    "soy sdr", "soy ae", "soy founder", "soy ceo", "soy director", "soy gerente",
    "mi empresa", "mi negocio", "mi industria", "mi sector", "mi rol",
    "fit", "me sirve", "para mí", "para mi", "comparado con", "diferencia con",
]
COLD_KW = [
    "de qué se trata", "de que se trata", "que es", "qué es",
    "que voy a aprender", "qué voy a aprender",
    "no sé nada", "no se nada", "no soy técnico", "no soy tecnico",
    "principiante", "empezar de cero", "primera vez",
    "cuánto tiempo", "cuanto tiempo", "horas por semana", "tiempo le tengo",
    "grabad", "me lo pierdo", "si me pierdo",
]

# Categorización por keywords (para generar respuesta)
CATEGORIES = [
    ("PRICING", ["precio", "costo", "cuanto cuesta", "cuánto cuesta", "cuanto sale",
                 "cuánto sale", "valor", "inversion", "inversión", "dolar", "dólar",
                 "usd", "descuento", "financ", "pago", "cuotas", "promo", "beca", "reserva"]),
    ("SCHEDULE", ["fecha", "cuando", "cuándo", "empieza", "inicio", "arranca", "cohorte",
                  "próxima", "proxima", "horario", "duración", "duracion"]),
    ("FORMAT", ["virtual", "presencial", "grabad", "grabac", "en vivo", "modalidad",
                "online", "asincr", "sincronic", "sesiones", "clases"]),
    ("FIT", ["sirve", "sirvo", "soy ", "para mí", "para mi", "me sirve", "aplica",
             "principiante", "no técnico", "no tecnico"]),
    ("TOOLS", ["n8n", "dapta", "gpt", "agente", "chatbot", "voz", "hubspot", "salesforce",
               "pipedrive", "crm", "herramient", "tools", "stack", "plataforma", "software"]),
    ("OUTBOUND", ["outbound", "prospect", "prospecció", "prospeccio", "lead gen", "cold",
                  "outreach", "generar leads", "captac", "enrich", "dossier"]),
    ("INBOUND", ["inbound", "convers", "chat", "speed", "responder",
                 "follow up", "followup", "discovery", "llamada", "reuni"]),
    ("REVOPS", ["forecast", "revops", "pipeline", "agentes autón", "autonom",
                "reporte", "métrica", "metrica", "scoring", "calificac"]),
    ("CONTENT", ["linkedin", "contenido", "autoridad", "marca personal", "social selling",
                 "redes", "post"]),
    ("CASES", ["caso", "ejemplo", "industria", "sector", "b2b", "b2c", "enterprise",
               "pyme", "startup", "mi industria"]),
    ("OUTCOME", ["resultados", "roi", "impacto", "beneficio", "aprend", "qué voy a",
                 "que voy a", "obtener", "llevarme", "lograr"]),
    ("LEVEL", ["nivel", "requisito", "prerequisito", "conocimiento previo", "sé de",
               "se de", "no sé", "no se nada"]),
]

GENERIC_EMPTY = {"ninguna", "ninguno", "no", "no se", "no sé", "nada", "x", "-",
                 "na", "none", "ok", "ok.", "si", "sí", "todo", "?", "??", "...",
                 "n/a", "ninguna por ahora", "ninguna pregunta", "."}


def title_case(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return ""
    # Si todo mayúsculas o todo minúsculas, normalizar
    if s.isupper() or s.islower():
        return " ".join(w.capitalize() for w in s.split())
    return s


def clean_company(s: str) -> str:
    s = (s or "").strip().strip('"').strip()
    if not s:
        return ""
    # Quitar puntos finales sueltos
    s = s.rstrip(".")
    return title_case(s)


def clean_question(q: str) -> str:
    q = (q or "").strip()
    if not q:
        return "[VACIO]"
    if len(q) < 4:
        return "[VACIO]"
    if q.lower().strip() in GENERIC_EMPTY:
        return "[VACIO]"
    # Si es solo signos
    if re.fullmatch(r"[\s\.\?\!\-\,]+", q):
        return "[VACIO]"
    return q


def detect_intent(question: str) -> str:
    if question == "[VACIO]":
        return "NEUTRAL"
    ql = question.lower()
    if any(k in ql for k in HOT_KW):
        return "HOT"
    if any(k in ql for k in WARM_KW):
        return "WARM"
    if any(k in ql for k in COLD_KW):
        return "COLD"
    return "COLD"  # Tiene pregunta no clasificada → COLD por defecto


def detect_category(question: str) -> str:
    if question == "[VACIO]":
        return "EMPTY"
    ql = question.lower()
    for cat, kws in CATEGORIES:
        if any(k in ql for k in kws):
            return cat
    return "OTHER"


def first_name(full_name: str) -> str:
    parts = (full_name or "").strip().split()
    return parts[0] if parts else "—"


def generate_response(nombre, empresa, rol, pregunta, categoria, nivel) -> str:
    """Genera respuesta personalizada con plantillas por categoría + datos del lead."""
    fn = first_name(nombre)
    rol_low = (rol or "").lower()

    # Bloque CTA según nivel — FOMO real: del lote de 15, quedan solo 3
    promo_line = f"De los {CUPOS_INICIAL} cupos a USD 1.750 (USD 200 off), solo quedan {CUPOS_RESTANTES}."
    if nivel == "HOT":
        cta = f"{promo_line} Reservá ahora: {CHECKOUT_URL}"
    elif nivel == "WARM":
        cta = f"{promo_line} Si necesitás validar fit antes, agendá 15 min: {CALENDLY_URL}. Si ya tenés decidido, asegurá uno de los {CUPOS_RESTANTES} cupos: {CHECKOUT_URL}"
    else:
        cta = f"Para arrancar: 15 min con admisiones {CALENDLY_URL}. {promo_line} Reservar: {CHECKOUT_URL}"

    if pregunta == "[VACIO]":
        return (
            f"Hola {fn}, vi que te registraste al webinar 30X AI Sales. "
            f"Para armarte una propuesta concreta necesito saber: ¿qué te gustaría resolver con IA en tu proceso comercial? "
            f"Cuanto más específico (prospección, follow-up, forecasting, atención de inbound, etc.), mejor te oriento si AI Sales "
            f"(4 semanas, sobre tu pipeline real, USD 1.750 con la promo activa — quedan solo {CUPOS_RESTANTES} cupos de {CUPOS_INICIAL}) te calza. {cta}"
        )

    bodies = {
        "PRICING": (
            f"Hola {fn}, sobre el precio: regular USD 1.950, pero por asistir al webinar abrimos {CUPOS_INICIAL} cupos a USD 1.750 "
            f"(USD 200 off). De esos, **solo quedan {CUPOS_RESTANTES} disponibles**. Aceptamos tarjeta o transferencia. "
            f"En 4 semanas trabajás sobre tu pipeline real con Nicolás Rojas (CEO Dapta) y Andrés Bilbao (co-founder Rappi); "
            f"vienen +100K créditos Dapta gratis y certificado oficial 30X. {cta}"
        ),
        "SCHEDULE": (
            f"Hola {fn}, la próxima cohorte arranca pronto — son 4 semanas, 8 sesiones en vivo, 100% online (todas grabadas con 1 año de acceso). "
            f"Cupos totales: 100 por cohorte. Para confirmar fecha exacta y reservar lugar, 15 min con admisiones: {CALENDLY_URL}. "
            f"Promo activa: USD 1.750 — abrimos {CUPOS_INICIAL} cupos a este precio y **quedan solo {CUPOS_RESTANTES}**: {CHECKOUT_URL}"
        ),
        "FORMAT": (
            f"Hola {fn}, es 100% online. 8 sesiones en vivo donde aplicás sobre TU pipeline real (no demos genéricas), todas grabadas con 1 año de acceso. "
            f"Si te perdés alguna, la ves después sin perder progreso. Más comunidad activa de SDRs, AEs y líderes comerciales. {cta}"
        ),
        "FIT": (
            f"Hola {fn}, AI Sales está pensado exactamente para perfiles como el tuyo ({rol or 'líder comercial'}): heads of sales, directores, founders que venden, AEs, SDR/BDR leads. "
            f"No necesitás background técnico — el stack (Dapta, n8n, GPTs) no requiere developers. "
            f"Trabajás sobre TU pipeline real desde semana 1, no sobre casos hipotéticos. {cta}"
        ),
        "TOOLS": (
            f"Hola {fn}, sobre el stack: trabajás directo con Dapta (infraestructura IA), n8n (orquestación), GPTs custom, agentes de voz y conectores a tu CRM (HubSpot, Salesforce, Pipedrive). "
            f"Vienen +100K créditos Dapta gratis y los templates de n8n listos para copiar/pegar. "
            f"No armás el stack desde cero — lo aplicás sobre tu pipeline desde la primera semana. {cta}"
        ),
        "OUTBOUND": (
            f"Hola {fn}, tu pregunta cae directo en Módulo 3 (Inteligencia de Cuentas: dossiers automáticos antes del primer contacto) y Módulo 4 (Hiper-Personalización a Escala: secuencias multicanal que se sienten 1-a-1). "
            f"Aplicás todo sobre TU lista real de cuentas desde la semana 1. {cta}"
        ),
        "INBOUND": (
            f"Hola {fn}, eso lo cubrimos en Módulo 5 (Conversational AI & Speed-to-Lead: agentes de voz y chat que califican y enrutan en segundos) y Módulo 6 (Discovery & Follow-Up: IA que escucha la llamada y arma el siguiente paso automáticamente). "
            f"Cero leads esperando, cero follow-ups olvidados. {cta}"
        ),
        "REVOPS": (
            f"Hola {fn}, Módulo 8 (RevOps, Forecasting & Agentes Autónomos): forecasting predictivo con criterio de negocio (no Excel ni corazonadas), CRM autónomo, y agentes SDR basados en IA. "
            f"Pensado para directores comerciales y revenue leaders que necesitan operación que escale sin sumar headcount. {cta}"
        ),
        "CONTENT": (
            f"Hola {fn}, Módulo 2 (Social Selling & Autoridad de Marca): sistema de contenido LinkedIn asistido por IA que convierte tu expertise en oportunidades. "
            f"No son tips de copywriting — es un workflow que produce contenido relevante a escala desde lo que vos ya sabés. {cta}"
        ),
        "CASES": (
            f"Hola {fn}, los frameworks de IA aplicados a ventas son agnósticos de industria — funciona igual en B2B SaaS, fintech, consumo masivo, servicios, agro, salud. "
            f"Lo que cambia es el ejemplo concreto que armamos sobre tu pipeline (de {empresa or 'tu empresa'}), no la metodología. {cta}"
        ),
        "OUTCOME": (
            f"Hola {fn}, la métrica que sale del programa es 20x productividad en 4 semanas. En operativa real: research por cuenta de 2h a 10 min, respuesta a inbound duplicada, follow-ups 5x. "
            f"Salís con sistema de outbound asistido funcionando, agentes inbound corriendo y forecasting predictivo armado — sobre tu pipeline de {empresa or 'tu empresa'}. {cta}"
        ),
        "LEVEL": (
            f"Hola {fn}, cero conocimiento previo de IA o programación necesario. El programa está diseñado específicamente para líderes comerciales no técnicos. "
            f"Si entendés tu proceso de ventas, podés aplicar IA encima. Las sesiones son de aplicación, no de teoría. {cta}"
        ),
    }

    if categoria in bodies:
        return bodies[categoria]

    # Categoría OTHER → respuesta genérica que cita el rol/empresa
    return (
        f"Hola {fn}, gracias por tu pregunta. AI Sales son 4 semanas trabajando sobre tu pipeline real con Nicolás Rojas (Dapta) y Andrés Bilbao (Rappi), "
        f"100% online, +100K créditos Dapta gratis. Para alguien con tu perfil ({rol or 'líder comercial'} en {empresa or 'tu empresa'}), "
        f"lo más concreto es que en 4 semanas armás outbound asistido, inbound conversacional y forecasting predictivo aplicado a tu operación. {cta}"
    )


def main():
    rows_in = []
    with open(SRC, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows_in.append(r)

    print(f"Leídos: {len(rows_in)} registros")

    out_rows = []
    counts = {"HOT": 0, "WARM": 0, "COLD": 0, "NEUTRAL": 0}
    asist = {"Si": 0, "No": 0}

    for r in rows_in:
        nombre = title_case(r.get("name", ""))
        correo = (r.get("email") or "").strip().lower()
        telefono = (r.get("phone_number") or "").strip()
        empresa = clean_company(r.get(EMPRESA_COL, ""))
        rol = title_case(r.get(ROL_COL, ""))
        pregunta_raw = r.get(QUESTION_COL, "") or ""
        pregunta = clean_question(pregunta_raw)
        utm = (r.get("utm_source") or "direct").strip() or "direct"
        asistio = r.get("has_joined_event", "No") or "No"
        asistio = "Si" if asistio.strip().lower() in ("yes", "si", "sí", "true", "1") else "No"

        nivel = detect_intent(pregunta)
        categoria = detect_category(pregunta)
        respuesta = generate_response(nombre, empresa, rol, pregunta, categoria, nivel)

        counts[nivel] += 1
        asist[asistio] += 1

        out_rows.append({
            "nombre": nombre,
            "correo": correo,
            "telefono": telefono,
            "empresa": empresa,
            "rol": rol,
            "pregunta_formulario": pregunta,
            "utm_source": utm,
            "asistio": asistio,
            "nivel_intencion": nivel,
            "respuesta_personalizada": respuesta,
        })

    fieldnames = ["nombre", "correo", "telefono", "empresa", "rol",
                  "pregunta_formulario", "utm_source", "asistio",
                  "nivel_intencion", "respuesta_personalizada"]
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    print(f"Escritos: {len(out_rows)} → {OUT.name}")
    print(f"  Niveles: {counts}")
    print(f"  Asistencia: {asist}")


if __name__ == "__main__":
    main()
