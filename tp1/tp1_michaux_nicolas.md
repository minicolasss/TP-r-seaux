I. Récolte d'informations


🌞 Adresses IP de ta machine

affiche l'adresse IP que ta machine a sur sa carte réseau WiFi
affiche l'adresse IP que ta machine a sur sa carte réseau ethernet

 Réponse :
 ```
PS C:\Users\NICOLAS> ipconfig /all

Carte réseau sans fil Wi-Fi :
Adresse IPv4. . . . . . . . . . . . . .: 10.33.76.110
   ```


🌞 Si t'as un accès internet normal, d'autres infos sont forcément dispos...

affiche l'adresse IP de la passerelle du réseau local

affiche l'adresse IP du serveur DNS que connaît ton PC
affiche l'adresse IP du serveur DHCP que connaît ton PC

 Réponse :
 ```
    PS C:\Users\NICOLAS> ipconfig /all

    Carte réseau sans fil Wi-Fi :

      Passerelle par défaut. . . . . . . . . : 10.33.79.254
         Serveurs DNS. . .  . . . . . . . . . . : 8.8.8.8
        Serveur DHCP . . . . . . . . . . . . . : 10.33.79.254
```



🌟 BONUS : Détermine s'il y a un pare-feu actif sur ta machine

détermine s'il exise un pare-feu actif sur votre machine
si oui, je veux aussi voir une commande pour lister les règles du pare-feu

   réponse : 


   ```

 PS C:\Users\NICOLAS> Get-NetFirewallProfile | ft Name,Enabled

      Name    Enabled
      ----    -------
      Domain     True
      Private    True
      Public     True
```

```
      PS C:\Users\NICOLAS>  New-NetFirewallRule -DisplayName "Autoriser le Bureau à distance (RDP)" -Group "Bureau à distance" -Profile Domain -Enabled True -Action Allow

         Name                          : {51d1b0e8-64f1-4c72-aa0a-ee9d4c9a5f86}
         DisplayName                   : Autoriser le Bureau à distance (RDP)
         Description                   :
         DisplayGroup                  : Bureau à distance
         Group                         : Bureau à distance
         Enabled                       : True
         Profile                       : Domain
         Platform                      : {}
         Direction                     : Inbound
         Action                        : Allow
         EdgeTraversalPolicy           : Block
         LooseSourceMapping            : False
         LocalOnlyMapping              : False
         Owner                         :
         PrimaryStatus                 : OK
         Status                        : La règle a été analysée à partir de la banque. (65536)
         EnforcementStatus             : NotApplicable
         PolicyStoreSource             : PersistentStore
         PolicyStoreSourceType         : Local
         RemoteDynamicKeywordAddresses : {}
         PolicyAppId                   :
```


II. Utiliser le réseau

   🌞 Envoie un ping vers...

fais un ping vers ta propre adresse IP

vers l'adresse IP 127.0.0.1

réponse : 
```
   PS C:\Users\NICOLAS> ping 10.33.76.110

   Envoi d’une requête 'Ping'  10.33.76.110 avec 32 octets de données :
   Réponse de 10.33.76.110 : octets=32 temps<1ms TTL=128
   Réponse de 10.33.76.110 : octets=32 temps<1ms TTL=128
   Réponse de 10.33.76.110 : octets=32 temps<1ms TTL=128
   Réponse de 10.33.76.110 : octets=32 temps<1ms TTL=128

   Statistiques Ping pour 10.33.76.110:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
   Durée approximative des boucles en millisecondes :
    Minimum = 0ms, Maximum = 0ms, Moyenne = 0ms
```
```
    PS C:\Users\NICOLAS> ping 127.0.0.1

   Envoi d’une requête 'Ping'  127.0.0.1 avec 32 octets de données :
   Réponse de 127.0.0.1 : octets=32 temps<1ms TTL=128
   Réponse de 127.0.0.1 : octets=32 temps<1ms TTL=128
   Réponse de 127.0.0.1 : octets=32 temps<1ms TTL=128
   Réponse de 127.0.0.1 : octets=32 temps<1ms TTL=128

   Statistiques Ping pour 127.0.0.1:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
   Durée approximative des boucles en millisecondes :
    Minimum = 0ms, Maximum = 0ms, Moyenne = 0ms
```


🌞 On continue avec ping. Envoie un ping vers...

ta passerelle

un(e) pote sur le réseau

un site internet


réponse : 
```
   PS C:\Users\NICOLAS> ping 10.33.79.254

   Envoi d’une requête 'Ping'  10.33.79.254 avec 32 octets de données :
   Délai d’attente de la demande dépassé.
   Délai d’attente de la demande dépassé.

   Statistiques Ping pour 10.33.79.254:
    Paquets : envoyés = 2, reçus = 0, perdus = 2 (perte 100%)
```
```
    PS C:\Users\NICOLAS> ping 10.33.77.159

   Envoi d’une requête 'Ping'  10.33.77.159 avec 32 octets de données :
   Réponse de 10.33.77.159 : octets=32 temps=4 ms TTL=128
   Réponse de 10.33.77.159 : octets=32 temps=17 ms TTL=128
   Réponse de 10.33.77.159 : octets=32 temps=5 ms TTL=128
   Réponse de 10.33.77.159 : octets=32 temps=5 ms TTL=128

   Statistiques Ping pour 10.33.77.159:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
   Durée approximative des boucles en millisecondes :
    Minimum = 4ms, Maximum = 17ms, Moyenne = 7ms
```
```
    ping www.thinkerview.com

   Envoi d’une requête 'ping' sur www.thinkerview.com [188.114.96.7] avec 32 octets de données :
   Réponse de 188.114.96.7 : octets=32 temps=17 ms TTL=55
   Réponse de 188.114.96.7 : octets=32 temps=16 ms TTL=55
   Réponse de 188.114.96.7 : octets=32 temps=15 ms TTL=55
   Réponse de 188.114.96.7 : octets=32 temps=15 ms TTL=55

   Statistiques Ping pour 188.114.96.7:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
   Durée approximative des boucles en millisecondes :
    Minimum = 15ms, Maximum = 17ms, Moyenne = 15ms
```
🌞 Faire une requête DNS à la main

   réponse : 

```
PS C:\Users\NICOLAS> nslookup www.thinkerview.com
Serveur :   dns.google
Address:  8.8.8.8

Réponse ne faisant pas autorité :
Nom :    www.thinkerview.com
Addresses:  2a06:98c1:3120::7
         2a06:98c1:3121::7
         188.114.97.7
         188.114.96.7
```
```
PS C:\Users\NICOLAS> nslookup www.wikileaks.org
Serveur :   dns.google
Address:  8.8.8.8

Réponse ne faisant pas autorité :
Nom :    wikileaks.org
Addresses:  80.81.248.21
         51.159.197.136
Aliases:  www.wikileaks.org
```

```
PS C:\Users\NICOLAS> nslookup www.torproject.org
Serveur :   dns.google
Address:  8.8.8.8

Réponse ne faisant pas autorité :
Nom :    www.torproject.org
Addresses:  2a01:4f8:fff0:4f:266:37ff:feae:3bbc
         2620:7:6002:0:466:39ff:fe7f:1826
         2a01:4f9:c010:19eb::1
         2620:7:6002:0:466:39ff:fe32:e3dd
         2a01:4f8:fff0:4f:266:37ff:fe2c:5d19
         204.8.99.144
         116.202.120.165
         95.216.163.36
         116.202.120.166
         204.8.99.146
```
         
III. Sniffer le réseau

🌞 J'attends dans le dépôt git de rendu un fichier ping.pcap

réponse :
```
   PS C:\Users\NICOLAS> ping google.com
 ```
[lien vers ma capture](./ping1.pcap)
```
PS C:\Users\NICOLAS> ping DNS
```
[lien vers ma capture](./dns.pcap)

IV. Network scanning et adresses IP

🌞 Effectue un scan du réseau auquel tu es connecté

Réponse :

```
PS C:\Users\NICOLAS> nmap -sn -PR 10.33.64.0/20
```
```
Nmap done: 4096 IP addresses (520 hosts up) scanned in 170.05 seconds
```


🌞 Changer d'adresse IP

mon adresse ip de base : 

```
 IPv4 Address. . . . . . . . . . . : 192.168.0.44
 ```

 Pour changer l'adresse IP, j'ai exécuté la commande.


 ```
 PS C:\Users\NICOLAS> netsh interface ip set address "Wi-Fi" static 192.168.0.58 255.255.255.0 192.168.0.254
 ```

 Et voici ma nouvelle adresse IP.

 ```
  IPv4 Address. . . . . . . . . . . : 192.168.0.58
 ```