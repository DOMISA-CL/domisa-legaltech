from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitimos que servicios externos como Twilio hablen con tu servidor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"status": "Domisa Online"}

@app.post("/analizar-multas")
async def whatsapp_bot(request: Request):
    # Intentamos obtener el mensaje de varias formas para no fallar
    body = await request.body()
    print(f"Datos recibidos: {body}") # Esto podrás verlo en los Logs de Render
    
    try:
        # Extraemos el texto del mensaje
        form_data = await request.form()
        mensaje_cliente = form_data.get("Body", "HOLA").upper()
        
        respuesta = (
            f"🚗 *DOMISA LEGALTECH*\n\n"
            f"Recibimos tu mensaje: *{mensaje_cliente}*\n"
            f"Estamos procesando los datos de tu patente. ⏳"
        )
    except Exception:
        respuesta = "¡Hola! Bienvenido a Domisa. Envíanos una patente para comenzar."

    # Formato TwiML básico
    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{respuesta}</Message></Response>'
    return Response(content=twiml, media_type="application/xml")
