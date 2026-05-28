#!/usr/bin/env python3
"""
Genera index.html a partir de registros-master.csv.

Construye el dashboard completo del webinar 30X AI Sales con:
- Topbar live
- Hero estilo statement
- Stats bar (Total / HOT / WARM / COLD / Decision makers / Empresas grandes)
- Sección FAQ agrupada por intent y ordenada por frecuencia
- Grid de leads con filtros y modal
- Live generator (botón GENERAR PROPUESTA contra proxy de Vercel)
- Meta-footer
"""

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "registros-master.csv"
OUT_PATH = ROOT / "index.html"

PROXY_URL = "https://webinar-ai-sales.vercel.app/api/claude"
CALENDLY_URL = "https://calendly.com/d/cxpx-kmb-ccy/30x-sales-ai-sales-admisiones"
CURSO_URL = "https://30x.com/programas/ai-sales"
CHECKOUT_URL = "https://checkout.oracle30x.co/checkout/aisales-discount"
PRICE_FULL = 1950
PRICE_PROMO = 1750
CUPOS_PROMO = 15

# Keywords para categorizar preguntas
CATS = [
    ("TOOLS", "Stack y herramientas (Dapta, n8n, GPTs)",
     ["n8n", "dapta", "gpt", "agente", "chatbot", "voz", "hubspot", "salesforce",
      "pipedrive", "crm", "herramient", "tools", "stack", "plataforma", "software"]),
    ("PRICING", "Precio, pago y reserva de cupo",
     ["precio", "costo", "cuanto cuesta", "cuánto cuesta", "cuanto sale", "cuánto sale",
      "valor", "inversion", "inversión", "dolar", "dólar", "usd", "descuento", "financ",
      "pago", "cuotas", "promo", "beca", "reserva"]),
    ("FIT", "¿Me sirve a mí? Fit por rol o tipo de empresa",
     ["sirve", "sirvo", "soy ", "para mí", "para mi", "me sirve", "aplica",
      "principiante", "no técnico", "no tecnico"]),
    ("OUTCOME", "Resultado: qué me llevo del programa",
     ["resultados", "roi", "impacto", "beneficio", "aprend", "qué voy a",
      "que voy a", "obtener", "llevarme", "lograr"]),
    ("SCHEDULE", "Fechas, cohorte y duración",
     ["fecha", "cuando", "cuándo", "empieza", "inicio", "arranca", "cohorte",
      "próxima", "proxima", "horario", "duración", "duracion"]),
    ("OUTBOUND", "Outbound, prospección y enrichment",
     ["outbound", "prospect", "prospecció", "prospeccio", "lead gen", "cold",
      "outreach", "generar leads", "captac", "enrich", "dossier"]),
    ("CASES", "Casos por industria o tipo de empresa",
     ["caso", "ejemplo", "industria", "sector", "b2b", "b2c", "enterprise",
      "pyme", "startup", "mi industria"]),
    ("FORMAT", "Modalidad: en vivo, grabado, online",
     ["virtual", "presencial", "grabad", "grabac", "en vivo", "modalidad",
      "online", "asincr", "sincronic", "sesiones", "clases"]),
    ("INBOUND", "Inbound: conversational AI, discovery, follow-up",
     ["inbound", "convers", "chat", "speed-to-lead", "responder",
      "follow up", "followup", "discovery", "llamada", "reuni"]),
    ("CONTENT", "Social Selling y autoridad de marca",
     ["linkedin", "contenido", "autoridad", "marca personal", "social selling",
      "redes", "post"]),
    ("LEVEL", "Conocimiento previo necesario",
     ["nivel", "requisito", "prerequisito", "conocimiento previo", "sé de",
      "se de", "no sé", "no se nada"]),
    ("REVOPS", "Forecasting, RevOps y agentes autónomos",
     ["forecast", "revops", "pipeline", "agentes autón", "autonom",
      "reporte", "métrica", "metrica", "scoring", "calificac"]),
]

# Respuestas oficiales por categoría (basadas en CLAUDE.md)
ANSWERS = {
    "TOOLS": "Trabajás directo sobre el stack: **Dapta** (infraestructura de IA), **n8n** (orquestación), **GPTs custom**, agentes de voz, e integraciones con tu CRM (HubSpot, Salesforce, Pipedrive). Vienen **+100K créditos de Dapta gratis** y todos los templates de n8n listos para copiar/pegar. No tenés que armar el stack desde cero — lo aplicás sobre tu pipeline desde la primera semana.",
    "PRICING": "Precio regular: **USD 1.950**. **Promo activa para asistentes al webinar: USD 1.750** (USD 200 off, cupos limitados a 15 personas). Aceptamos tarjeta de crédito y transferencia bancaria; si necesitás otra opción, lo coordinamos con admisiones. Por la cantidad de templates, los +100K créditos de Dapta y la mentoría en vivo con Nicolás Rojas y Andrés Bilbao, el ROI se mide en deals cerrados las primeras semanas, no en costo recuperado. **Reservar con descuento → checkout.oracle30x.co/checkout/aisales-discount**",
    "FIT": "Está pensado para **líderes comerciales no técnicos**: heads of sales, directores comerciales, founders que venden, account executives, SDR/BDR leads y revenue leaders. No necesitás saber programar — el stack que aprendés (Dapta, n8n, GPTs) no requiere developers. Si liderás un equipo de ventas, prospectás o cerrás, te calza. Trabajamos sobre TU pipeline real, no sobre casos hipotéticos.",
    "OUTCOME": "La métrica concreta del programa es **20x productividad en 4 semanas**. En operativa real: equipos que reducen el research por cuenta de 2h a 10 min, founders que duplican respuesta a leads inbound, AEs que mandan 5x los follow-ups que mandaban antes. El impacto exacto depende de qué vendés y tu ciclo de venta, pero todos salen con: sistema de outbound asistido funcionando, agentes de inbound corriendo y forecasting predictivo armado.",
    "SCHEDULE": "La próxima cohorte arranca pronto — cupos limitados a **100 personas** por cohorte, programa de **4 semanas**, **8 sesiones en vivo** (más material grabado por 1 año). Para fecha confirmada y reservar lugar, agendá 15 min con admisiones: [link Calendly]",
    "OUTBOUND": "Hay dos módulos dedicados: **Módulo 3 — Inteligencia de Cuentas & Data Enrichment** (dossiers automáticos antes del primer contacto, señales de compra detectadas por IA) y **Módulo 4 — Outbound: Hiper-Personalización a Escala** (secuencias multicanal que se sienten 1-a-1 sin que las escribas a mano). Aplicás todo sobre tu lista real de cuentas desde la semana 1.",
    "CASES": "Los frameworks de IA aplicados a ventas son **agnósticos de industria**. Funciona igual en B2B SaaS, fintech, consumo masivo, servicios profesionales, agro, salud — todos cierran, todos prospectan, todos pueden multiplicar productividad. Lo que cambia es el ejemplo concreto que armamos sobre tu pipeline; la metodología es la misma. En las sesiones en vivo trabajás directamente sobre TUS cuentas, no sobre demos de juguete.",
    "FORMAT": "**100% online**. 8 sesiones en vivo en las que aplicás sobre tu pipeline real (no demos). Todas las sesiones quedan grabadas con **1 año de acceso**. Si te perdés alguna, la ves después sin perder progreso. Más comunidad de SDRs, AEs y líderes comerciales activos en el stack, donde se comparten templates y casos en tiempo real.",
    "INBOUND": "Dos módulos: **Módulo 5 — Conversational AI & Speed-to-Lead** (agentes de voz y chat que califican, enrutan y convierten sin fricción, eliminando el lapso entre lead inbound y primera respuesta) y **Módulo 6 — Discovery & Follow-Up** (IA que escucha la llamada, analiza objeciones y arma el siguiente paso antes de que cuelgues). Cero leads esperando, cero follow-ups olvidados.",
    "CONTENT": "**Módulo 2 — Social Selling & Autoridad de Marca**. No son tips de copywriting: es un sistema de contenido (LinkedIn principalmente) que convierte expertise en oportunidades. Workflow asistido por IA que produce contenido relevante a escala desde lo que vos ya sabés, sin que parezca generado por máquina.",
    "LEVEL": "**Cero conocimiento previo de IA o programación necesario.** El programa está diseñado específicamente para líderes comerciales no técnicos. Si entendés tu proceso de ventas, podés aplicar IA encima — las sesiones en vivo son de aplicación, no de teoría. El stack (Dapta, n8n, GPTs) está pensado para usuarios sin background técnico.",
    "REVOPS": "**Módulo 8 — RevOps, Forecasting & Agentes Autónomos.** Forecasting predictivo con criterio de negocio (no Excel ni corazonadas), CRM autónomo que se actualiza solo, y agentes SDR basados en IA que sostienen el pipeline sin sumar headcount. Pensado para directores comerciales y revenue leaders que necesitan operación que escale.",
}

DECISION_KW = [
    "ceo", "founder", "fundador", "director", "head", "c-level", "cofounder",
    "co-founder", "vp", "vicepresidente", "presidente", "dueño", "dueno",
    "owner", "chief"
]

ENTERPRISE = [
    "bancolombia", "rappi", "mercadolibre", "meli", "mastercard", "nubank",
    "globant", "santander", "itau", "itaú", "platzi", "crehana", "despegar",
    "accenture", "google", "microsoft", "amazon", "meta", "siigo", "konfio",
    "tigo", "claro", "movistar", "telefonica", "telefónica", "bbva", "davivienda",
    "grupo aval", "cencosud", "falabella", "arcor", "ypf", "telmex"
]


def load_rows():
    with open(CSV_PATH, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def categorize_questions(rows):
    counts = Counter()
    samples = defaultdict(list)
    for r in rows:
        q = (r.get("pregunta_formulario") or "").strip()
        if q in ("[VACIO]", "") or len(q) < 5:
            continue
        if q.lower() in ("ninguna", "ninguno", "no", "no se", "no sé",
                         "nada", "x", "-", "na", "none", "ok", "ok.",
                         "si", "sí", "todo"):
            continue
        ql = q.lower()
        for cat, _label, kws in CATS:
            if any(k in ql for k in kws):
                counts[cat] += 1
                if len(samples[cat]) < 3:
                    samples[cat].append(q[:160])
                break
    return counts, samples


def build_stats(rows, q_counts):
    return {
        "total": len(rows),
        "hot": sum(1 for r in rows if r["nivel_intencion"] == "HOT"),
        "warm": sum(1 for r in rows if r["nivel_intencion"] == "WARM"),
        "cold": sum(1 for r in rows if r["nivel_intencion"] == "COLD"),
        "neutral": sum(1 for r in rows if r["nivel_intencion"] == "NEUTRAL"),
        "attended": sum(1 for r in rows if r["asistio"] == "Si"),
        "decision_makers": sum(
            1 for r in rows
            if any(k in (r.get("rol") or "").lower() for k in DECISION_KW)
        ),
        "enterprise": sum(
            1 for r in rows
            if any(b in (r.get("empresa") or "").lower() for b in ENTERPRISE)
        ),
        "real_questions": sum(q_counts.values()),
        "categories_count": len(q_counts),
    }


def build_leads(rows):
    out = []
    for r in rows:
        out.append({
            "n": r.get("nombre", "").strip(),
            "e": r.get("correo", "").strip(),
            "t": r.get("telefono", "").strip(),
            "c": (r.get("empresa") or "").strip(),
            "r": (r.get("rol") or "").strip(),
            "q": (r.get("pregunta_formulario") or "[VACIO]").strip(),
            "u": (r.get("utm_source") or "direct").strip() or "direct",
            "a": r.get("asistio", "No"),
            "i": r.get("nivel_intencion", "NEUTRAL"),
            "p": (r.get("respuesta_personalizada") or "").strip(),
        })
    return out


def build_faqs(q_counts, samples):
    faqs = []
    label_map = {c[0]: c[1] for c in CATS}
    for cat, count in q_counts.most_common():
        faqs.append({
            "cat": cat,
            "label": label_map[cat],
            "count": count,
            "samples": samples[cat],
            "answer": ANSWERS.get(cat, ""),
        })
    return faqs


HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>30X AI Sales · Dashboard de Leads · Live from Webinar</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700;800&family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0a0a0a;
  --bg-elevated: #131313;
  --bg-card: #1a1a1a;
  --border: #2a2a2a;
  --border-bright: #3a3a3a;
  --text: #e8e8e8;
  --text-dim: #888;
  --text-faint: #555;
  --accent: #c7f352;
  --accent-dim: #8aa624;
  --accent-glow: rgba(199, 243, 82, 0.15);
  --red: #ff4d4d;
  --red-dim: #a63a3a;
  --green: #3aff8a;
  --amber: #ff9933;
  --blue: #4d9fff;
  --purple: #c084fc;
  --mono: 'JetBrains Mono', 'Courier New', monospace;
  --display: 'Instrument Serif', Georgia, serif;
  --sans: 'Geist', system-ui, sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  background: var(--bg); color: var(--text);
  font-family: var(--sans); font-size: 14px; line-height: 1.5;
  overflow-x: hidden; -webkit-font-smoothing: antialiased;
}
body::before {
  content: ''; position: fixed; inset: 0;
  background-image:
    radial-gradient(at 20% 0%, rgba(199, 243, 82, 0.06) 0px, transparent 50%),
    radial-gradient(at 80% 100%, rgba(255, 77, 77, 0.04) 0px, transparent 50%);
  pointer-events: none; z-index: 0;
}
body::after {
  content: ''; position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
  background-size: 40px 40px; pointer-events: none; z-index: 0;
}
.topbar {
  position: sticky; top: 0; z-index: 100;
  background: rgba(10,10,10,0.85); backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  padding: 12px 24px; display: flex; align-items: center; justify-content: space-between;
  font-family: var(--mono); font-size: 11px; letter-spacing: 0.08em;
}
.topbar-left { display: flex; gap: 24px; align-items: center; flex-wrap: wrap; }
.brand {
  font-family: var(--mono); font-weight: 800; color: var(--accent);
  letter-spacing: 0.15em; display: flex; align-items: center; gap: 8px;
}
.brand::before { content: '◢'; color: var(--red); font-size: 14px; }
.topbar-status { color: var(--text-dim); display: flex; align-items: center; gap: 8px; }
.dot-live {
  display: inline-block; width: 6px; height: 6px;
  border-radius: 50%; background: var(--green);
  animation: pulse 2s infinite; box-shadow: 0 0 8px var(--green);
}
@keyframes pulse { 50% { opacity: 0.4; } }
.topbar-right { display: flex; gap: 16px; color: var(--text-dim); flex-wrap: wrap; }
.topbar-right span { padding: 4px 10px; border: 1px solid var(--border); border-radius: 3px; }
.topbar-right span.highlight { color: var(--accent); border-color: var(--accent-dim); }
.promo-pill {
  background: var(--accent); color: var(--bg);
  padding: 4px 10px; border-radius: 3px;
  text-decoration: none; font-weight: 700;
  font-family: var(--mono); letter-spacing: 0.08em;
  border: 1px solid var(--accent);
  transition: transform 0.15s, box-shadow 0.15s;
}
.promo-pill:hover { transform: translateY(-1px); box-shadow: 0 0 14px var(--accent-glow); background: var(--text); }

.hero {
  position: relative; z-index: 1;
  padding: 80px 48px 60px;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(180deg, transparent, rgba(199,243,82,0.02));
}
.hero-grid {
  display: grid; grid-template-columns: 1.4fr 1fr; gap: 60px;
  max-width: 1600px; margin: 0 auto;
}
.hero-eyebrow {
  font-family: var(--mono); font-size: 11px; color: var(--accent);
  letter-spacing: 0.25em; margin-bottom: 24px;
  display: flex; align-items: center; gap: 12px;
}
.hero-eyebrow::after { content: ''; height: 1px; flex: 1; background: var(--accent); opacity: 0.3; }
.hero h1 {
  font-family: var(--display); font-size: clamp(48px, 6vw, 88px);
  line-height: 1.0; font-weight: 400; letter-spacing: -0.02em;
  margin-bottom: 24px;
}
.hero h1 em { color: var(--accent); font-style: italic; }
.hero h1 .strike {
  text-decoration: line-through; text-decoration-color: var(--red);
  text-decoration-thickness: 3px; color: var(--text-dim);
}
.hero-sub {
  font-size: 17px; color: var(--text-dim); max-width: 580px;
  line-height: 1.6; margin-bottom: 32px;
}
.hero-sub strong { color: var(--text); }
.hero-meta {
  display: flex; gap: 20px; font-family: var(--mono); font-size: 11px;
  color: var(--text-faint); letter-spacing: 0.1em; flex-wrap: wrap;
}
.hero-meta span { display: flex; align-items: center; gap: 6px; }
.hero-meta span::before { content: '▸'; color: var(--accent); }

.ai-thinking {
  background: var(--bg-elevated); border: 1px solid var(--border);
  border-radius: 4px; padding: 24px;
  font-family: var(--mono); font-size: 12px;
  position: relative; overflow: hidden;
}
.ai-thinking::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, var(--accent), var(--red), var(--blue));
  opacity: 0.6;
}
.ai-thinking-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px; padding-bottom: 16px;
  border-bottom: 1px dashed var(--border);
  color: var(--text-dim); font-size: 10px; letter-spacing: 0.15em;
}
.ai-thinking-header .live { color: var(--green); display: flex; align-items: center; gap: 6px; }
.ai-thinking-content { line-height: 1.7; color: var(--text); min-height: 280px; }
.ai-thinking-content .think { color: var(--text-dim); font-style: italic; }
.ai-thinking-content .tag { color: var(--accent); }
.ai-thinking-content .ok { color: var(--green); }
.cursor {
  display: inline-block; width: 8px; height: 14px;
  background: var(--accent); animation: blink 1s infinite;
  vertical-align: text-bottom;
}
@keyframes blink { 50% { opacity: 0; } }

.stats-bar {
  display: grid; grid-template-columns: repeat(6, 1fr);
  border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);
  background: var(--bg-elevated);
}
.stat {
  padding: 24px; border-right: 1px solid var(--border);
  position: relative; transition: background 0.2s;
}
.stat:last-child { border-right: none; }
.stat:hover { background: var(--bg-card); }
.stat-label {
  font-family: var(--mono); font-size: 10px; color: var(--text-faint);
  letter-spacing: 0.15em; margin-bottom: 8px;
}
.stat-value {
  font-family: var(--display); font-size: 48px; font-weight: 400;
  letter-spacing: -0.03em; line-height: 1; color: var(--text);
}
.stat-value.accent { color: var(--accent); }
.stat-value.red { color: var(--red); }
.stat-value.warm { color: var(--amber); }
.stat-value.cold { color: var(--blue); }
.stat-sub { font-family: var(--mono); font-size: 11px; color: var(--text-dim); margin-top: 6px; }

.main {
  position: relative; z-index: 1; max-width: 1600px;
  margin: 0 auto; padding: 48px 48px 120px;
}
.section-title {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 32px; padding-top: 60px; gap: 24px; flex-wrap: wrap;
}
.section-title h2 {
  font-family: var(--display); font-size: 44px; font-weight: 400;
  letter-spacing: -0.02em;
}
.section-title h2 em { color: var(--accent); font-style: italic; }
.section-meta {
  font-family: var(--mono); font-size: 11px; color: var(--text-dim);
  letter-spacing: 0.15em;
}
.section-intro {
  color: var(--text-dim); max-width: 820px; margin-bottom: 32px; font-size: 15px;
}
.section-intro strong { color: var(--text); }

.faq-list { display: flex; flex-direction: column; gap: 1px; background: var(--border); }
.faq-item {
  background: var(--bg); padding: 24px 32px;
  cursor: pointer; transition: background 0.15s; position: relative;
}
.faq-item:hover { background: var(--bg-elevated); }
.faq-q { display: flex; justify-content: space-between; align-items: flex-start; gap: 24px; }
.faq-q-text {
  font-family: var(--display); font-size: 24px; font-weight: 400;
  line-height: 1.2; letter-spacing: -0.01em;
}
.faq-q-meta {
  font-family: var(--mono); font-size: 11px; color: var(--text-dim);
  flex-shrink: 0; text-align: right;
}
.faq-q-meta .count {
  color: var(--accent); font-size: 24px; display: block; font-family: var(--display);
}
.faq-toggle {
  font-family: var(--mono); font-size: 20px; color: var(--accent);
  margin-left: 12px; transition: transform 0.2s; flex-shrink: 0;
}
.faq-item.open .faq-toggle { transform: rotate(45deg); }
.faq-a {
  max-height: 0; overflow: hidden;
  transition: max-height 0.3s ease, margin-top 0.3s ease, padding 0.3s ease;
  color: var(--text); font-size: 15px; line-height: 1.7; white-space: pre-line;
}
.faq-item.open .faq-a {
  max-height: 1200px; margin-top: 20px; padding: 20px;
  background: var(--bg-elevated); border-left: 2px solid var(--accent);
}
.faq-a strong { color: var(--accent); }
.faq-samples {
  margin-top: 18px; padding-top: 14px; border-top: 1px dashed var(--border);
  font-family: var(--mono); font-size: 12px; color: var(--text-dim);
  line-height: 1.7;
}
.faq-samples .label {
  display: block; color: var(--text-faint); font-size: 10px;
  letter-spacing: 0.15em; margin-bottom: 8px;
}
.faq-samples blockquote {
  font-family: var(--display); font-style: italic; font-size: 14px;
  color: var(--text); padding-left: 12px; border-left: 2px solid var(--border-bright);
  margin: 6px 0;
}

.filters {
  display: flex; gap: 8px; flex-wrap: wrap;
  margin-bottom: 24px; font-family: var(--mono); font-size: 11px;
}
.filter {
  padding: 8px 14px; background: var(--bg-elevated);
  border: 1px solid var(--border); color: var(--text-dim);
  cursor: pointer; letter-spacing: 0.1em;
  transition: all 0.15s; text-transform: uppercase;
}
.filter:hover { color: var(--text); border-color: var(--border-bright); }
.filter.active {
  background: var(--accent); color: var(--bg);
  border-color: var(--accent); font-weight: 700;
}
.filter.hot { color: var(--red); border-color: rgba(255,77,77,0.4); }
.filter.hot.active { background: var(--red); color: #fff; border-color: var(--red); }
.filter.warm { color: var(--amber); border-color: rgba(255,153,51,0.4); }
.filter.warm.active { background: var(--amber); color: var(--bg); border-color: var(--amber); }
.filter.cold { color: var(--blue); border-color: rgba(77,159,255,0.4); }
.filter.cold.active { background: var(--blue); color: #fff; border-color: var(--blue); }
.filter.attended { color: var(--green); border-color: rgba(58,255,138,0.4); }
.filter.attended.active { background: var(--green); color: var(--bg); border-color: var(--green); }
.filter-search {
  margin-left: auto; display: flex; align-items: center;
  background: var(--bg-elevated); border: 1px solid var(--border);
  padding: 6px 12px; font-family: var(--mono); min-width: 240px;
}
.filter-search input {
  background: transparent; border: none; color: var(--text);
  font-family: var(--mono); font-size: 12px; outline: none; width: 100%;
}
.filter-search::before { content: '/'; color: var(--accent); margin-right: 8px; }

.leads-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 16px;
}
.lead-card {
  background: var(--bg-elevated); border: 1px solid var(--border);
  padding: 20px; cursor: pointer; transition: all 0.2s;
  position: relative; overflow: hidden;
}
.lead-card::before {
  content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
  background: var(--border);
}
.lead-card.lvl-HOT::before { background: var(--red); box-shadow: 0 0 12px rgba(255,77,77,0.3); }
.lead-card.lvl-WARM::before { background: var(--amber); }
.lead-card.lvl-COLD::before { background: var(--blue); }
.lead-card.lvl-NEUTRAL::before { background: var(--text-faint); }
.lead-card:hover { border-color: var(--border-bright); transform: translateY(-2px); }
.lead-card.lvl-HOT:hover { border-color: var(--red-dim); }
.lead-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; gap: 12px; }
.lead-name {
  font-family: var(--display); font-size: 22px; font-weight: 400;
  letter-spacing: -0.01em; line-height: 1.1; margin-bottom: 4px;
}
.lead-role { font-family: var(--mono); font-size: 11px; color: var(--text-dim); letter-spacing: 0.05em; }
.lead-role .at { color: var(--text-faint); margin: 0 4px; }
.lead-role .company { color: var(--accent); }
.lead-tier { font-family: var(--mono); font-size: 10px; letter-spacing: 0.1em; text-align: right; flex-shrink: 0; }
.lead-tier .lvl { font-family: var(--display); font-size: 24px; line-height: 1; font-weight: 400; }
.lead-card.lvl-HOT .lvl { color: var(--red); }
.lead-card.lvl-WARM .lvl { color: var(--amber); }
.lead-card.lvl-COLD .lvl { color: var(--blue); }
.lead-card.lvl-NEUTRAL .lvl { color: var(--text-dim); }
.lead-tags { display: flex; gap: 6px; flex-wrap: wrap; margin: 12px 0; }
.tag {
  font-family: var(--mono); font-size: 9px; padding: 3px 7px;
  background: rgba(255,255,255,0.04); border: 1px solid var(--border);
  color: var(--text-dim); letter-spacing: 0.1em; text-transform: uppercase;
}
.tag.dm { color: var(--accent); border-color: var(--accent-dim); }
.tag.big { color: var(--red); border-color: var(--red-dim); }
.tag.attended { color: var(--green); background: rgba(58,255,138,0.08); border-color: rgba(58,255,138,0.3); }
.lead-question {
  font-size: 13px; color: var(--text); font-style: italic;
  border-left: 2px solid var(--border-bright);
  padding-left: 12px; margin-top: 12px; line-height: 1.5;
  display: -webkit-box; -webkit-line-clamp: 3;
  -webkit-box-orient: vertical; overflow: hidden;
}
.lead-question.empty { color: var(--text-faint); font-style: normal; }
.lead-question::before { content: '"'; color: var(--accent); margin-right: 2px; }
.lead-question::after { content: '"'; color: var(--accent); margin-left: 2px; }
.lead-question.empty::before, .lead-question.empty::after { display: none; }

.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.85); backdrop-filter: blur(8px);
  z-index: 1000; display: none;
  align-items: center; justify-content: center; padding: 40px;
}
.modal-overlay.active { display: flex; }
.modal {
  background: var(--bg); border: 1px solid var(--border-bright);
  max-width: 920px; width: 100%; max-height: 90vh;
  overflow-y: auto; position: relative;
}
.modal::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--red));
}
.modal-close {
  position: absolute; top: 16px; right: 16px;
  background: transparent; border: 1px solid var(--border);
  color: var(--text-dim); cursor: pointer;
  width: 32px; height: 32px; font-family: var(--mono); font-size: 16px;
  display: flex; align-items: center; justify-content: center; z-index: 2;
}
.modal-close:hover { color: var(--accent); border-color: var(--accent-dim); }
.modal-body { padding: 48px; }
.modal-header { margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }
.modal-header .lvl-badge {
  display: inline-block; font-family: var(--mono); font-size: 11px;
  padding: 4px 10px; border: 1px solid var(--border);
  margin-bottom: 12px; letter-spacing: 0.15em;
}
.modal-header .lvl-badge.HOT { color: var(--red); border-color: var(--red-dim); background: rgba(255,77,77,0.08); }
.modal-header .lvl-badge.WARM { color: var(--amber); border-color: rgba(255,153,51,0.3); background: rgba(255,153,51,0.06); }
.modal-header .lvl-badge.COLD { color: var(--blue); border-color: rgba(77,159,255,0.3); }
.modal-header .lvl-badge.NEUTRAL { color: var(--text-dim); }
.modal-header h2 {
  font-family: var(--display); font-size: 48px; font-weight: 400;
  letter-spacing: -0.02em; line-height: 1.05; margin-bottom: 8px;
}
.modal-header .modal-role {
  font-family: var(--mono); color: var(--text-dim);
  font-size: 13px; letter-spacing: 0.05em;
}
.modal-header .modal-role .company { color: var(--accent); }
.modal-section { margin-bottom: 32px; }
.modal-section-title {
  font-family: var(--mono); font-size: 11px; color: var(--text-dim);
  letter-spacing: 0.2em; margin-bottom: 16px;
  display: flex; align-items: center; gap: 12px;
}
.modal-section-title::before { content: ''; width: 16px; height: 1px; background: var(--accent); }
.modal-question {
  font-family: var(--display); font-size: 24px; font-style: italic;
  line-height: 1.4; color: var(--text);
  padding: 20px 24px; border-left: 3px solid var(--accent);
  background: rgba(199,243,82,0.03);
}
.modal-question.empty { color: var(--text-faint); font-style: normal; font-size: 16px; font-family: var(--mono); }
.suggested-answer {
  background: var(--bg-elevated);
  border: 1px solid var(--accent-dim);
  border-left: 3px solid var(--accent);
  padding: 24px;
  font-family: var(--sans);
  font-size: 15px;
  line-height: 1.65;
  color: var(--text);
  position: relative;
  white-space: pre-wrap;
}
.suggested-answer::before {
  content: 'RESPUESTA LISTA PARA ENVIAR';
  position: absolute;
  top: -8px; left: 16px;
  background: var(--bg);
  padding: 0 8px;
  font-size: 9px;
  color: var(--accent);
  letter-spacing: 0.2em;
  font-family: var(--mono);
}

.modal-cta { display: flex; gap: 12px; margin-top: 24px; flex-wrap: wrap; }
.btn {
  font-family: var(--mono); font-size: 11px;
  padding: 12px 24px; background: transparent;
  border: 1px solid var(--border-bright); color: var(--text);
  cursor: pointer; letter-spacing: 0.15em;
  text-transform: uppercase; transition: all 0.15s;
  text-decoration: none; display: inline-flex; align-items: center; gap: 6px;
}
.btn:hover { background: var(--bg-elevated); color: var(--accent); }
.btn.primary { background: var(--accent); color: var(--bg); border-color: var(--accent); font-weight: 700; }
.btn.primary:hover { background: var(--text); border-color: var(--text); color: var(--bg); }
.btn:disabled { opacity: 0.4; cursor: not-allowed; }

.proposal-section {
  background: var(--bg-elevated); border: 1px solid var(--border);
  padding: 40px; position: relative;
}
.proposal-section::before {
  content: 'LIVE GENERATION'; position: absolute; top: -8px; left: 32px;
  background: var(--bg); padding: 0 12px;
  font-family: var(--mono); font-size: 10px;
  letter-spacing: 0.25em; color: var(--accent);
}
.proposal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.proposal-output {
  background: var(--bg); border: 1px solid var(--border);
  padding: 24px; min-height: 240px;
  font-family: var(--mono); font-size: 13px;
  line-height: 1.7; white-space: pre-wrap; color: var(--text); margin-top: 16px;
}
.proposal-output:empty::before {
  content: 'Seleccioná un lead arriba (click en "Generar propuesta nueva en vivo" dentro del modal) — Claude escribe la propuesta custom con datos reales del programa.';
  color: var(--text-faint); font-style: italic;
}

.notes-area {
  width: 100%; background: var(--bg); border: 1px solid var(--border);
  color: var(--text); padding: 12px; border-radius: 4px;
  font-family: inherit; font-size: 13px; resize: vertical; min-height: 80px;
}
.notes-area:focus { outline: none; border-color: var(--accent); }

.toast {
  position: fixed; bottom: 24px; left: 50%;
  transform: translateX(-50%) translateY(80px);
  background: var(--accent); color: var(--bg);
  padding: 10px 20px; border-radius: 4px;
  font-family: var(--mono); font-size: 12px;
  text-transform: uppercase; letter-spacing: 0.1em;
  font-weight: 700; transition: transform .25s cubic-bezier(.16,1,.3,1);
  z-index: 2000;
}
.toast.show { transform: translateX(-50%) translateY(0); }

.load-more {
  display: block; margin: 32px auto 0;
  padding: 14px 32px; background: transparent;
  border: 1px solid var(--border); color: var(--text-dim);
  font-family: var(--mono); font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.12em;
  cursor: pointer; transition: all .15s;
}
.load-more:hover { border-color: var(--accent); color: var(--accent); }

.meta-footer {
  margin-top: 80px; padding: 40px 48px;
  border-top: 1px solid var(--border); background: var(--bg-elevated);
  font-family: var(--mono); font-size: 11px; color: var(--text-dim);
}
.meta-footer-inner {
  max-width: 1600px; margin: 0 auto;
  display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 48px;
}
.meta-footer h4 {
  font-family: var(--display); font-size: 20px; font-weight: 400;
  color: var(--text); margin-bottom: 12px; font-style: italic;
}
.meta-footer p { line-height: 1.7; }
.meta-footer .stack-list { line-height: 2; }
.meta-footer .stack-list span { color: var(--accent); }

@media (max-width: 1100px) {
  .hero-grid { grid-template-columns: 1fr; }
  .stats-bar { grid-template-columns: repeat(3, 1fr); }
  .stats-bar .stat:nth-child(3) { border-right: none; }
  .stats-bar .stat { border-bottom: 1px solid var(--border); }
  .meta-footer-inner { grid-template-columns: 1fr; }
}
@media (max-width: 700px) {
  .hero { padding: 48px 24px; }
  .main { padding: 24px 24px 80px; }
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
  .section-title { padding-top: 40px; flex-direction: column; align-items: flex-start; gap: 8px; }
  .section-title h2 { font-size: 32px; }
  .modal-body { padding: 28px; }
  .modal-header h2 { font-size: 32px; }
  .leads-grid { grid-template-columns: 1fr; }
  .topbar { padding: 10px 16px; font-size: 10px; flex-wrap: wrap; gap: 8px; }
  .topbar-right span { padding: 3px 6px; }
  .faq-q-text { font-size: 18px; }
}
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-bright); }
</style>
</head>
<body>

<div class="topbar">
  <div class="topbar-left">
    <span class="brand">30X · AI SALES</span>
    <span class="topbar-status"><span class="dot-live"></span>LIVE FROM WEBINAR</span>
  </div>
  <div class="topbar-right">
    <span id="clock">--:--:--</span>
    <span>n = __TOTAL__ leads</span>
    <span class="highlight">hot = __HOT__</span>
    <a href="__CHECKOUT_URL__" target="_blank" class="promo-pill">PROMO · USD 1.750 · __CUPOS_PROMO__ CUPOS →</a>
  </div>
</div>

<section class="hero">
  <div class="hero-grid">
    <div>
      <div class="hero-eyebrow">SISTEMA DE INTELIGENCIA DE LEADS · CONSTRUIDO EN VIVO</div>
      <h1>
        Esto no es un<br>
        <span class="strike">webinar más</span><br>
        es <em>el output</em><br>
        del programa.
      </h1>
      <p class="hero-sub">
        Tomamos las <strong>__TOTAL__ inscripciones</strong> al webinar 30X AI Sales, las pasamos por un sistema construido <strong>en horas, sin developers</strong>, y ahora sabemos: quién es <strong>decision maker</strong>, qué <strong>preguntó</strong> cada uno, qué <strong>módulo del programa</strong> le resuelve eso, y exactamente <strong>qué propuesta enviarle</strong>. Esto es lo que vas a salir construyendo del programa. No diapositivas. Sistemas.
      </p>
      <div class="hero-meta">
        <span>__TOTAL__ leads procesados</span>
        <span>__HOT__ de alta intención pre-seleccionados</span>
        <span>__CATS__ categorías de pregunta detectadas</span>
        <span>0 líneas escritas por developer</span>
      </div>
    </div>
    <div class="ai-thinking">
      <div class="ai-thinking-header">
        <span>system://claude · reasoning_log</span>
        <span class="live"><span class="dot-live"></span>STREAMING</span>
      </div>
      <div class="ai-thinking-content" id="thinking-stream"></div>
    </div>
  </div>
</section>

<div class="stats-bar">
  <div class="stat">
    <div class="stat-label">TOTAL LEADS</div>
    <div class="stat-value">__TOTAL__</div>
    <div class="stat-sub">inscritos al webinar</div>
  </div>
  <div class="stat">
    <div class="stat-label">HOT · INTENCIÓN COMPRA</div>
    <div class="stat-value red">__HOT__</div>
    <div class="stat-sub">prioridad 1 · llamada en 24h</div>
  </div>
  <div class="stat">
    <div class="stat-label">WARM · INTERÉS PROFUNDO</div>
    <div class="stat-value warm">__WARM__</div>
    <div class="stat-sub">técnica o de fit</div>
  </div>
  <div class="stat">
    <div class="stat-label">DECISION MAKERS</div>
    <div class="stat-value accent">__DM__</div>
    <div class="stat-sub">CEO · Founder · Director · C-level</div>
  </div>
  <div class="stat">
    <div class="stat-label">EMPRESAS GRANDES</div>
    <div class="stat-value">__BIG__</div>
    <div class="stat-sub">enterprise detectadas en la base</div>
  </div>
  <div class="stat">
    <div class="stat-label">PREGUNTAS REALES</div>
    <div class="stat-value">__QREAL__</div>
    <div class="stat-sub">__CATS__ intents detectados</div>
  </div>
</div>

<main class="main">

  <div class="section-title">
    <h2>Lo que <em>todos</em> quieren saber.</h2>
    <span class="section-meta">FAQ · agrupado por intent · ordenado por frecuencia</span>
  </div>
  <p class="section-intro">
    De las <strong>__QREAL__ preguntas reales</strong> recibidas en el formulario de inscripción, la IA detectó <strong>__CATS__ intents distintos</strong>. Estas son las respuestas oficiales del equipo de admisiones, listas para usar en vivo. Click para expandir.
  </p>
  <div class="faq-list" id="faq-list"></div>

  <div class="section-title">
    <h2>Cada lead, <em>analizado</em>.</h2>
    <span class="section-meta">nivel de intención · respuesta lista · click para abrir</span>
  </div>
  <p class="section-intro">
    Cada lead tiene <strong>nivel de intención</strong> detectado por la IA (HOT / WARM / COLD / NEUTRAL) y una <strong>respuesta personalizada pre-generada</strong> basada en su pregunta + datos reales del programa. Click en cualquiera para ver la respuesta y mandarla por Gmail o WhatsApp en un clic.
  </p>

  <div class="filters">
    <button class="filter active" data-filter="ALL">Todos · __TOTAL__</button>
    <button class="filter hot" data-filter="HOT">Hot · __HOT__</button>
    <button class="filter warm" data-filter="WARM">Warm · __WARM__</button>
    <button class="filter cold" data-filter="COLD">Cold · __COLD__</button>
    <button class="filter" data-filter="NEUTRAL">Neutral · __NEUTRAL__</button>
    <button class="filter" data-filter="DM">Decision makers · __DM__</button>
    <button class="filter attended" data-filter="ATTENDED">Asistieron · __ATTENDED__</button>
    <div class="filter-search">
      <input type="text" id="search" placeholder="buscar nombre / empresa / rol...">
    </div>
  </div>

  <div class="leads-grid" id="leads-grid"></div>
  <button class="load-more" id="load-more" style="display:none">Cargar más</button>

  <div class="section-title">
    <h2>Propuesta personalizada, <em>al instante</em>.</h2>
    <span class="section-meta">Claude API · sin templates</span>
  </div>
  <p class="section-intro">
    Seleccioná un lead arriba y dale a <strong>"Generar propuesta nueva en vivo"</strong> dentro del modal. El proxy llama a Claude vía API con el contexto completo del lead + datos del programa, y escribe la propuesta custom en tiempo real. Es el mismo motor que vas a construir en los módulos 4 y 6 del programa.
  </p>
  <div class="proposal-section">
    <div class="proposal-header">
      <div>
        <div style="font-family: var(--mono); font-size: 10px; color: var(--text-dim); letter-spacing: 0.2em; margin-bottom: 6px;">CONTEXTO DEL LEAD</div>
        <div id="proposal-context" style="font-family: var(--display); font-size: 22px; font-style: italic; color: var(--text);">— ningún lead seleccionado —</div>
      </div>
    </div>
    <div class="proposal-output" id="proposal-output-bottom"></div>
  </div>

</main>

<div class="modal-overlay" id="modal-overlay">
  <div class="modal">
    <button class="modal-close" onclick="closeModal()">×</button>
    <div class="modal-body" id="modal-body"></div>
  </div>
</div>

<div class="toast" id="toast">Copiado</div>

<div class="meta-footer">
  <div class="meta-footer-inner">
    <div>
      <h4>¿Cómo se construyó esto?</h4>
      <p>Este dashboard se construyó <strong style="color: var(--accent);">en horas, sin developers</strong>, usando <strong>Claude</strong> para el análisis y razonamiento sobre cada lead, <strong>Claude Code</strong> para generar el frontend, y un único HTML deployable en Vercel. Es exactamente el tipo de sistema que vas a salir construyendo del programa 30X AI Sales: cosas reales que mueven la operación comercial, no slides.</p>
    </div>
    <div>
      <h4>Stack utilizado</h4>
      <div class="stack-list">
        <span>›</span> Claude (reasoning)<br>
        <span>›</span> Claude Code (vibecoding)<br>
        <span>›</span> Python (procesamiento CSV)<br>
        <span>›</span> Vanilla HTML/JS (zero framework)<br>
        <span>›</span> Vercel serverless (proxy a Claude API)
      </div>
    </div>
    <div>
      <h4>Promo asistentes al webinar</h4>
      <p style="color: var(--accent); font-family: var(--mono); font-size: 12px;">USD 200 OFF · SOLO __CUPOS_PROMO__ CUPOS.</p>
      <p style="margin-top: 12px;">Precio regular USD 1.950 → <strong style="color: var(--accent);">USD 1.750 por inscribirte hoy</strong>. 4 semanas, 8 sesiones en vivo con Nicolás Rojas (Dapta) y Andrés Bilbao (Rappi).</p>
      <p style="margin-top: 16px;"><a href="__CHECKOUT_URL__" target="_blank" style="display: inline-block; background: var(--accent); color: var(--bg); padding: 12px 18px; font-family: var(--mono); font-size: 11px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; text-decoration: none;">Reservar con descuento →</a></p>
      <p style="margin-top: 10px; font-size: 10px;"><a href="__CURSO_URL__" target="_blank" style="color: var(--text-dim); text-decoration: underline;">o ver página del programa</a></p>
    </div>
  </div>
</div>

<script>
// ============ CONFIG ============
const PROXY_URL = "__PROXY_URL__";
const CALENDLY_URL = "__CALENDLY_URL__";
const CURSO_URL = "__CURSO_URL__";
const CHECKOUT_URL = "__CHECKOUT_URL__";

// ============ DATA ============
__LEADS_JSON__

__FAQS_JSON__

const DECISION_KW = __DECISION_KW__;

// ============ STATE ============
let currentFilter = "ALL";
let currentSearch = "";
let pageSize = 60;
let displayed = pageSize;

// Orden: HOT > WARM > COLD > NEUTRAL, asistieron primero
const LVL_ORDER = { HOT: 0, WARM: 1, COLD: 2, NEUTRAL: 3 };
LEADS.sort((a, b) => {
  const o = LVL_ORDER[a.i] - LVL_ORDER[b.i];
  if (o !== 0) return o;
  return (b.a === "Si" ? 1 : 0) - (a.a === "Si" ? 1 : 0);
});

// ============ HELPERS ============
function escapeHtml(s) {
  if (!s) return "";
  return String(s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
function isDecisionMaker(role) {
  const r = (role || "").toLowerCase();
  return DECISION_KW.some(k => r.includes(k));
}
function mdInline(s) {
  // **bold** → <strong>; preserva line-breaks como <br>
  return escapeHtml(s)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>');
}

// ============ CLOCK ============
function tickClock() {
  const d = new Date();
  const pad = n => String(n).padStart(2, "0");
  document.getElementById("clock").textContent = `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}
tickClock();
setInterval(tickClock, 1000);

// ============ AI THINKING STREAM (simulado) ============
const THINKING_LINES = [
  { txt: "» loading dataset registros-luma.csv... ", cls: "think" },
  { txt: "ok · __TOTAL__ rows · 0 errors\n", cls: "ok" },
  { txt: "» normalizing names (title case)...\n», deduping emails...\n", cls: "think" },
  { txt: "» extracting question column 'qué preguntas tienes acerca del programa de 30X \"AI Sales\"'\n", cls: "think" },
  { txt: "» __QREAL__ preguntas con contenido real · __EMPTY__ vacías\n", cls: "tag" },
  { txt: "» clasificando por intent... ", cls: "think" },
  { txt: "ok · __CATS__ categorías detectadas\n", cls: "ok" },
  { txt: "» segmentando por nivel de intención...\n  HOT __HOT__ · WARM __WARM__ · COLD __COLD__ · NEUTRAL __NEUTRAL__\n", cls: "tag" },
  { txt: "» detectando decision makers (CEO, Founder, Director, C-level)...\n  __DM__ identificados\n", cls: "tag" },
  { txt: "» matching empresas grandes contra base enterprise...\n  __BIG__ matches\n", cls: "tag" },
  { txt: "» generando respuesta personalizada por lead (Claude Sonnet 4.6)...\n  Conectando pregunta → módulo del programa.\n  Citando precio (USD 1.950), 4 semanas, 8 módulos, mentores Rojas+Bilbao.\n  Sin emojis. Sin marketingese. Tono Dylan / 30X.\n", cls: "think" },
  { txt: "» __TOTAL__ propuestas listas para enviar\n", cls: "ok" },
  { txt: "» dashboard live\n», botón \"GENERAR PROPUESTA\" conectado a /api/claude (Vercel proxy)\n», ready.\n", cls: "ok" },
];
function streamThinking() {
  const el = document.getElementById("thinking-stream");
  el.innerHTML = "";
  let i = 0, charIdx = 0, span = null;
  function step() {
    if (i >= THINKING_LINES.length) {
      el.insertAdjacentHTML("beforeend", '<span class="cursor"></span>');
      return;
    }
    const cur = THINKING_LINES[i];
    if (!span) {
      span = document.createElement("span");
      span.className = cur.cls;
      el.appendChild(span);
    }
    if (charIdx < cur.txt.length) {
      span.textContent += cur.txt[charIdx++];
      el.scrollTop = el.scrollHeight;
      setTimeout(step, 8 + Math.random() * 12);
    } else {
      i++; charIdx = 0; span = null;
      setTimeout(step, 100);
    }
  }
  step();
}
streamThinking();

// ============ FAQ ============
function renderFAQ() {
  const html = FAQS.map((f, idx) => `
    <div class="faq-item" data-idx="${idx}" onclick="toggleFAQ(${idx})">
      <div class="faq-q">
        <div>
          <div class="faq-q-text">${escapeHtml(f.label)}</div>
        </div>
        <div class="faq-q-meta">
          <span class="count">${f.count}</span>
          <span>preguntas</span>
        </div>
        <span class="faq-toggle">+</span>
      </div>
      <div class="faq-a">
        <div>${mdInline(f.answer)}</div>
        ${f.samples && f.samples.length ? `
          <div class="faq-samples">
            <span class="label">EJEMPLOS REALES DEL FORMULARIO</span>
            ${f.samples.map(s => `<blockquote>${escapeHtml(s)}</blockquote>`).join("")}
          </div>` : ""}
      </div>
    </div>
  `).join("");
  document.getElementById("faq-list").innerHTML = html;
}
function toggleFAQ(idx) {
  document.querySelector(`.faq-item[data-idx="${idx}"]`).classList.toggle("open");
}
renderFAQ();

// ============ LEADS GRID ============
function getFiltered() {
  const q = currentSearch.toLowerCase();
  return LEADS.filter(l => {
    if (currentFilter === "ATTENDED" && l.a !== "Si") return false;
    if (currentFilter === "DM" && !isDecisionMaker(l.r)) return false;
    if (["HOT","WARM","COLD","NEUTRAL"].includes(currentFilter) && l.i !== currentFilter) return false;
    if (q) {
      const hay = (l.n + " " + l.c + " " + l.r + " " + l.q).toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
}
function renderCards() {
  const filtered = getFiltered();
  const slice = filtered.slice(0, displayed);
  const grid = document.getElementById("leads-grid");
  grid.innerHTML = slice.map(l => {
    const idx = LEADS.indexOf(l);
    const isEmpty = l.q === "[VACIO]";
    const qDisplay = isEmpty ? "Sin pregunta del formulario" : (l.q.length > 160 ? l.q.slice(0, 160) + "..." : l.q);
    const dm = isDecisionMaker(l.r);
    const attended = l.a === "Si";
    return `
      <div class="lead-card lvl-${l.i}" onclick="openModal(${idx})">
        <div class="lead-header">
          <div>
            <div class="lead-name">${escapeHtml(l.n)}</div>
            <div class="lead-role">${escapeHtml(l.r || "—")} <span class="at">@</span> <span class="company">${escapeHtml(l.c || "—")}</span></div>
          </div>
          <div class="lead-tier">
            <div class="lvl">${l.i}</div>
            <div>${escapeHtml(l.u)}</div>
          </div>
        </div>
        <div class="lead-tags">
          ${dm ? '<span class="tag dm">decision maker</span>' : ''}
          ${attended ? '<span class="tag attended">asistió</span>' : ''}
        </div>
        <div class="lead-question ${isEmpty ? 'empty' : ''}">${escapeHtml(qDisplay)}</div>
      </div>
    `;
  }).join("");
  const lm = document.getElementById("load-more");
  lm.style.display = filtered.length > displayed ? "block" : "none";
  lm.textContent = `Cargar más · ${filtered.length - displayed} restantes`;
}

// ============ MODAL ============
function openModal(idx) {
  const l = LEADS[idx];
  const isEmpty = l.q === "[VACIO]";
  const mailtoSubject = encodeURIComponent(`${l.n.split(" ")[0]}, respuesta a tu pregunta del webinar 30X AI Sales`);
  const mailtoBody = encodeURIComponent(l.p);
  const waMessage = encodeURIComponent(`Hola ${l.n.split(" ")[0]}, soy del equipo de 30X. ${l.p}`);
  const waNumber = (l.t || "").replace(/[^\d]/g, "");
  const noteKey = `note_${l.e}`;
  const savedNote = localStorage.getItem(noteKey) || "";

  document.getElementById("proposal-context").textContent = `${l.n} · ${l.r || "—"} @ ${l.c || "—"}`;
  document.getElementById("proposal-output-bottom").textContent = "";

  document.getElementById("modal-body").innerHTML = `
    <div class="modal-header">
      <span class="lvl-badge ${l.i}">${l.i}</span>
      ${l.a === "Si" ? '<span class="lvl-badge" style="color: var(--green); border-color: rgba(58,255,138,0.3); margin-left: 8px;">ASISTIÓ</span>' : ''}
      ${isDecisionMaker(l.r) ? '<span class="lvl-badge" style="color: var(--accent); border-color: var(--accent-dim); margin-left: 8px;">DECISION MAKER</span>' : ''}
      <h2>${escapeHtml(l.n)}</h2>
      <div class="modal-role">${escapeHtml(l.r || "—")} <span style="color: var(--text-faint)">@</span> <span class="company">${escapeHtml(l.c || "—")}</span></div>
      <div class="modal-role" style="margin-top: 8px;">${escapeHtml(l.e)}${l.t ? ' · ' + escapeHtml(l.t) : ''} · UTM: ${escapeHtml(l.u)}</div>
    </div>

    <div class="modal-section">
      <div class="modal-section-title">PREGUNTA DEL FORMULARIO</div>
      <div class="modal-question ${isEmpty ? 'empty' : ''}">
        ${isEmpty ? 'No completó la pregunta del formulario.' : escapeHtml(l.q)}
      </div>
    </div>

    <div class="modal-section">
      <div class="modal-section-title">RESPUESTA PERSONALIZADA</div>
      <div class="suggested-answer">${escapeHtml(l.p)}</div>
    </div>

    <div class="modal-cta">
      <button class="btn primary" id="btn-generate" onclick="generateProposal(${idx})">Generar propuesta nueva en vivo →</button>
      <button class="btn" onclick="copyText(LEADS[${idx}].p)">Copiar respuesta</button>
      <a class="btn" href="mailto:${escapeHtml(l.e)}?subject=${mailtoSubject}&body=${mailtoBody}" target="_blank">Abrir en Gmail</a>
      ${waNumber ? `<a class="btn" href="https://wa.me/${waNumber}?text=${waMessage}" target="_blank">Abrir en WhatsApp</a>` : ''}
      <a class="btn" href="${CALENDLY_URL}" target="_blank">Agendar llamada</a>
      <a class="btn primary" href="${CHECKOUT_URL}" target="_blank">Reservar USD 1.750 →</a>
    </div>

    <div class="modal-section" style="margin-top: 32px;">
      <div class="modal-section-title">NOTAS INTERNAS · GUARDADAS EN ESTE NAVEGADOR</div>
      <textarea class="notes-area" id="notes" placeholder="Notas privadas sobre este lead..." oninput="localStorage.setItem('${noteKey}', this.value)">${escapeHtml(savedNote)}</textarea>
    </div>

    <div class="modal-section">
      <div class="modal-section-title">PROPUESTA GENERADA POR CLAUDE EN VIVO</div>
      <div class="proposal-output" id="proposal-output"></div>
    </div>
  `;

  document.getElementById("modal-overlay").classList.add("active");
  document.body.style.overflow = "hidden";
}
function closeModal() {
  document.getElementById("modal-overlay").classList.remove("active");
  document.body.style.overflow = "";
}
document.getElementById("modal-overlay").addEventListener("click", e => {
  if (e.target.id === "modal-overlay") closeModal();
});
document.addEventListener("keydown", e => { if (e.key === "Escape") closeModal(); });

// ============ COPY ============
function copyText(t) {
  navigator.clipboard.writeText(t).then(() => {
    const toast = document.getElementById("toast");
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 1500);
  });
}

// ============ GENERATE PROPOSAL (proxy) ============
async function generateProposal(idx) {
  const l = LEADS[idx];
  const btn = document.getElementById("btn-generate");
  const out = document.getElementById("proposal-output");
  const outBottom = document.getElementById("proposal-output-bottom");

  btn.disabled = true;
  btn.textContent = "Generando...";
  out.textContent = "» llamando a Claude...";
  if (outBottom) outBottom.textContent = "» llamando a Claude...";

  const prompt = `Sos parte del equipo de 30X. Escribime una propuesta personalizada para este lead que se registró al webinar "30X AI Sales: Cómo Clonar a tu Mejor Vendedor con AI".

Datos del lead:
- Nombre: ${l.n}
- Empresa: ${l.c || "no informa"}
- Rol: ${l.r || "no informa"}
- Pregunta original: ${l.q === "[VACIO]" ? "(no respondió la pregunta abierta)" : l.q}
- Nivel de intención detectado: ${l.i}

Contexto del programa 30X AI Sales (usalo como verdad, no inventes datos):
- 4 semanas, 8 módulos en vivo, 100% online, sesiones grabadas (1 año de acceso).
- Para líderes comerciales NO técnicos: heads of sales, directores comerciales, founders que venden, AEs, SDR/BDR leads, revenue leaders.
- Mentores: Nicolás Rojas (CEO Dapta, Forbes 30u30) y Andrés Bilbao (co-founder Rappi).
- 8 módulos: 1) AI Mindset & Stack del Top Performer, 2) Social Selling, 3) Outbound Inteligencia de Cuentas, 4) Outbound Hiper-Personalización a Escala, 5) Inbound Conversational AI & Speed-to-Lead, 6) Inbound Discovery & Follow-Up, 7) Sales Coaching con Conversational Intelligence, 8) RevOps Forecasting & Agentes Autónomos.
- Stack mencionado: n8n, Dapta, GPTs, agentes de voz, integraciones con CRM.
- Precio regular USD 1.950. **Promo activa para asistentes al webinar: USD 1.750 (USD 200 off), solo 15 cupos a este precio.** Reserva de cupo: USD 199. Cupos totales de la cohorte limitados a 100. +100K créditos Dapta gratis. Certificado oficial 30X Executive Education.
- URL del programa: ${CURSO_URL}
- Link de checkout con descuento USD 1.750: ${CHECKOUT_URL}

La propuesta debe:
1. Saludo personal por nombre (solo primer nombre).
2. Referencia específica a su pregunta o contexto de su rol/empresa.
3. Conectar con el módulo concreto del programa que resuelve eso.
4. Mencionar que se trabaja sobre el pipeline real del lead, no demos genéricas.
5. Call to action: **Reservar con el descuento USD 1.750 vía ${CHECKOUT_URL}** (mencionar que quedan 15 cupos a ese precio) o agendar llamada (${CALENDLY_URL}) si necesita despejar dudas antes.

Máximo 200 palabras. Tono Dylan Pereira / 30X: directo, cercano, sin marketingese, sin emojis, sin promesas vacías.`;

  try {
    const res = await fetch(PROXY_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const txt = data.text || data.content?.[0]?.text || JSON.stringify(data);
    out.textContent = txt;
    if (outBottom) outBottom.textContent = txt;
  } catch (err) {
    out.innerHTML = `<span style="color: var(--red)">⚠ Error: ${escapeHtml(err.message)}</span>\n\nUsá la respuesta pre-generada arriba como plan B.`;
    if (outBottom) outBottom.innerHTML = out.innerHTML;
  } finally {
    btn.disabled = false;
    btn.textContent = "Generar otra propuesta →";
  }
}

// ============ EVENT LISTENERS ============
document.getElementById("search").addEventListener("input", e => {
  currentSearch = e.target.value;
  displayed = pageSize;
  renderCards();
});
document.querySelectorAll(".filter").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentFilter = btn.dataset.filter;
    displayed = pageSize;
    renderCards();
  });
});
document.getElementById("load-more").addEventListener("click", () => {
  displayed += pageSize;
  renderCards();
});
renderCards();
</script>
</body>
</html>
"""


def main():
    rows = load_rows()
    q_counts, samples = categorize_questions(rows)
    stats = build_stats(rows, q_counts)
    leads = build_leads(rows)
    faqs = build_faqs(q_counts, samples)

    leads_json = "const LEADS = " + json.dumps(leads, ensure_ascii=False, separators=(",", ":")) + ";"
    faqs_json = "const FAQS = " + json.dumps(faqs, ensure_ascii=False) + ";"
    dm_json = json.dumps(DECISION_KW)

    html = HTML
    replacements = {
        "__PROXY_URL__": PROXY_URL,
        "__CALENDLY_URL__": CALENDLY_URL,
        "__CURSO_URL__": CURSO_URL,
        "__CHECKOUT_URL__": CHECKOUT_URL,
        "__CUPOS_PROMO__": str(CUPOS_PROMO),
        "__LEADS_JSON__": leads_json,
        "__FAQS_JSON__": faqs_json,
        "__DECISION_KW__": dm_json,
        "__TOTAL__": str(stats["total"]),
        "__HOT__": str(stats["hot"]),
        "__WARM__": str(stats["warm"]),
        "__COLD__": str(stats["cold"]),
        "__NEUTRAL__": str(stats["neutral"]),
        "__ATTENDED__": str(stats["attended"]),
        "__DM__": str(stats["decision_makers"]),
        "__BIG__": str(stats["enterprise"]),
        "__QREAL__": str(stats["real_questions"]),
        "__EMPTY__": str(stats["total"] - stats["real_questions"]),
        "__CATS__": str(stats["categories_count"]),
    }
    for k, v in replacements.items():
        html = html.replace(k, v)

    OUT_PATH.write_text(html, encoding="utf-8")
    print(f"OK · index.html generated · {OUT_PATH.stat().st_size // 1024} KB")
    print(f"   · {stats['total']} leads")
    print(f"   · {stats['real_questions']} preguntas reales en {stats['categories_count']} categorías")
    print(f"   · {stats['decision_makers']} decision makers · {stats['enterprise']} enterprise")


if __name__ == "__main__":
    main()
