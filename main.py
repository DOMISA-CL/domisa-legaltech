from fastapi import FastAPI, Request, Response
import datetime

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "Domisa Online"}

@app.post("/analizar-multas")
async def whatsapp_bot(request: Request):
    try:
        form_data = await request.form()
        texto = form_data.get("Body", "").strip().upper()
        
        # LÓGICA DE RESPUESTA AUTOMÁTICA
        # 1. Si el usuario envía una patente (Ej: ABCD12 o AB-CD-12)
        if len(texto) >= 6 and any(char.isdigit() for char in texto):
            respuesta = (
                f"🚗 *ANÁLISIS DE PATENTE: {texto}*\n\n"
                "He recibido tu patente con éxito. Para darte un presupuesto real, necesito un dato más:\n\n"
                "👉 *¿De qué año es la multa más antigua?*\n"
                "(Responde solo el número, ejemplo: 2019)"
            )
        
        # 2. Si el usuario envía un año (4 números)
        elif texto.isdigit() and len(texto) == 4:
            anio = int(texto)
            antiguedad = 2026 - anio
            
            if antiguedad >= 3:
                respuesta = (
                    f"✅ *MULTA PRESCRIPTIBLE*\n\n"
                    f"Tu multa de {anio} tiene {antiguedad} años. Por ley, ya podemos solicitar borrarla de tu certificado.\n\n"
                    "Escribe *GESTIONAR* para que un abogado de Domisa tome tu caso hoy mismo. ⚖️"
                )
            else:
                respuesta = (
                    f"⚠️ *MULTA RECIENTE*\n\n"
                    f"Tu multa de {anio} solo tiene {antiguedad} años. Legalmente aún no cumple el plazo de 3 años para borrado automático, pero podemos revisar si tiene errores de notificación. ¿Te interesa?"
                )
        
        # 3. Saludo inicial
        else:
            respuesta = (
                "👋 *Bienvenido a Domisa LegalTech*\n\n"
                "Soy tu asistente legal automático. Para comenzar, por favor *envíame la patente* del vehículo que quieres analizar."
            )

    except Exception as e:
        respuesta = "Lo siento, hubo un error al procesar. Por favor, intenta enviando la patente de nuevo."

    # Formato TwiML para Twilio
    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{respuesta}</Message></Response>'
    return Response(content=twiml, media_type="application/xml")
