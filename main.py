from fastapi import FastAPI, Request, Response
import datetime

app = FastAPI()

@app.post("/analizar-multas")
async def whatsapp_bot(request: Request):
    form_data = await request.form()
    # Limpiamos el mensaje (quitamos espacios y pasamos a mayúsculas)
    texto = form_data.get("Body", "").strip().upper()
    
    # 1. Lógica de respuesta: ¿Es una patente? (6 caracteres aprox)
    if len(texto) >= 6 and len(texto) <= 7:
        patente = texto
        # Cálculo simulado: Supongamos 2 multas de TAG de 1 UTM cada una
        valor_utm = 66500 
        ahorro_estimado = valor_utm * 2 
        
        mensaje = (
            f"⚖️ *AUDITORÍA LEGAL DOMISA*\n"
            f"----------------------------------\n"
            f"🔍 *Resultado para la patente:* {patente}\n\n"
            f"✅ Hemos detectado multas que califican para *prescripción* (borrado legal por antigüedad).\n\n"
            f"💰 *Ahorro estimado:* ${ahorro_estimado:,} CLP\n"
            f"⏳ *Estado:* Pendiente de gestión\n\n"
            f"----------------------------------\n"
            f"Si deseas eliminar estas multas de tu certificado, responde con la palabra *GESTIONAR* y un asesor de Domisa te contactará en breve. 🇨🇱"
        )
    # 2. Si el cliente dice gracias o saluda
    elif "HOLA" in texto or "GRACIAS" in texto:
        mensaje = (
            "👋 ¡Hola! Bienvenido a *Domisa LegalTech*.\n\n"
            "Para analizar tus multas de TAG y vías exclusivas, por favor *envíame la patente* de tu vehículo (ej: ABCD12)."
        )
    # 3. Respuesta por defecto
    else:
        mensaje = "Para iniciar el análisis legal, por favor ingresa una patente válida de 6 caracteres. 🚗"

    # Empaquetado para WhatsApp
    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{mensaje}</Message></Response>'
    return Response(content=twiml, media_type="application/xml")
