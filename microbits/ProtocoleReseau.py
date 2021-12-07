#//ETIENNE
import radio

import json
from securite import *

"""
destination = 1
source = 2
message = "Salut je suis en json"
message = {}

"""

    
class ProtocoleRadio:
    """
    Classe protocoleRadio.
    Comprend toutes les fonctionnalités pour envoyer et recevoir des messages 
    """
    def __init__(self,identifiant):
        self.moi = identifiant#Mon identifiant sur le protocole.
    
    def get_message(self)->str and str:
        """
        Fonctionnalité pour recevoir les messages sur le protocole qui me sont destinés.
        """
        recep = radio.receive()
        if recep:
            #format le message sous forme de json
            try:
                recep = json.loads(Secu().decrypt(recep))
            except Exception:
                print("Le message ne m'était pas destiné, il n'a pas été formaté correctement.")
                return 0,0
            destination = recep["destination"]            
            source = recep["source"]
            message = recep["message"]
            checksum = recep["checksum"]
            
            
            if message_recup[0] == self.moi:
                if Secu().checksum(destination+source+message) == checksum:
                    #le message s'addresse a moi.
                    return source,message# source, message
        return 0,0

    def send_message(self,dest,msg):
        """
        Envoie un message crypté sous le format "dest|source|message|checksum"
        """
        to_send = json.dumps({"destination": dest,"source": self.moi,"message": moi,"checksum":Secu().checksum(dest+self.moi+message)})
        radio.send(Secu().crypt(to_send))
        #return 1 pour send.
        return 1

    
    
    """
    
class ProtocoleRadio:

    Classe protocoleRadio.
     toutes les fonctionnalités pour envoyer et recevoir des messages 
    
    def __init__(self):
        self.moi = "2"#Mon identifiant sur le protocole.
    
    def get_message(self)->str and str:
        
        Fonctionnalité pour recevoir les messages sur le protocole qui me sont destinés.
        
        recep = radio.receive()
        if recep:
            recep = Secu().decrypt(recep)
            
            message_recup = recep.split("|")
            if message_recup[0] == self.moi:
                if Secu().checksum(message_recup[0]+"|"+message_recup[1]+"|"+message_recup[2]) == message_recup[3]:
                    #le message s'addresse a moi.
                    return message_recup[1],message_recup[2]# source, message
        return 0,0

    def send_message(self,dest,msg):
        
        Envoie un message crypté sous le format "dest|source|message|checksum"
        
        to_send_informations = dest+"|"+self.moi+"|"+msg
        to_send = to_send_informations+"|"+Secu().hash(to_send_informations)        
        radio.send(Secu().crypt(to_send))
        #return 1 pour send.
        return 1

    """
