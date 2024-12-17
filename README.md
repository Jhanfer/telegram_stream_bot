
# Telegram Stream Bot

Este bot de Telegram está diseñado para interactuar con usuarios y gestionar alertas personalizadas. Sus principales características son:

* Registro de Usuarios: Permite a los usuarios registrar un __username__ de twitch. El bot almacena esta información junto con el chat_id del chat para futuras interacciones.

* Gestión de Alertas: Una vez registrado, el bot procede a crear trabajos que verificaran si el __username__ proporcionado al inicializar el bot está en vivo. El bot enviará una alerta al iniciar el stream y otra al terminarlo.

* Manejo de Errores: El bot incluye manejo de errores en casos de que el servidor tarde en enviar los datos o de errores de protocolos, reintentando la llamada.

* Interacción Dinámica: Responde a las interacciones de los usuarios con el motivo de informar que los comandos se están ejecutando de manera correcta.

* Configuración Personalizada: El bot tiene la capacidad de gestionarse en distintos chats, esto permite que cada usuario pueda configurarlo y este va a respetar esas configuraciones por chat.

---
#### Ejecutar el script:

- Clonar este repositorio usando:
```
$ git clone https://github.com/Jhanfer/telegram_stream_bot.git
```
- Dirigirse a la carpeta del repositorio y posteriormente a code:
```
$ cd telegram_stream_bot
$ cd code
```
- Entrar al script y cambiar la variable "API_KEY" por su propia clave api obtenida en el [bot father](https://telegram.me/BotFather).

- Ejecutar el script:
```
$ chmod +x telegram_bot.py #se le da permisos
$ ./telegram_bot.py
```

#### Dependencias necesarias: 
* python-telegram-bot == 20.3
* python-telegram-bot[job-queue]

> [!IMPORTANT]  
> Se necesita tener una API KEY que se obtiene en el [bot father](https://telegram.me/BotFather) de telegram para poder ejecutar el script.

---

---

Este bot ha surgido como una idea de poder avisar sobre streams en twitch en # grupos o chats de telegram.

He utilizado la api [python-telegram-bot](https://docs.python-telegram-bot.org/en/v21.7/index.html) y mi propia api de twitch. El bot se encuentra desplegado en [pthonanyware](https://www.pythonanywhere.com) por lo que puede presentar retrasos o lentitud de ejecución.


---
#### Gracias por leer c: 