# 30X AI Sales — Dashboard de Leads

Dashboard interactivo del webinar **30X AI Sales: Cómo Clonar a tu Mejor Vendedor con AI**.

- 1.347 leads procesados y segmentados (HOT / WARM / COLD / NEUTRAL)
- Respuesta personalizada pre-generada para cada uno
- Botón "Generar propuesta en vivo" que llama a Claude vía proxy
- Botones de Gmail y WhatsApp con mensaje pre-cargado por lead

## Estructura

```
.
├── index.html         # Dashboard (todo embebido, datos incluidos)
├── api/claude.js      # Proxy serverless de Vercel (esconde la API key)
├── package.json       # Mínimo, para que Vercel detecte el proyecto Node
├── CLAUDE.md          # Instrucción maestra (referencia)
├── registros-master.csv  # Dataset procesado (no se sube — está en .gitignore si lo agregás)
└── COMO-USAR.md       # Guía de uso del proyecto
```

## Deploy en Vercel — 3 pasos

### 1. Subí esto a un repo de GitHub

Creá un repo nuevo público llamado `Webinar-AI-Sales` y subí estos archivos.

### 2. Conectá el repo a Vercel

1. https://vercel.com → "Add New..." → "Project"
2. Seleccioná el repo `Webinar-AI-Sales` → Import
3. **Antes** de hacer click en Deploy, expandí "Environment Variables" y agregá:
   - Name: `ANTHROPIC_API_KEY`
   - Value: tu API key real (la copiás desde https://console.anthropic.com/settings/keys)
4. Click Deploy. Esperá 1-2 min.
5. Vercel te da una URL tipo `https://webinar-ai-sales-xxx.vercel.app`

### 3. Actualizá el PROXY_URL en index.html

Abrí `index.html`, buscá esta línea al inicio del `<script>`:

```js
const PROXY_URL = "https://TU-PROYECTO.vercel.app/api/claude";
```

Reemplazá `TU-PROYECTO` por la URL real que te dio Vercel. Commit + push. Vercel redeploya solo en 1-2 min.

También reemplazá:
- `CALENDLY_URL` por el link real de Calendly del equipo
- `CURSO_URL` ya está apuntando a https://30x.com/programas/ai-sales

### 4. Probar

Abrí la URL de Vercel → click en cualquier card → "Generar propuesta nueva en vivo".
Debería tardar 3-8 segundos y devolverte una propuesta personalizada en vivo.

## Cómo se usa durante el webinar

1. Abrí el dashboard 10 min antes del evento. Probá GENERAR PROPUESTA 3-4 veces con leads distintos.
2. Tené el dashboard en un tab separado de tus slides, listo para mostrar con un click.
3. Identificá ANTES quién es "el lead ejemplo" que vas a mostrar — idealmente alguien presente en el webinar.
4. En vivo: mostrás contadores → buscás al lead ejemplo → click VER DETALLE → mostrás su pregunta + respuesta pre-generada → "ahora les muestro algo mejor" → GENERAR PROPUESTA → esperás los 5-8 segundos en silencio → leés en voz alta.
5. Cerrás con: "Esto que acaban de ver es exactamente lo que enseña AI Sales."

## Cómo se usa después del webinar

El equipo comercial entra al dashboard y trabaja en paralelo:
- Filtran por HOT que asistieron → click VER DETALLE → "Abrir en WhatsApp" → mensaje pre-cargado.
- Filtran por WARM que NO asistieron → "Abrir en Gmail" → mensaje pre-cargado con respuesta personalizada en el cuerpo.
- Notas internas se guardan automáticamente en localStorage de cada navegador.

## Plan B si el botón GENERAR PROPUESTA falla en vivo

El modal ya tiene la **respuesta personalizada pre-generada arriba**. Leés esa, no se nota nada.

## Costo

Cada llamada al botón usa ~1500 tokens. Con Claude Sonnet 4.5:
- Costo por llamada: ~$0.01-0.02 USD
- 100 llamadas durante el webinar: ~$1-2 USD total

Vercel free tier alcanza perfectamente.
