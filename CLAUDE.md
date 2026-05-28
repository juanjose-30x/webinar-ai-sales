# CLAUDE.md — Webinar 30X AI Sales (Cómo Clonar a tu Mejor Vendedor con AI)

> Este archivo es la instrucción maestra para que Claude (Code o claude.ai) replique el flujo del **Webinar Xtreme Growth** adaptado al **Webinar 30X AI Sales**.
>
> Repo de referencia (resultado a replicar): https://github.com/cristina-barbosa-sabagh/Webinar-Xtreme-Growth
> Demo en vivo de referencia: https://webinar-xtreme-growth.vercel.app

---

## 0. Contexto del proyecto

Estamos armando el dashboard interactivo del **Webinar 30X "AI Sales": Cómo Clonar a tu Mejor Vendedor con AI** de Growth Rockstar / 30X. El dashboard cumple tres roles:

1. **ANTES del webinar:** procesar el CSV de Luma, segmentar leads por intención de compra, generar respuesta personalizada para cada uno.
2. **DURANTE el webinar:** mostrarse en vivo como prueba social. El botón "GENERAR PROPUESTA" llama a Claude vía API y muestra una propuesta nueva en vivo (el wow moment).
3. **DESPUÉS del webinar:** ser la base operativa del equipo comercial para mandar mensajes personalizados por correo y WhatsApp en las primeras 72h.

**El insight clave: el dashboard se construye ANTES y se USA durante.** Es lo que diferencia este webinar de cualquier otro.

---

## 1. Datos del webinar (rellenar antes de empezar)

| Campo | Valor |
|---|---|
| Nombre del webinar | **30X AI Sales: Cómo Clonar a tu Mejor Vendedor con AI** |
| Curso que se vende | **30X AI Sales** (Growth Rockstar / 30X) |
| URL oficial del programa | https://30x.com/programas/ai-sales |
| Fecha del webinar | _[COMPLETAR]_ |
| Hora | _[COMPLETAR]_ |
| Link Luma | _[COMPLETAR]_ |
| Link Zoom / Meet | _[COMPLETAR]_ |
| Link Calendly del equipo | _[COMPLETAR]_ |
| Link inscripción al curso | https://30x.com/programas/ai-sales |
| Repo GitHub destino | `Webinar-AI-Sales` (o el nombre que defina el usuario) |
| URL del dashboard (Vercel) | _[se completa después del deploy]_ |
| URL del endpoint proxy | `https://[dashboard-vercel].vercel.app/api/claude` |

---

## 2. Contexto completo del curso 30X AI Sales

> **IMPORTANTE para Claude:** Esta es la única fuente de verdad sobre el curso. **NO inventes nada que no esté acá.** Si el usuario te da info adicional en chat, usala. El PDF oficial `AI_Sales_Deck.pdf` está en la raíz del proyecto si querés consultarlo directamente.

### Pitch del programa
Domina la inteligencia artificial aplicada a ventas. Creado para líderes comerciales **no técnicos**, enfocado a la práctica para que multipliques tu ingreso aplicando desde ya.
**20x productividad — 4 semanas.**

### Para quién es
Líderes y profesionales de ventas B2B:
- Heads of sales
- Directores comerciales
- Founders que venden
- Account executives
- SDR / BDR leads
- Revenue leaders
- Empresas con o sin adopción actual de IA

### Qué resuelve (el dolor)
"Cuántas oportunidades pierdes hoy porque tu equipo de ventas no está aprovechando IA para prospectar, priorizar y cerrar."

Mientras muchos líderes comerciales todavía "experimentan" con IA, otros ya multiplicaron su pipeline, aceleraron el ciclo de venta y construyeron ventajas competitivas difíciles de copiar. El problema no es falta de información sobre IA — es falta de claridad y de formación práctica para usarla en la operativa diaria, integrarla al proceso comercial y medir su impacto en revenue.

### 6 beneficios principales
1. **Productividad desde semana 1** — Usás IA para automatizar prospección, research de cuentas y preparación de reuniones reales de tu pipeline.
2. **Implementación inmediata en tu proceso comercial** — Cada semana aplicás lo aprendido sobre leads, cuentas y oportunidades reales de tu organización.
3. **Más y mejores oportunidades calificadas** — Diseñás flujos de outbound y nutrición asistidos por IA que generan conversaciones de mayor calidad.
4. **Conocimiento curado y aplicado** — Accedés a lo último en ventas con AI, filtrado por experiencia en operación comercial real.
5. **Forecasting y priorización con criterio de negocio** — Construís vistas de pipeline asistidas por IA para priorizar deals, enfocar esfuerzos y prever riesgos.
6. **Mejor tasa de conversión y win-rate** — IA para mejorar discovery, propuestas, follow-ups y manejo de objeciones con mensajes específicos por segmento.

### Mentores
- **Nicolás Rojas** — CEO de Dapta & Forbes 30 Under 30. Fundador técnico que escaló empresas a +100 empleados y levantó $7,4M en capital. Construye Dapta, infraestructura de IA para miles de empresas.
- **Andrés Bilbao** — Co-founder de Rappi (primer unicornio de la región, +USD 2.000M levantados, valuación +USD 5.000M) & 30X Co-Founder. Lidera Next y Achievers en la frontera de la IA.

### Los 8 módulos
1. **AI Mindset & el Stack del Top Performer** — Pensar antes de automatizar. IA como amplificador humano en cada etapa.
2. **Social Selling & Autoridad de Marca** — Sistemas de contenido que convierten confianza en oportunidades reales.
3. **Outbound: Inteligencia de Cuentas & Data Enrichment** — Research, señales de compra y dossiers automáticos antes del primer contacto.
4. **Outbound: Automatización e Hiper-Personalización a Escala** — Escalar outreach sin perder relevancia. Orquestación multicanal.
5. **Inbound: Conversational AI & Speed-to-Lead** — Agentes de voz y chat que califican, enrutan y convierten sin fricción.
6. **Inbound: Discovery & Follow-Up** — IA que escucha, analiza, sugiere y automatiza los siguientes pasos en cada llamada.
7. **AI Sales Performance: Sales Coaching & Conversational Intelligence** — Convertir cada llamada en data accionable para entrenar equipos y replicar patrones de top performers.
8. **AI Sales Performance: RevOps, Forecasting & Agentes Autónomos** — Forecasting predictivo, CRM autónomo y SDRs basados en IA.

### Metodología
- Ejecución práctica, no teoría. Desde semana 1 trabajás sobre TU pipeline real (tus leads, cuentas, oportunidades).
- Conocimiento curado por operación comercial real.
- 100% online. Sesiones virtuales en vivo + clases grabadas.
- Templates y workflows listos para copiar/pegar (n8n, prompts, configs).

### Lo que hace único al programa
- **Altamente práctico:** multiplicás tu ingreso aplicando el futuro de las ventas desde ya.
- **Foco en ventas:** prospección, conversión y revenue. No herramientas por las herramientas.
- **Para líderes no técnicos:** aplicás IA en tu pipeline sin técnico ni desarrollos costosos.
- **Sobre tu pipeline real:** lo que ves lo usás de inmediato.

### Datos duros (inversión y condiciones)
| Concepto | Valor |
|---|---|
| Precio | **USD 1.950** |
| Reserva de cupo (early bird) | USD 199 |
| Formas de pago | Tarjeta de crédito o transferencia bancaria. Opciones adicionales: consultar con el equipo. |
| Duración | 4 semanas |
| Sesiones en vivo | 8 sesiones (quedan grabadas) |
| Cupos | Limitado a 100 |
| Modalidad | 100% online |
| Acceso a grabaciones | 1 año |
| Extras incluidos | +100K créditos gratis de Dapta · Certificado oficial de 30X Executive Education · Acceso a comunidad AI Sales (SDRs, AEs, líderes comerciales) · Templates y workflows listos |

⚠️ Las fechas exactas (16 de abril – 11 de mayo en el deck original) **pueden no aplicar al webinar actual**. Si el usuario no aclaró fechas vigentes, usá lenguaje genérico ("la próxima cohorte arranca pronto") y dejá `[FECHA]` entre corchetes para confirmar.

### Tono y posicionamiento (importante para los copys)
- Directo, conversacional, sin marketingese.
- "Multiplicá tu ingreso" y "20x productividad" son métricas que sí podés usar (vienen del deck).
- No prometer cierres mágicos. Sí prometer ejecución desde semana 1 sobre el pipeline real del lead.
- Sin emojis exagerados. Estilo Dylan Pereira / Growth Rockstar.

---

## 3. CSV de registros

El CSV de Luma está en la raíz como `registros-luma.csv` (~10.000 registros del webinar AI Sales).

**Estructura real de las columnas relevantes** (importante: son distintas a las del webinar Xtreme Growth — adaptarse a esta estructura):

| Columna en CSV | Uso |
|---|---|
| `name` | Nombre completo |
| `email` | Correo |
| `phone_number` | WhatsApp (formato internacional, ej. +573...) |
| `has_joined_event` | "Yes" / "No" — asistencia (se llena DESPUÉS del webinar) |
| `utm_source` | Canal de origen (útil para análisis) |
| `En qué empresa trabajas?` | Empresa |
| `Cuál es tu rol?` | Rol / cargo |
| `Qué preguntas tienes acerca del programa de 30X "AI Sales" (Ventas con IA)?` | **LA PREGUNTA CLAVE — materia prima de todo el flujo** |

⚠️ La columna de la pregunta tiene comillas escapadas en el header (`""AI Sales""`). Al procesar el CSV con pandas o JavaScript, leerla con cuidado de parser de comillas.

---

## 4. Flujo completo a ejecutar

### FASE 1 — Análisis y limpieza del CSV (PROMPT 1)

Cuando el usuario suba el CSV (`registros-luma.csv`) y pida "limpiar", hacer:

- Leer el CSV completo.
- Para cada persona extraer: nombre, correo, teléfono, empresa, rol, pregunta del formulario, utm_source, has_joined_event.
- Normalizar nombres a Title Case (María, no MARIA ni maría).
- Uniformar nombres de empresa (si "Globant" aparece como "GLOBANT", "globant.", etc. → unificar).
- Si la pregunta está vacía o es genérica ("ninguna", "no sé", "nada", solo espacios, "x", "-") → marcar `pregunta_formulario = [VACIO]`.
- Incluir a TODAS las personas registradas, sin excluir a nadie.
- Devolver tabla limpia en CSV: `nombre, correo, telefono, empresa, rol, pregunta_formulario, utm_source, asistio`.

### FASE 2 — Segmentación por intención de compra (PROMPT 2)

Sobre la tabla limpia, agregar columna `nivel_intencion` con uno de estos 4 valores. Usar el vocabulario REAL del programa para detectar señales:

- **HOT** — Preguntó por:
  - Precio, descuentos, financiamiento, cupones, cupo, reserva.
  - Fechas de inicio de la próxima cohorte, fechas de las sesiones.
  - Certificado, validez, ROI esperado.
  - Empresas, tarifas corporativas, factura.
  - O expresó intención clara: "quiero inscribirme", "cómo aplico", "guardame un cupo".

- **WARM** — Hizo preguntas técnicas profundas o de fit:
  - Sobre módulos específicos (outbound, inbound, conversational AI, forecasting, RevOps, agentes autónomos).
  - Herramientas mencionadas en el programa: **Dapta, n8n, HubSpot, Salesforce, Pipedrive, GPTs, agentes de voz, conversational intelligence, sales coaching**.
  - Comparó con otros cursos / programas de IA.
  - Preguntó por casos aplicados a SU industria o tipo de empresa.
  - Dudas de fit: "soy SDR / AE / founder / director comercial, ¿me sirve?".
  - Preguntó por la comunidad, templates, workflows incluidos.

- **COLD** — Hizo preguntas generales:
  - "¿De qué se trata?", "¿qué voy a aprender?".
  - "No sé nada de AI / no soy técnico, ¿puedo?".
  - "Cuánto tiempo le tengo que dedicar por semana".
  - "Si me lo pierdo, ¿queda grabado?".
  - Curiosidad sin urgencia, sin señales de compra.

- **NEUTRAL** — Pregunta `[VACIO]` o muy genérica ("nada", "ninguna", "x").

Además devolver un párrafo corto con patrones detectados: qué le interesa a los HOT, qué objeciones tienen los WARM, qué dudas frecuentes tienen los COLD, % aproximado por categoría.

### FASE 3 — Respuesta personalizada por persona (PROMPT 3)

Para cada lead, escribir una respuesta personalizada que:

1. Vaya al grano, sin saludos largos.
2. Responda la **pregunta específica** que esa persona hizo, usando datos REALES del curso (precio USD 1.950, 4 semanas, 8 módulos en vivo, +100K créditos Dapta, mentores Nicolás Rojas y Andrés Bilbao, 100 cupos, certificado oficial 30X).
3. Conecte con un **módulo concreto** del programa según la pregunta (ver mapeo abajo).
4. Termine con CTA suave: agendar llamada (link Calendly) / aplicar al curso / responder este mensaje.
5. **NO usar emojis, NO lenguaje marketinero genérico, NO inventar datos del curso.** Si falta info muy puntual (fecha exacta de la próxima cohorte), dejarla entre `[CORCHETES]`.
6. Máximo 150 palabras.
7. Tono Dylan Pereira / Growth Rockstar: directo, conversacional, sin promesas vacías.

**Mapeo pregunta → módulo a referenciar (guía para Claude):**
- Pregunta sobre prospección / outbound / leads / cold outreach → Módulos 3 y 4.
- Pregunta sobre cómo atender más leads / chatbots / WhatsApp / voz → Módulo 5.
- Pregunta sobre discovery / llamadas / follow-up → Módulo 6.
- Pregunta sobre cómo entrenar al equipo / coaching → Módulo 7.
- Pregunta sobre forecasting / CRM / RevOps / agentes autónomos → Módulo 8.
- Pregunta sobre contenido / LinkedIn / autoridad / inbound orgánico → Módulo 2.
- Pregunta general "cómo empiezo con IA" / fit / "soy no técnico" → Módulo 1.
- Pregunta sobre herramientas específicas (n8n, Dapta, GPTs) → Mencionar templates incluidos y +100K créditos Dapta.
- Pregunta sobre precio / pago / fechas / cupos → Datos duros + reserva USD 199 + CTA agendar llamada.

Si la pregunta es `[VACIO]`, generar un mensaje breve y genérico: "Vi que te registraste al webinar de AI Sales. ¿Qué te gustaría resolver con AI en tu proceso comercial? Cuanto más específico, más concreta te puedo armar la propuesta."

Devolver CSV con todas las columnas anteriores + `respuesta_personalizada`.

⚠️ Si la lista es muy larga (más de 50 registros) y la respuesta se corta, continuar desde donde quedó cuando el usuario lo pida, sin repetir los anteriores.

### FASE 4 — Construir el dashboard interactivo

**Generar `index.html`** (single-file, sin dependencias externas salvo CDN) con estas características:

**Estructura:**
- Header con título "**30X AI Sales — Dashboard de Leads**", fecha del webinar, y 4 contadores grandes: Total leads, HOT, WARM, COLD.
- Subtítulo: "Cómo Clonar a tu Mejor Vendedor con AI".
- Grilla de cards: 3 columnas en desktop, 1 en mobile.
- Filtros arriba: por nivel de intención, búsqueda por nombre/empresa, filtro por asistencia (cuando aplique).

**Cada card muestra:**
- Nombre + empresa + rol.
- Badge de colores según nivel: HOT=rojo, WARM=naranja, COLD=azul, NEUTRAL=gris.
- Pregunta del formulario (truncada a 100 caracteres con "ver más").
- Botón "VER DETALLE" que abre modal.

**Dentro del modal:**
- Toda la info del lead.
- Pregunta completa.
- Respuesta personalizada en un cuadro con borde.
- Botón "COPIAR MENSAJE" (copia al portapapeles).
- Botón **"GENERAR PROPUESTA"** (llama al proxy de Claude — en FASE 5 se conecta).
- Botón **"Abrir en Gmail"** → `mailto:` con asunto y cuerpo pre-cargados.
- Botón **"Abrir en WhatsApp"** → `https://wa.me/[telefono]?text=[mensaje]` con mensaje pre-cargado.
- Textarea "notas internas" que persiste en `localStorage`.

**Diseño:**
- Minimalista, fondo oscuro (`#0a0a0a`), texto blanco, acentos verde lima (`#c7f352` — el mismo que usa el deck de AI Sales).
- Tipografía moderna sans-serif (system font stack o Inter desde Google Fonts).
- Responsive mobile-first.
- Animaciones suaves al abrir modales (fade + scale).

**Datos:**
- Embebé los datos del CSV directamente en el HTML como `const LEADS = [...]` (array JS).
- Encoding correcto para tildes y acentos.
- NO usar `fetch` externo de datos.

**Configuración:**
- Variable `const PROXY_URL = "https://[completar].vercel.app/api/claude"` al inicio del archivo, fácil de editar.

**Entregable:** un solo archivo `index.html` listo para abrir en cualquier navegador.

### FASE 5 — Proxy serverless en Vercel

Generar tres archivos en la carpeta `api/`:

- `api/claude.js` → endpoint serverless en Vercel.
- `package.json` → dependencias mínimas.
- Actualizar el `README.md` con instrucciones de deploy (basado en el del repo de referencia).

**Requisitos del proxy (`api/claude.js`):**

- Endpoint en `/api/claude` que reciba `POST` con JSON `{prompt: "..."}` y devuelva la respuesta de Claude.
- La API key se lee de variable de entorno `ANTHROPIC_API_KEY` (NUNCA hardcodeada).
- Modelo: `claude-sonnet-4-20250514` (o el más reciente). `max_tokens: 1500`.
- CORS abierto (`Access-Control-Allow-Origin: *`).
- Manejo de errores claro: si falta API key, devolver 500 con mensaje. Si Anthropic devuelve error, propagar el mensaje.
- Solo aceptar POST. Para GET/otros, devolver 405 "Method not allowed".
- Sin TypeScript, JavaScript puro. Mínimas dependencias (`@anthropic-ai/sdk` es suficiente).

**Conexión del botón GENERAR PROPUESTA:**

El botón en el modal envía al proxy un prompt como:

```
Sos parte del equipo de Growth Rockstar / 30X. Escribime una propuesta personalizada para este lead que se registró al webinar "30X AI Sales: Cómo Clonar a tu Mejor Vendedor con AI".

Datos del lead:
- Nombre: [nombre]
- Empresa: [empresa]
- Rol: [rol]
- Pregunta original: [pregunta_formulario]

Contexto del programa (úsalo como verdad, no inventes datos):
- 30X AI Sales: 4 semanas, 8 módulos en vivo, 100% online.
- Para líderes comerciales no técnicos: heads of sales, directores comerciales, founders que venden, AEs, SDR/BDR leads.
- Mentores: Nicolás Rojas (CEO Dapta, Forbes 30u30) y Andrés Bilbao (co-founder Rappi).
- Cubre: AI Mindset, Social Selling, Outbound con data enrichment e hiper-personalización, Inbound con conversational AI, Discovery & Follow-up, Sales Coaching con conversational intelligence, RevOps & forecasting con agentes autónomos.
- Stack mencionado: n8n, Dapta, GPTs, agentes de voz, integraciones con CRM.
- Precio USD 1.950. Reserva de cupo USD 199. Cupos limitados a 100. Certificado oficial 30X Executive Education. +100K créditos Dapta gratis. 1 año de acceso a grabaciones.
- URL del programa: https://30x.com/programas/ai-sales

La propuesta debe:
1. Saludo personal por nombre.
2. Referencia específica a su pregunta o contexto de su rol/empresa.
3. Conectar con el módulo concreto del programa que resuelve eso.
4. Mencionar el formato (4 semanas, sobre su pipeline real) cuando aplique.
5. Call to action: agendar llamada o reservar cupo (USD 199).

Máximo 200 palabras. Tono cercano, directo, sin marketingese, sin emojis, sin promesas vacías.
```

Mientras espera respuesta: mostrar spinner o texto "Generando…".
Cuando llega: mostrar en cuadro nuevo dentro del modal con botón "COPIAR".
Si falla: mensaje de error claro + fallback "usá la respuesta pre-generada arriba".

### FASE 6 — Actualización post-webinar

Cuando el usuario suba el CSV post-webinar (con `has_joined_event` lleno), actualizar el dashboard:

- Agregar badge "ASISTIÓ" (verde) o "NO ASISTIÓ" (gris) a cada card.
- Agregar filtro "Asistencia": Todos / Solo asistieron / Solo NO asistieron.
- Reordenar por defecto: primero HOT que asistieron, luego WARM que asistieron, luego HOT que no asistieron, etc.
- Mantener todo lo demás igual.

### FASE 7 — Copys de mailing masivo segmentado (PROMPT 8)

Generar 4 copys para mandar la grabación + CTA al curso, segmentados por:

1. **Heads of Sales / Directores comerciales / Revenue leaders** — foco en pipeline, forecasting, win-rate, RevOps. Mencionar módulos 7 y 8.
2. **Founders que venden / CEOs B2B** — foco en multiplicar productividad sin contratar más vendedores. Mencionar 20x productividad, cómo construir la máquina autónoma.
3. **Account Executives / SDR / BDR leads** — foco en outbound hiper-personalizado, conversational AI, speed-to-lead, discovery con IA. Mencionar módulos 3, 4, 5, 6.
4. **Recuperación** — gente que no asistió al webinar pero está en la base. Subject que apele al FOMO sano, link a la grabación + CTA al curso.

Cada copy: Subject + cuerpo (máx 200 palabras) + descripción del grupo destinatario. Tono Dylan Pereira / Growth Rockstar: directo, conversacional, sin emojis exagerados, sin promesas vacías. Mencionar siempre el dato concreto: 4 semanas, USD 1.950, 100 cupos, mentores Rojas + Bilbao.

---

## 5. Reglas de oro para Claude

- **Empezar siempre por leer `registros-luma.csv`** antes de generar nada.
- **Usar SIEMPRE los datos reales del curso de la sección 2** (precio, módulos, mentores, etc.). NO inventes nada que no esté ahí. Si dudás de algo puntual (fecha exacta de la próxima cohorte), poné `[CORCHETES]` y avisá al usuario.
- **Nunca poner la API key en el HTML ni en el CSV ni en el repo.** Siempre como variable de entorno en Vercel.
- **Mantener tono Dylan Pereira / Growth Rockstar**: directo, sin marketingese, sin emojis exagerados, sin promesas vacías. "20x productividad" sí podés usar, "vas a cerrar el doble en 7 días" no.
- **Iterar es esperado**: el dashboard suele tomar 5-15 rondas de ajuste. No intentar hacerlo perfecto en la primera pasada — generar una versión funcional rápido y mejorar.
- **Para el HTML usar artifact** si estás en claude.ai (el usuario puede ver el preview y descargarlo).
- Si Claude se queda corto procesando muchos leads, dividir en tandas de 50 y avisar al usuario.

---

## 6. Checklist de entregables finales

Al final del flujo, el usuario debe tener:

- [ ] `registros-limpios.csv` (post Prompt 1)
- [ ] `registros-segmentados.csv` (post Prompt 2)
- [ ] `registros-master.csv` con respuestas personalizadas (post Prompt 3)
- [ ] `index.html` del dashboard funcionando localmente
- [ ] `api/claude.js` y `package.json` para el proxy
- [ ] Repo público en GitHub con todo lo anterior
- [ ] Dashboard deployado en Vercel con la URL funcionando
- [ ] Variable de entorno `ANTHROPIC_API_KEY` cargada en Vercel
- [ ] Botón GENERAR PROPUESTA probado 3-4 veces con leads distintos
- [ ] 4 copys de mailing masivo segmentado
