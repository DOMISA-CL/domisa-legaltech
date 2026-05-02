from fastapi import FastAPI, Request, Response

app = FastAPI()

# --- ESTA ES LA PARTE QUE EVITA EL "NOT FOUND" ---
@app.get("/")
async def home():
    return {"status": "Domisa LegalTech Online", "mensaje": "El servidor funciona correctamente"}

# --- ESTA ES LA PARTE QUE HABLA CON WHATSAPP ---
@app.post("/analizar-multas")
async def whatsapp_bot(request: Request):
    form_data = await request.form()
    texto = form_data.get("Body", "").strip().upper()
    
    if len(texto) >= 6 and len(texto) <= 7:
        patente = texto
        valor_utm = 66500 
        ahorro_estimado = valor_utm * 2 
        
        mensaje = (
            f"⚖️ *AUDITORÍA LEGAL DOMISA*\n"
            f"----------------------------------\n"
            f"🔍 *Resultado para la patente:* {patente}\n\n"
            f"✅ Hemos detectado multas que califican para *prescripción*.\n\n"
            f"💰 *Ahorro estimado:* ${ahorro_estimado:,} CLP\n\n"
            f"----------------------------------\n"
            f"Responde *GESTIONAR* y un asesor te contactará. 🇨🇱"
        )
    else:
        mensaje = "👋 ¡Hola! Bienvenido a *Domisa LegalTech*. Envíame una patente (ej: ABCD12) para analizar tus multas."

    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{mensaje}</Message></Response>'
    return Response(content=twiml, media_type="application/xml")
