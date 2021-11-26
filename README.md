#Mini-projet for 4IRC students at CPE Lyon

## Installing the server
In a new raspbian installation:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git python python-serial minicom
sudo usermod -aG dialout pi
```

Add a line into `rc.local`to start the game


### VM
#### Serveur Ubuntu: 
	id: **ubuntu** **server**
	pass: **password**

 depuis le serveur ubuntu, mettre une @IP  a la machine sur le même port que le Raspberry.
ex : 192.168.1.2 ( Raspberry  192.168.1.1) 
depuis le terminal : 
```bash 
ssh 192.168.1.1 -l pi
```
## config Machine Virtuelle (Cas PC CPE...):
```bash
sudo nano /etc/netplan/{tab}

:: 
# Let NetworkManager manage all devices on this system
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
      - 192.168.1.2/24
::
sudo netplan try
sudo netplan apply

```


# Config Raspberry:

#### Raspberry:
	id: **pi**
	pass: **raspberrycpe**

## config Réseau Raspberry.:
```bash
sudo nano /etc/netplan/{tab}

:: 
# Let NetworkManager manage all devices on this system
network:
  version: 2
  renderer: NetworkManager
  wifis:
    wnp0s3:
      dhcp4: yes
      access-points:
	network_ssid_name: "SSIDwifi"
	password: "CléDeSécuritéwifi"
::
sudo netplan try
sudo netplan apply

git clone https://github.com/tellebma/ProtocoleRadio-iot-python-java
cd ProtocoleRadio-iot-python-java
echo 'python '$PWD'/server/controller.py'>./server/start-server.sh

#LANCER LE SCRIPT :
bash ./server/start-server.sh

```
