# Cómo usar este proyecto — Guía rápida

Esta carpeta tiene todo lo que necesitás para armar el dashboard del **Webinar 30X AI Sales** replicando el flujo del Webinar Xtreme Growth.

## Qué hay acá

```
Webinar-AI-Sales/
├── CLAUDE.md              ← la instrucción maestra (NO la edites, es la receta)
├── registros-luma.csv     ← tu CSV de Luma ya copiado (~10.000 registros)
├── AI_Sales_Deck.pdf      ← brochure oficial del programa (referencia para Claude)
├── COMO-USAR.md           ← este archivo
├── README.md              ← README del repo
└── api/                   ← acá va a quedar el proxy serverless (vacío por ahora)
```

## Lo que ya está hecho

✅ Carpeta creada
✅ CSV de Luma copiado y renombrado a `registros-luma.csv` (~10.000 registros)
✅ Brochure oficial `AI_Sales_Deck.pdf` incluido como referencia
✅ `CLAUDE.md` adaptado al webinar AI Sales con:
   - Estructura exacta de las columnas de tu CSV
   - **Toda la info del programa embebida** (precio USD 1.950, 8 módulos, 4 semanas, mentores Rojas + Bilbao, stack n8n/Dapta/GPTs, +100K créditos Dapta, certificado 30X)
   - Mapeo pregunta del lead → módulo a referenciar en la respuesta
   - Vocabulario real del programa para detectar señales HOT/WARM/COLD
✅ Las 7 fases del flujo definidas con prompts listos

## Cómo usar el `CLAUDE.md` — 3 opciones

### Opción A — Con Claude Code (recomendado, más fluido)

1. Instalá Claude Code si no lo tenés: https://docs.claude.com/en/docs/claude-code/overview
2. Abrí la terminal en esta carpeta:
   ```bash
   cd ~/ruta/a/Webinar-AI-Sales
   claude
   ```
3. Claude detecta automáticamente el `CLAUDE.md` y lo carga como contexto del proyecto. Le decís:
   > "Empecemos con la FASE 1: limpiá el CSV"

   Y va ejecutando fase por fase.

### Opción B — Con claude.ai (chat web normal, también funciona perfecto)

1. Andá a https://claude.ai → "New chat" → asegurate de tener modelo Opus o Sonnet (el más nuevo).
2. **Primer mensaje:** arrastrá los dos archivos al chat:
   - `CLAUDE.md`
   - `registros-luma.csv`
3. Escribí algo así:
   > "Acá te paso el `CLAUDE.md` con la instrucción completa del proyecto y el `registros-luma.csv`. Seguí el flujo del CLAUDE.md fase por fase. Empezá por FASE 1 — Análisis y limpieza del CSV (PROMPT 1)."
4. Claude ejecuta FASE 1 → te devuelve el CSV limpio.
5. Decís: "Ahora FASE 2." → segmentación.
6. Decís: "Ahora FASE 3." → respuestas personalizadas.
7. **Para FASE 4 (dashboard) abrí un chat NUEVO** (importante, el contexto pesa) y subí el `CLAUDE.md` + el CSV master final. Pedile FASE 4.
8. Iterá el dashboard 5-15 veces hasta que esté como querés.
9. Otro chat nuevo para FASE 5 (proxy).

### Opción C — Subir a GitHub y trabajar desde ahí

1. Subí esta carpeta como repo nuevo en GitHub (público, igual que el de referencia).
2. Cualquier persona del equipo que abra Claude Code en el repo va a tener el `CLAUDE.md` cargado automáticamente.

## Orden de las fases (referencia rápida)

| Fase | Qué hace | Cuándo |
|---|---|---|
| 1 | Limpia el CSV (nombres, empresas, preguntas vacías) | Días previos al webinar |
| 2 | Segmenta leads en HOT / WARM / COLD / NEUTRAL | Días previos |
| 3 | Genera respuesta personalizada para cada lead | Días previos |
| 4 | Construye el dashboard HTML (chat nuevo) | Días previos |
| 5 | Crea el proxy en Vercel para conectar Claude en vivo | Días previos |
| 6 | Actualiza dashboard con asistencia post-webinar | Día +1 |
| 7 | Genera 4 copys de mailing masivo segmentado | Día +1 a +3 |

## Datos que tenés que completar antes de empezar la FASE 1

Abrí `CLAUDE.md` y completá la tabla de **sección 1 — Datos del webinar**:

- Fecha y hora del webinar
- Link Luma del evento
- Link Zoom / Meet
- Link Calendly del equipo
- Link de inscripción al curso

Si todavía no los tenés, igual podés arrancar — Claude los va a dejar como `[CORCHETES]` y los completás después.

## Atajos por si surge algo

- **El CSV tiene una columna rara** (la pregunta del formulario tiene comillas dobles escapadas: `""AI Sales""`). Ya está documentado en `CLAUDE.md` sección 2 para que Claude lo parsee bien.
- **Si Claude se queda corto procesando 10k leads** en la FASE 3: decile "continuá desde donde te quedaste, no repitas los anteriores". A veces toca dividir en tandas de 50.
- **Para deploy a GitHub + Vercel**: seguí la guía exacta del repo de referencia: https://github.com/cristina-barbosa-sabagh/Webinar-Xtreme-Growth (la sección "Deploy en Vercel — 5 minutos" del README).
- **Si el botón GENERAR PROPUESTA falla en vivo**: el modal ya tiene la respuesta pre-generada arriba. Leés esa y seguís. Plan B siempre listo.

## Lo más importante

El `CLAUDE.md` ya contiene los **prompts exactos** que necesita Claude para cada fase. No tenés que reinventar nada — solo decirle "empezá por FASE 1" y dejar que corra. Si algo no sale como esperás, pedile que itere ("hacelo mostrando primero los HOT", "agregame botón de WhatsApp", etc.).

**Tiempo estimado primera vez:** 7-10 días distribuidos.
**Segunda vez:** 3-4 días.
**Tercera vez:** 1-2 días, ya es protocolo.
