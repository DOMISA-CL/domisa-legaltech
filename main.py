from fastapi import FastAPI, Request, Response
import datetime

app = FastAPI()

# Simulamos una pequeña base de datos en memoria para recordar qué patente envió cada usuario
sesiones_usuarios = {}

@app.get("/")
async def home():
    return {"status": "Domisa LegalTech Pro"}

@app.post("/analizar-multas")
async def whatsapp_bot(request: Request):
    form_data = await request.form()
    usuario_id = form_data.get("From") # El número de celular del cliente
    texto = form_data.get("Body", "").strip().upper()
    
    # 1. Si el usuario envía una patente (ej: ABCD12)
    if len(texto) == 6:
        sesiones_usuarios[usuario_id] = texto # Guardamos la patente que está consultando
        respuesta = (
            f"🚗 *Patente detectada:* {texto}\n\n"
            "Para calcular si tus multas se pueden borrar, por favor dime:\n"
            "*¿De qué año es la multa más antigua que tienes?* (Responde solo el año, ej: 2020)"
        )

    # 2. Si el usuario envía un año (4 dígitos)
    elif texto.isdigit() and len(texto) == 4:
        anio_multa = int(texto)
        anio_actual = datetime.datetime.now().year
        antiguedad = anio_actual - anio_multa
        patente_guardada = sesiones_usuarios.get(usuario_id, "tu vehículo")

        if antiguedad >= 3:
            respuesta = (
                f"✅ *¡EXCELENTES NOTICIAS!*\n\n"
                f"La multa del año {anio_multa} para la patente *{patente_guardada}* tiene {antiguedad} años.\n"
                "⚖️ Según la Ley 18.287, esta multa ya *PRESCRIBIÓ*.\n\n"
                "Podemos eliminarla de tu certificado. Responde *GESTIONAR* para hablar con un abogado de Domisa."
            )
        else:
            respuesta = (
                f"⚠️ *AVISO LEGAL*\n\n"
                f"La multa es del año {anio_multa} ({antiguedad} años de antigüedad).\n"
                "La ley exige al menos *3 años* para solicitar el borrado. Aún es muy reciente, pero podemos revisar si tiene errores de forma. ¿Deseas una revisión manual?"
            )
            
    # 3. Respuesta por defecto
    else:
        respuesta = "👋 Bienvenido a *Domisa LegalTech*.\n\nEnvíame la *patente* del vehículo que quieres limpiar de multas."

    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{respuesta}</Message></Response>'
    return Response(content=twiml, media_type="application/xml")
