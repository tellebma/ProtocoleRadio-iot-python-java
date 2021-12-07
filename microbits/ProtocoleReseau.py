#//ETIENNE

import radio
from securite import *



    
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
                if Secu().checksum(message_recup[0]+"|"+message_recup[1]+"|"+message_recup[2]) == message_recup[3]:
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
