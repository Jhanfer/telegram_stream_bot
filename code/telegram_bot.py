import dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Updater, Application
from twitch_api import TwitchAPI
import asyncio
import http.server
import socketserver
import telegram


api = TwitchAPI("unweonmais")
dotenv.load_dotenv()
API_KEY = os.environ.get("API_KEY")
bot = telegram.Bot(token=API_KEY)


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length)
        update = telegram.Update.de_json(body.decode('utf-8'), bot)

        # Procesar la actualización (ej: responder a un mensaje)
        if update.message:
            chat_id = update.message.chat.id
            message_text = update.message.text
            bot.send_message(chat_id=chat_id, text=f"Has dicho: {message_text}")

        self.send_response(200)
        self.end_headers()






contadores = {
    "contador1":0,
    "contador2":0
}


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
            await context.bot.send_message(chat_id, f'{api.user} está en vivo! \n{data["title"]} \n{data["game_name"]} \n🔴{int(data["viewer_count"]):,}🔴 \nhttps://twitch.tv/{api.user} \n@baltaok @Legna')
            contador1["contador1"] += 1

        elif api.is_live() == False:
            if contador1["contador1"] > 0 or estado_anterior["is_live"] == True:
                contador1["contador1"] = 0
                estado_anterior["is_live"] = False
                await context.bot.send_message(chat_id, f'Ahora mismo {api.user} no está en vivo! \n@baltaok @Legna')



if __name__ == "__main__":
    
    with socketserver.TCPServer(("", 8080), MyHandler) as httpd:
        print("serving at port", 8080)
    
        app = ApplicationBuilder().token(API_KEY).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("hola", hola))


        app.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=True,drop_pending_updates=True)


        httpd.serve_forever()

