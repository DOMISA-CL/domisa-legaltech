from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "Servidor Domisa Activo"}

@app.post("/analizar-multas")
async def whatsapp_bot(request: Request):
    try:
        # Intentamos obtener los datos del formulario (Twilio estándar)
        form_data = await request.form()
        mensaje = form_data.get("Body", "").strip().upper()
        
        # Si por alguna razón el formulario llega vacío, intentamos otra lógica
        if not mensaje:
            respuesta = "Recibimos un mensaje vacío. Por favor escribe una patente o un año."
        
        # Lógica de respuesta
        elif mensaje.isdigit() and len(mensaje) == 4:
            anio = int(mensaje)
            if anio <= 2023:
                respuesta = f"✅ El año {anio} califica para borrado legal en Domisa."
            else:
                respuesta = f"⚠️ El año {anio} es muy reciente para la ley de prescripción."
        elif len(mensaje) >= 6:
            respuesta = f"🚗 Patente {mensaje} recibida. ¿De qué año es la multa?"
        else:
            respuesta = "👋 Bienvenido a Domisa. Envía una patente para comenzar."

    except Exception as e:
        # Si todo lo anterior falla, este mensaje nos dirá que falta la librería
        respuesta = "Configurando sistema... por favor reintenta el envío en 1 minuto."
        print(f"Error técnico: {e}")

    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{respuesta}</Message></Response>'
    return Response(content=twiml, media_type="application/xml")
