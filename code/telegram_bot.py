import dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from twitch_api import TwitchAPI
import asyncio

api = TwitchAPI("unweonmais")


dotenv.load_dotenv()
API_KEY = os.environ.get("API_KEY")
app = ApplicationBuilder().token(API_KEY).build()

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hola {update.effective_user.first_name}! Todo bien pa?')





async def stream_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hola {update.effective_user.first_name}! Todo bien pa? andamo iniciando el bot')
    pasada = True
    while True:
        if api.is_live():
            if not context.user_data.get('sent_message', False):
                await update.message.reply_text(f"{api.user} está en directo! \n{api.get_url()}")
                context.user_data['sent_message'] = True
            #await asyncio.sleep(5)  # Esperar un minuto antes de volver a verificar
        else:
            context.user_data['sent_message'] = False
            if pasada == True:
                pasada = False
                await update.message.reply_text(f"Ahora mismo el papu \"{api.user}\" no está en directo")
            continue


if __name__ == "__main__":
    app.add_handler(CommandHandler("start", stream_alert))
    app.run_polling()
    