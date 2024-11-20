import dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Updater, Application
from twitch_api import TwitchAPI
import asyncio
from flask import Flask, request
import telegram

contadores = {
    "contador1":0,
    "contador2":0
}
api = TwitchAPI("Rubius")
dotenv.load_dotenv()
API_KEY = os.environ.get("API_KEY")
flask = Flask(__name__)
app = ApplicationBuilder().token(API_KEY).build()
bot = telegram.Bot(API_KEY)

async def hola(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Todo bien, {update.effective_user.first_name} pa? ")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id:
        context.job_queue.run_repeating(stream_alert, interval=5, first=0, chat_id=chat_id)

    if contadores["contador1"] < 1:
        contadores["contador1"] += 1
        await update.message.reply_text(f'Hola {update.effective_user.first_name}! Todo bien pa? andamo iniciando el bot')
    else:
        await update.message.reply_text(f'Ya estoy iniciado.')


contador1 = {
    "contador1":0,
}
estado_anterior = {"is_live": False}

async def stream_alert(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.chat_id 
    if chat_id:
        data = api.get_data()
        if api.is_live() == True and contador1["contador1"] < 1:
            await context.bot.send_message(chat_id, f'{api.user} está en vivo! \n{data["title"]} \n{data["game_name"]} \n🔴{int(data["viewer_count"]):,.2f}🔴 \nhttps://twitch.tv/{api.user}')
            contador1["contador1"] += 1

        elif api.is_live() == False:
            if contador1["contador1"] > 0 or estado_anterior["is_live"] == True:
                contador1["contador1"] = 0
                estado_anterior["is_live"] = False
                await context.bot.send_message(chat_id, f'Ahora mismo {api.user} no está en vivo!')


@flask.route('/' + bot.token, methods=['POST'])
def receive_update():
    # Obtener la actualización de Telegram
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    # Procesar la actualización (ej: responder a un mensaje)
    if update.message:
        chat_id = update.message.chat.id
        message_text = update.message.text
        bot.send_message(chat_id=chat_id, text=f"Has dicho: {message_text}")

    return 'ok'





if __name__ == "__main__":
    

    
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hola", hola))

    flask.run(host='0.0.0.0', port=8080)
    app.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=True,drop_pending_updates=True)



