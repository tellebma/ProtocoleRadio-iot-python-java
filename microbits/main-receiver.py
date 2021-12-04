#//MAXIME
from microbit import *
import radio

def getFromTel()->None:
    """
    Recupere les commandes souhaitées par le Téléphone.
    Il existe une fonctionnalité de Debug avec les deux boutons
    """
    recep = uart.read()
    if recep:
        return str(recep,'utf-8')
    #Man pr debug.
    if button_a.was_pressed():
        return "TL"
    if button_b.was_pressed():
        return "LT"
    return 0   

def ask(fonction:str)->None:
    """
    Envoie une requete a l'auter microbit, en demandant soit, la température en premier soit, la lumière.

    fonction:
        TL or LT
    """
    ProtocoleRadio().send_message("2",fonction)
    #Demande latemperature a l'autre microbit
    tentative = 0
    while True:
        tentative += 1
        source,message = ProtocoleRadio().get_message()
        if source and message:
            if source == "2": 
                return message
        if tentative > 200:
            ProtocoleRadio().send_message("2",fonction)
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
            key+=1 #pour chaque itération on décale la key de 1 
            cryptedMessage += chr(ord(lettre)+key)
        return cryptedMessage

    def decrypt(self,cryptedMessage:str,key:int=10)->str:
        """
        Passe un message crypté et une clef, le return en message clair. 
        Utilisation d'un césar modifié.
        """
        clearMessage = ""
        for lettre in cryptedMessage:
            key+=1 #pour chaque itération on décale la key de 1 
            clearMessage += chr(ord(lettre)-key)
        return clearMessage
        
    def checksum(self,message:str)->str:
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
    def __init__(self)->None:
	self.moi = "1"#Mon identifiant sur le protocole.
    
    def get_message(self)->str and str:
        """
        Fonctionnalité pour recevoir les messages sur le protocole qui me sont destinés.
        """
        recep = radio.receive()
        if recep:
            message_recup = Secu().decrypt(recep).split("|")
            if message_recup[0] == self.moi:
                if Secu().checksum(message_recup[0]+"|"+message_recup[1]+"|"+message_recup[2]) == message_recup[3]:
                    #le message s'addresse a moi.
                    return message_recup[1],message_recup[2]#1 source,message
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


"""CODE PRINCIPAL POUR LE RECEIVER CONNECTE A LA PASSERELLE"""
if __name__ == "__main__":
    #init radio
    radio.config(channel=24)#les deux channels doivent être identique entre les deux microbits.
    radio.on()
    uart.init(115200)
    while True:
        """
        Main Boucle
        """
        demande = getFromTel()#commande recu par le téléphone.
        if demande:
            message = ask(demande)#recupere le message souhaité par le téléphone.
            sleep(500)
            uart.write(bytes(message,'utf-8'))#envoi a la raspberry la réponse au message
