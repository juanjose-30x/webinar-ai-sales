# PASOS PARA TI — Despliegue en 15 minutos

> Ya está TODO armado. Solo tenés que subir esto a GitHub y conectarlo a Vercel.

## 1. Probá el dashboard localmente (1 min)

Doble click en `index.html` → se abre en tu navegador. Deberías ver:
- 1.347 leads totales
- 67 HOT, 120 WARM, 250 COLD
- Cards con filtros, búsqueda, modal funcional

El botón "Generar propuesta nueva en vivo" va a fallar porque el `PROXY_URL` apunta a placeholder. Es esperable — se arregla en el paso 4.

## 2. Subí el proyecto a GitHub (5 min)

**Opción A — Desde la web (más simple):**

1. Andá a https://github.com/new
2. Repository name: `Webinar-AI-Sales`
3. **Tildá "Public"**
4. **NO tildes** "Add a README" (ya tenemos uno)
5. Create repository
6. En la página del repo: click "uploading an existing file"
7. Arrastrá TODOS los archivos de esta carpeta (menos `.env` si existe — el `.gitignore` ya lo protege)
8. Abajo "Commit changes" → click

**Opción B — Desde Cursor (también sirve):**

Abrí Cursor en esta carpeta → panel "Source Control" a la izquierda (icono de la rama) → "Initialize Repository" → escribí mensaje "Setup inicial" → "Commit" → "Publish Branch" → te pide login a GitHub → seleccioná "Public".

## 3. Conseguí tu API key de Anthropic (2 min)

1. Andá a https://console.anthropic.com/settings/keys
2. Si no tenés cuenta de API (distinta de claude.ai), creala con el mismo correo
3. Cargale saldo: Billing → Add credits → USD 5-10 alcanza para todo
4. Create Key → copiá la key (empieza con `sk-ant-api...`)
5. Guardala momentáneamente en un Notes — la usás en el paso 4

## 4. Deploy en Vercel (3 min)

1. https://vercel.com → Sign in with GitHub
2. "Add New..." → "Project"
3. En la lista de repos: encontrá `Webinar-AI-Sales` → "Import"
4. **IMPORTANTE — Antes de Deploy:**
   - Expandí "Environment Variables"
   - Name: `ANTHROPIC_API_KEY`
   - Value: pegá la key que copiaste en el paso 3
   - Click "Add"
5. Click "Deploy"
6. Esperá 1-2 minutos. Vercel te tira URL tipo `https://webinar-ai-sales-xxx.vercel.app`
7. Copiá esa URL.

## 5. Conectá el botón al proxy (3 min)

1. En GitHub, abrí `index.html` directo en la web
2. Click ícono lápiz (Edit)
3. Buscá (Ctrl+F) esta línea cerca del top del `<script>`:
   ```js
   const PROXY_URL = "https://TU-PROYECTO.vercel.app/api/claude";
   ```
4. Reemplazá `TU-PROYECTO` por el subdominio que te dio Vercel. Ejemplo:
   ```js
   const PROXY_URL = "https://webinar-ai-sales-xxx.vercel.app/api/claude";
   ```
5. Mientras estás ahí, reemplazá también:
   ```js
   const CALENDLY_URL = "https://calendly.com/TU-LINK";
   ```
   por el link real de Calendly del equipo.
6. Scroll abajo → "Commit changes"
7. Vercel detecta el cambio y redeploya solo en 1-2 minutos

## 6. Probá

1. Abrí tu URL de Vercel
2. Click en cualquier card → "Generar propuesta nueva en vivo"
3. Esperá 5-8 segundos
4. Debería aparecer una propuesta personalizada nueva

**Si falla:** abrí la consola del navegador (F12 → Console). Si dice CORS o 500, verificá en Vercel → Settings → Environment Variables que `ANTHROPIC_API_KEY` esté cargada. Después: Deployments → último → 3 puntos → Redeploy.

---

## El día del webinar

1. **10 min antes:** abrí el dashboard, probá GENERAR PROPUESTA 3-4 veces con leads distintos. Confirmá que responde rápido.
2. Tené el dashboard en un **tab separado de tus slides**, listo para mostrar con un click.
3. Identificá ANTES quién es el lead ejemplo que vas a mostrar — alguien presente.
4. **En vivo:**
   - Compartís pantalla
   - Mostrás los contadores: "Tenemos 1.347 personas registradas, 67 con intención alta de compra..."
   - Buscás al lead ejemplo
   - Click VER DETALLE → mostrás pregunta + respuesta pre-generada
   - "Ahora les muestro algo mejor"
   - Click GENERAR PROPUESTA → esperás los 5-8 segundos en silencio
   - Leés en voz alta
5. **Cerrás:** "Esto que acaban de ver es exactamente lo que enseña 30X AI Sales."

## Plan B si el botón falla en vivo

**El modal ya tiene la respuesta pre-generada arriba. Leés esa.** Nadie se entera.

## Después del webinar

El equipo entra al dashboard:
- Filtran HOT que asistieron → click cada card → "Abrir en WhatsApp" → mensaje pre-cargado
- Filtran WARM → "Abrir en Gmail" → mensaje pre-cargado en el cuerpo
- Notas internas se guardan en localStorage del navegador

---

## Si algo se rompe

- **"El botón no hace nada":** F12 → Console del navegador. Si dice 404 → la `PROXY_URL` está mal escrita. Si dice CORS → el proxy no está deployado bien. Si dice 500 → falta la API key en Vercel.
- **"Vercel redeployó pero veo la versión vieja":** Cmd+Shift+R (Mac) o Ctrl+F5 (Windows) en el navegador.
- **"No tengo saldo de Anthropic":** Billing en console.anthropic.com → recargá $5 USD → en 30 segundos vuelve a funcionar.
