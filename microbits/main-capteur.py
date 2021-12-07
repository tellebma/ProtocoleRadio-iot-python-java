#//ETIENNE
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text
from microbit import *
import radio

from ProtocoleRadio import *

IDENTIFIANT_RADIO = 2

def get()->(bool or str):
    """
    Fonction qui répond aux messages recu par l'auter microbit.
    Si le destinataire est "1" (l'autre microbit) alors on lui réponds le résultat de la commande.
    """
    source,message = ProtocoleRadio(IDENTIFIANT_RADIO).get_message()
    if source and message:
        if source == "1":            
            if message == "TL":
                ProtocoleRadio(IDENTIFIANT_RADIO).send_message(source,str(temperature())+","+str(display.read_light_level()))   
                return message
            elif message == "LT":
                ProtocoleRadio(IDENTIFIANT_RADIO).send_message(source,str(display.read_light_level())+","+str(temperature()))
                return message
    return False
    
def ask(fonction:str)->str:
    """
    Cette fonction n'est pas utilisée sur cette micro:bit...
    
    Envoie une requete a l'auter microbit, en demandant soit, la température en premier soit, la lumière.

    fonction:
        TL or LT
    """
    ProtocoleRadio(IDENTIFIANT_RADIO).send_message("1",fonction)
    tentative = 0
    while True:
        tentative += 1
        source,message = ProtocoleRadio(IDENTIFIANT_RADIO).get_message()
        if source and message:
            if source == "1":
                return message
        if tentative > 200:
            ProtocoleRadio(IDENTIFIANT_RADIO).send_message("1",fonction)
            tentative = 0


if __name__ == "__main__":
    initialize(pinReset=pin0) #on initialise l'écran OLED
    clear_oled() #on efface l'écran OLED au démarrage
    radio.config(channel=24) #on choisi le channel pour la radio et on l'active
    radio.on()
    previousVal = "TL"
    while True: #on affiche et refresh en permanence les valeurs de luminosité/température sur l'écran suivant l'ordre demandé par le serveur
        
        reponse = get()           
        
        if reponse:
            clear_oled()
            add_text(2, 3, "msg:" + reponse)
            previousVal = reponse
        
        if previousVal == "TL":   
            add_text(2, 1, "temp: " + str(temperature()))
            add_text(2, 2, "lum:  " + str(display.read_light_level()))
        else: # previousVal = LT...
            add_text(2, 1, "lum:  " + str(display.read_light_level()))
            add_text(2, 2, "temp: " + str(temperature()))
