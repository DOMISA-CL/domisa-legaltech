from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "Servidor Domisa Funcionando"}

@app.post("/analizar-multas")
async def whatsapp_bot(request: Request):
    try:
        # 1. Obtenemos los datos de Twilio de forma segura
        datos = await request.form()
        # El campo 'Body' es el mensaje que tú escribes en WhatsApp
        mensaje = datos.get("Body", "").strip().upper()
        
        # 2. Lógica simplificada
        # Si el mensaje es un año (ej: 2019)
        if mensaje.isdigit() and len(mensaje) == 4:
            anio = int(mensaje)
            if anio <= 2023:
                respuesta = f"✅ El año {anio} califica para borrado legal en Domisa. ¡Podemos eliminar esa multa!"
            else:
                respuesta = f"⚠️ El año {anio} es muy reciente. La ley exige 3 años de antigüedad."
        
        # Si el mensaje parece una patente (letras y números)
        elif len(mensaje) >= 6:
            respuesta = f"🚗 Patente {mensaje} recibida. Ahora dime: ¿De qué año es la multa? (Ej: 2020)"
        
        # Saludo inicial
        else:
            respuesta = "👋 Bienvenido a Domisa. Para empezar, envíame una patente o un año de multa."

    except Exception as e:
        # Esto nos ayudará a ver el error real en los Logs de Render
        print(f"Error detectado: {e}")
        respuesta = "Error de lectura. Por favor, intenta enviando solo el año (ej: 2020)."

    # 3. Respuesta en formato XML para Twilio
    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{respuesta}</Message></Response>'
    return Response(content=twiml, media_type="application/xml")
