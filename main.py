from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "Domisa LegalTech Pro Activo"}

@app.post("/analizar-multas")
async def whatsapp_bot(request: Request):
    try:
        # Capturamos los datos del mensaje
        form_data = await request.form()
        mensaje = form_data.get("Body", "").strip().upper()
        
        # 1. Lógica para el AÑO de la multa (4 dígitos)
        if mensaje.isdigit() and len(mensaje) == 4:
            anio = int(mensaje)
            # En 2026, multas de 2023 o anteriores ya tienen los 3 años
            if anio <= 2023:
                respuesta = (
                    f"✅ *¡ESTÁS DE SUERTE!*\n\n"
                    f"Tu multa del año {anio} ya puede ser **borrada legalmente**. En *Domisa* nos encargamos de todo el trámite por ti para limpiar tu certificado. ⚖️\n\n"
                    "👉 Escribe *GESTIONAR* para que un asesor tome tu caso hoy mismo."
                )
            else:
                respuesta = (
                    f"⚠️ *AVISO LEGAL*\n\n"
                    f"Tu multa es del año {anio}. La ley de prescripción exige al menos **3 años** de antigüedad.\n\n"
                    "Aún es muy reciente para un borrado automático, pero si tienes muchas multas, podemos revisar si hubo errores en la notificación. 🚗"
                )
        
        # 2. Lógica para la PATENTE (6 o más caracteres)
        elif len(mensaje) >= 6:
            respuesta = (
                f"🚗 *PATENTE RECIBIDA: {mensaje}*\n\n"
                "Estamos listos para el análisis. Ahora por favor dime:\n\n"
                "👉 *¿De qué año es la multa más antigua que te aparece?*\n"
                "_(Responde solo el año, por ejemplo: 2020)_"
            )
        
        # 3. Saludo inicial o mensaje por defecto
        else:
            respuesta = (
                "👋 *Bienvenido a Domisa LegalTech*\n\n"
                "Limpiamos tu certificado de multas TAG y vías exclusivas de manera legal y definitiva. 🇨🇱\n\n"
                "Para una **evaluación gratuita**, por favor envíame la *PATENTE* de tu vehículo."
            )

    except Exception as e:
        # En caso de cualquier error, enviamos un mensaje neutro
        print(f"Error: {e}")
        respuesta = "👋 Hola. Para comenzar el análisis de tus multas, por favor envíame la *PATENTE* de tu vehículo."

    # Formato TwiML para que WhatsApp lo interprete correctamente
    twiml_content = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{respuesta}</Message></Response>'
    
    return Response(content=twiml_content, media_type="application/xml")
