#//MAXIME
from microbit import *
import radio
from ProtocoleRadio import *

IDENTIFIANT_RADIO = 1

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
    ProtocoleRadio(IDENTIFIANT_RADIO).send_message("2",fonction)
    #Demande latemperature a l'autre microbit
    tentative = 0
    while True:
        tentative += 1
        source,message = ProtocoleRadio(IDENTIFIANT_RADIO).get_message()
        if source and message:
            if source == "2": 
                return message
        if tentative > 200:
            ProtocoleRadio(IDENTIFIANT_RADIO).send_message("2",fonction)
            tentative = 0


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
