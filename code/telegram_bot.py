import dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from twitch_api import TwitchAPI

dotenv.load_dotenv()
API_KEY = os.environ.get("TEST_BOT")
init = {}
estado = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    init[chat_id] = True
    await update.message.reply_text(f"Gracias por usarme :). Usa \"\\set_username *username*\" para añadir un nuevo nombre de usuario de Twitch.")

async def set_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in init and context.args:    
        username = context.args[0] 
        context.user_data.setdefault("data",{}) 

        if not chat_id in context.user_data["data"]:
            context.user_data["data"][chat_id] = username 

            estado[chat_id] = False 

            await update.message.reply_text(f"Ahora seguiré a \"{context.user_data['data'][chat_id]}\".") 
            job_name = f"{context.user_data['data'][chat_id]}_{chat_id}" 
            
            await star_job_queue(job_queue_name=job_name, context=context, chat_id=chat_id) 
            await context.bot.send_message(chat_id,f"Inicializando el bot.")
        else:
            await stop_job_queue(
                data=context.user_data["data"],
                context=context,
                chat_id=chat_id
            )

            context.user_data["data"][chat_id] = username
            job_name = f'{context.user_data["data"][chat_id]}_{chat_id}'
            
            estado[chat_id] = False

            await star_job_queue(job_queue_name=job_name, context=context, chat_id=chat_id) 
            await context.bot.send_message(chat_id,f"Asignando nuevo nombre de usuario.")
    else:
        if chat_id not in init:
            await context.bot.send_message(update.message.chat_id,f"Por favor, use el comando /start.")
        else:
            await context.bot.send_message(update.message.chat_id, "Coloque un nombre de usuario.")


async def star_job_queue(context: ContextTypes.DEFAULT_TYPE, chat_id,job_queue_name):
    """Inicializa la cola de trabajos"""
    context.job_queue.run_repeating(
        callback=stream_alert, 
        interval=20, 
        first=2, 
        chat_id=chat_id, 
        data=context.user_data, 
        name=job_queue_name
    )

async def stop_job_queue(data, context: ContextTypes.DEFAULT_TYPE, chat_id):
    """Detiene cualquier trabajo que se le pase"""
    print(f"{data.get(chat_id)}_{chat_id}")
    job_name = f"{data.get(chat_id)}_{chat_id}"
    current_job = context.job_queue.get_jobs_by_name(job_name)
    print(f"Deteniendo trabajo: {current_job}")
    if not current_job:
        await context.bot.send_message(chat_id,f"No se han encontrado tareas activas.")
    for job in current_job:
        job.schedule_removal()


async def stop_job_queue_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detener los trabajos desde chat"""
    chat_id = update.message.chat_id
    data = context.user_data.get("data")
    if data:
        await stop_job_queue(data, context, chat_id)
        await context.bot.send_message(chat_id,f"Tareas detenidas.")
    else:
        await context.bot.send_message(chat_id,f"No se han encontrado tareas activas.")



async def stream_alert(context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Ejecutando trabajo: {context.job.name}")
    chat_id = context.job.chat_id 
    username = context.job.data["data"][chat_id]
    if chat_id and not username == None:
        api = TwitchAPI(str(username))
        data = await api.get_data()
        if await api.is_live() == True and estado[chat_id] == False:
            await context.bot.send_message(chat_id, f"{api.user} está en vivo! \n{data['title']} \n{data['game_name']} \n🔴{int(data['viewer_count']):,}🔴 \nhttps://twitch.tv/{api.user} \n@baltaok @Legna")
            estado[chat_id] = True

        elif await api.is_live() == False:
            if estado[chat_id] == True:
                estado[chat_id] = False
                await context.bot.send_message(chat_id, f"Ahora mismo {api.user} no está en vivo! \n@baltaok @Legna")


if __name__ == "__main__":
    app = ApplicationBuilder().token(API_KEY).build()
    try:
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("set_username", set_username))
        app.add_handler(CommandHandler("stop", stop_job_queue_command))
        app.run_polling(close_loop=True,drop_pending_updates=True)
    except KeyboardInterrupt:
        app.shutdown()