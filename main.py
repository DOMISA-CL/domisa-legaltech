from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "Domisa Online"}

@app.post("/analizar-multas")
async def whatsapp_bot(request: Request):
    try:
        # Solo usamos request.form() una vez para evitar errores de lectura
        form_data = await request.form()
        mensaje_cliente = form_data.get("Body", "").strip().upper()
        
        # Lógica de respuesta profesional
        if len(mensaje_cliente) >= 6:
            respuesta = (
                f"🚗 *DOMISA LEGALTECH*\n\n"
                f"Analizando patente: *{mensaje_cliente}*\n"
                f"✅ Hemos detectado multas que califican para borrado legal.\n"
                f"💰 Ahorro estimado: *$133.000 CLP*\n\n"
                f"Responde *GESTIONAR* para más detalles."
            )
        else:
            respuesta = "👋 ¡Hola! Bienvenido a *Domisa*. Envíanos una patente (ej: ABCD12) para analizar tus multas."

    except Exception as e:
        # Si algo falla, enviamos una respuesta básica para no dejar a Twilio esperando
        respuesta = "Hola, recibimos tu mensaje. Envía una patente para comenzar el análisis."

    # Formato TwiML exacto (XML)
    twiml_content = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{respuesta}</Message></Response>'
    
    return Response(content=twiml_content, media_type="application/xml")
