from fastapi import FastAPI, Request
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

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "És um professor simpático de inglês. Explica com clareza."},
            {"role": "user", "content": user_message}
        ]
    )

    bot_reply = response.choices[0].message.content.strip()

    twilio_response = MessagingResponse()
    twilio_response.message(bot_reply)

    return str(twilio_response)
