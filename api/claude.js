// api/claude.js — Proxy serverless en Vercel para conectar el dashboard al API de Anthropic
// La API key se lee de la variable de entorno ANTHROPIC_API_KEY (NUNCA hardcodeada).

export default async function handler(req, res) {
  // CORS abierto (necesario para que el dashboard estático pueda llamar)
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed. Use POST." });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return res.status(500).json({
      error: "Falta variable de entorno ANTHROPIC_API_KEY. Configurala en Vercel → Settings → Environment Variables."
    });
  }

  const { prompt } = req.body || {};
  if (!prompt || typeof prompt !== "string") {
    return res.status(400).json({ error: "Falta el campo 'prompt' en el body." });
  }

  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01"
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1500,
        messages: [{ role: "user", content: prompt }]
      })
    });

    const data = await r.json();

    if (!r.ok) {
      return res.status(r.status).json({
        error: data.error?.message || "Error desconocido de Anthropic",
        details: data
      });
    }

    // Extraer el texto de la respuesta
    const text = data.content?.[0]?.text || "";
    return res.status(200).json({ text, raw: data });
  } catch (err) {
    return res.status(500).json({ error: "Error llamando al API de Anthropic", details: err.message });
  }
}
