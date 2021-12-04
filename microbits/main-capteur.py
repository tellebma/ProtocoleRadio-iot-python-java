#//ETIENNE
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from microbit import *
import radio

def get()->(bool or str):
    """
    Fonction qui répond aux messages recu par l'auter microbit.
    Si le destinataire est "1" (l'autre microbit) alors on lui réponds le résultat de la commande.
    """
    source,message = ProtocoleRadio().get_message()
    if source and message:
        if source == "1":            
            if message == "TL":
                ProtocoleRadio().send_message(source,str(temperature())+","+str(display.read_light_level()))   
                return message
            elif message == "LT":
                ProtocoleRadio().send_message(source,str(display.read_light_level())+","+str(temperature()))
                return message
    return False
    
def ask(fonction:str)->str:
    """
    Envoie une requete a l'auter microbit, en demandant soit, la température en premier soit, la lumière.

    fonction:
        TL or LT
    """
    ProtocoleRadio().send_message("1",fonction)
    tentative = 0
    while True:
        tentative += 1
        source,message = ProtocoleRadio().get_message()
        if source and message:
            if source == "1":
                return message
        if tentative > 200:
            ProtocoleRadio().send_message("1",fonction)
            tentative = 0

class Secu:
    """
    Class de sécurité, comprend toutes les fonctionnalités liées à la Sécu entre les microbits.       
    Securité. vraiment très sur!
    Algo de césar remodifié car on est vraiement très chaud  ! 
    """
    def crypt(self,message:str,key:int=10)->str:
        """
        Passe un message clair, le return en message crypté 
        Utilisation d'un césar modifié.
        """
        cryptedMessage = ""
        for lettre in message:
            key+=1 # pour chaque itération on décale la key de 1
            cryptedMessage += chr(ord(lettre)+key)
        return cryptedMessage

    def decrypt(self,cryptedMessage:str,key:int=10)->str:
        """
        Passe un message crypté et une clef, le return en message clair. 
        Utilisation d'un césar modifié.
        """
        clearMessage = ""
        for lettre in cryptedMessage:
            key+=1 # pour chaque itération on décale la key de 1
            clearMessage += chr(ord(lettre)-key)
        return clearMessage
        
    def hash(self,message:str)->str:
        """
        fonction de checksum entre les deux microbits.
        Nous permet de verifier l'intégrité du message.
        #Reste très basic car si un octet du message est incrémenté et un second décrémenté alors l'intégrité sera vue comme juste.
        """
        checksum = 0
        for letter in message:
            checksum += ord(letter)
        return str(checksum)    
    """
    import hashlib ne fonctionne pas :/
    def checksum(self,message):
        return hashlib.md5(message.encode()).hexdigest()
    """
    
class ProtocoleRadio:
    """
    Classe protocoleRadio.
    Comprend toutes les fonctionnalités pour envoyer et recevoir des messages 
    """
    def __init__(self):
        self.moi = "2"#Mon identifiant sur le protocole.
    
    def get_message(self)->str and str:
        """
        Fonctionnalité pour recevoir les messages sur le protocole qui me sont destinés.
        """
        recep = radio.receive()
        if recep:
            recep = Secu().decrypt(recep)
            message_recup = recep.split("|")
            if message_recup[0] == self.moi:
                if Secu().hash(message_recup[0]+"|"+message_recup[1]+"|"+message_recup[2]) == message_recup[3]:
                    #le message s'addresse a moi.
                    return message_recup[1],message_recup[2]# source, message
        return 0,0

    def send_message(self,dest,msg):
        """
        Envoie un message crypté sous le format "dest|source|message|checksum"
        """
        to_send_informations = dest+"|"+self.moi+"|"+msg
        to_send = to_send_informations+"|"+Secu().hash(to_send_informations)        
        radio.send(Secu().crypt(to_send))
        #return 1 pour send.
        return 1


if __name__ == "__main__":
    initialize(pinReset=pin0) #on initialise l'écran OLED
    clear_oled() #on efface l'écran OLED au démarrage
    radio.config(channel=24) #on choisi le channel pour la radio et on l'active
    radio.on()
    previousVal = True
    while True: #on affiche et refresh en permanence les valeurs de luminosité/température sur l'écran suivant l'ordre demandé par le serveur
        
        reponse = get()           
        
        if reponse:
            add_text(2, 3, "msg:" + reponse)
            previousVal = reponse
        
        if previousVal == "TL":            
            add_text(2, 1, "temp: "+ str(temperature()))
            add_text(2, 2, "lum: " + str(display.read_light_level()))
        else: # previousVal = LT...
            add_text(2, 1, "lum: " + str(display.read_light_level()))
            add_text(2, 2, "temp: "+ str(temperature()))
