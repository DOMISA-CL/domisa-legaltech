from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "Domisa Online"}

@app.post("/analizar-multas")
async def whatsapp_bot(request: Request):
    try:
        # Leemos los datos de Twilio de forma más compatible
        form_data = await request.form()
        
        # Twilio envía el mensaje en el campo 'Body'
        mensaje = form_data.get("Body", "").strip().upper()
        
        # LOGICA DE RESPUESTA
        if mensaje.isdigit() and len(mensaje) == 4:
            anio = int(mensaje)
            if anio <= 2023:
                respuesta = f"✅ El año {anio} califica para borrado legal en Domisa. ¡Podemos gestionar tu caso!"
            else:
                respuesta = f"⚠️ El año {anio} es muy reciente. La ley exige 3 años de antigüedad para la prescripción."
        
        elif len(mensaje) >= 6:
            respuesta = f"🚗 Recibimos la patente {mensaje}. Ahora dime: ¿De qué año es la multa más antigua? (Ej: 2020)"
        
        else:
            respuesta = "👋 Bienvenido a Domisa LegalTech. Para comenzar, envíame una patente o el año de tu multa."

    except Exception as e:
        # ESTO ES CLAVE: Si vuelve a fallar, verás el porqué en los Logs de Render
        print(f"DEBUG ERROR: {str(e)}")
        respuesta = "Hubo un problema técnico. Por favor, intenta de nuevo en unos minutos."

    # Respuesta TwiML
    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{respuesta}</Message></Response>'
    return Response(content=twiml, media_type="application/xml")
