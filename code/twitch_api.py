import requests
import os
import dotenv
import time 
#importamos dotenv, os y requests

#creamos una claser de TwitchAPI
class TwitchAPI:

    #cargamos el entorno. Se le puede dar un "path" para que cargue si así se desea.
    dotenv.load_dotenv()

    #cargamos las variables del entorno previamente puestas en ".env".
    CLIENT_ID:str = os.environ.get("TWITCH_CLIENT_ID")
    CLIENT_SECRET:str = os.environ.get("TWITCH_CLIENT_SECRET")
    
    #definimos el constructor de la clase
    def __init__(self, user) -> None:
        self.__token = None
        self.__token_exp = 0
        self.title = None
        self.user = user
        self.gen_token()

    def __str__(self):
        return f"Username: {self.user}"

    @property 
    def token(self):
        return self.__token

    @property
    def token_exp(self):
        return self.__token_exp

    @token.setter
    def token(self, token):
        self.__token = token
    
    @token_exp.setter
    def token_exp(self, token_exp):
        self.__token_exp = token_exp

    #función para generar los tokens de twitch
    def gen_token(self):
        #hacemos un "post" usando "request" a "https://id.twitch.tv/oauth2/token".
        response=requests.post(
            "https://id.twitch.tv/oauth2/token",
            data={
                "client_id":self.CLIENT_ID,
                "client_secret":self.CLIENT_SECRET,
                "grant_type":"client_credentials"
                #Los datos a cargar en el post y usamos las variables de entorno que hemos creado y obtenido usando "os.environ.get()" de ".env".
            }
        )
        
        #Si la respuesta de "response" es "200 OK" guarda el json de los datos en la variable "data"
        #Accedemos al "acces_token" de los datos anteriormente guardados en "data" y lo asignamos a "token"
        #Accedemos al "expires_in" del json y le sumamos la hora del sistema. Guardamos esos datos en "token_expires"
        if response.status_code == 200:
            data=response.json()
            self.token = data["access_token"]
            self.token_exp = time.time() + data["expires_in"]
        else:
            self.token=None
            self.token_exp=0
        #De no dar "200 OK" vuelve a asignar los valores default de los tokens

    #Retorna "False" cuando el token está expirado o no está generado
    def token_valid(self) -> bool:
        if time.time() < self.token_exp:
            return True
        else:
            return False

    #Evalúa si el token está expirado o si no se ha generado y llama a la función para que lo genere
    async def is_live(self) -> bool:
        
        if not self.token_valid():
            self.gen_token()

        #Hacemos un "get" usando "requests" y guardamos los datos en "response".
        response=requests.get(
            f"https://api.twitch.tv/helix/streams?user_login={self.user}", #le pasamos el usuario a la url de twitch
            headers={
                "Client-Id":self.CLIENT_ID,
                "Authorization":f"Bearer {self.token}"
            }
            #se le pasa el "client_id" y el "Authorization"
        )

        #Comprobamos que el status code de la respuesta sea "200 OK". Además, comprueba si existe data dentro del json de la respuesta, de no ser así, retornamos False

        if response.status_code == 200 and response.json()["data"]:
            return True
        else:
            return False

    async def get_data(self):
        if await self.is_live() == False:
            return {"title":"No estoy en vivo","game_name":"Regresa pronto!"}
        else:
            response = requests.get(
            f"https://api.twitch.tv/helix/streams?user_login={self.user}",
            headers={
                "Client-Id":self.CLIENT_ID,
                "Authorization":f"Bearer {self.token}"})
            
            if response.status_code == 200 and response.json()["data"]:
                data = response.json()["data"]
                return data[0]
            else:
                return {"title":"No estoy en vivo ahora","game_name":"Quédate al pendiente de mi canal de Twitch!"}
    
    def get_url(self):
        return f"https://twitch.tv/{self.user}"
    



if __name__ == "__main__":
    api = TwitchAPI("thedanirep")
    print(api.get_data())