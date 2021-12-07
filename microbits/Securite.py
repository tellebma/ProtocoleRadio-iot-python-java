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
