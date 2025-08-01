from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    user_message = form.get("Body")

    if not user_message:
        return PlainTextResponse("No message received", status_code=400)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "És um professor simpático de inglês. Explica com clareza."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception as e:
        return PlainTextResponse(f"OpenAI Error: {str(e)}", status_code=500)

    twilio_response = MessagingResponse()
    twilio_response.message(bot_reply)
    return PlainTextResponse(str(twilio_response), media_type="application/xml")



