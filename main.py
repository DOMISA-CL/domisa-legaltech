from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

app = FastAPI()

# 1. Página de inicio para que no salga "Not Found"
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1 style="color: #1a73e8;">Domisa LegalTech Operativo</h1>
            <p>El servidor de Inteligencia Legal está conectado a Internet.</p>
            <p style="color: green;">✔ Listo para recibir mensajes de WhatsApp</p>
        </body>
    </html>
    """

# 2. El "Cerebro" que responde a WhatsApp
@app.post("/analizar-multas")
async def whatsapp_bot(request: Request):
    try:
        # Twilio envía los datos en este formato
        form_data = await request.form()
        patente = form_data.get("Body", "S/P").upper().strip()
        
        # LÓGICA DE NEGOCIO SIMPLIFICADA:
        # Aquí simulamos que si la patente tiene 6 letras/números, calculamos ahorro.
        if len(patente) >= 6:
            ahorro_fake = 133000 # Esto después se automatiza con tu base de datos
            mensaje_respuesta = (
                f"🚗 *AUDITORÍA DOMISA*\n\n"
                f"Analizamos la patente: *{patente}*\n"
                f"✅ Detectamos multas con más de 3 años.\n"
                f"💰 Ahorro potencial: *$ {ahorro_fake:,} CLP*.\n\n"
                f"¿Deseas que gestionemos la eliminación? Responde *SÍ*."
            )
        else:
            mensaje_respuesta = "¡Hola! Por favor envía una patente válida (ej: ABCD12) para analizar tus multas."

        # Formato TwiML para que WhatsApp lo reciba
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Message>{mensaje_respuesta}</Message>
        </Response>"""
        
        return Response(content=twiml_response, media_type="application/xml")
    
    except Exception as e:
        return Response(content="<Response><Message>Error técnico, reintenta.</Message></Response>", media_type="application/xml")
