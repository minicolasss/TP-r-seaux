# TP1 : Les premiers pas de bébé B1


## Sommaire

  - [Sommaire](#sommaire)
- [I. Récolte d'informations](#i-récolte-dinformations)
- [II. Utiliser le réseau](#ii-utiliser-le-réseau)
- [III. Sniffer le réseau](#iii-sniffer-le-réseau)
- [IV. Network scanning et adresses IP](#iv-network-scanning-et-adresses-ip)


# I. Récolte d'informations


🌞 **Adresses IP de ta machine**

- affiche l'adresse IP que ta machine a sur sa carte réseau WiFi
```zsh
┌─[nico@parrot]─[~]
└──╼ $ip a
...
3: wlo1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
...
    inet 192.168.0.44/24 brd 192.168.0.255 scope global dynamic noprefixroute wlo1
...
```
- affiche l'adresse IP que ta machine a sur sa carte réseau ethernet
```zsh
┌─[nico@parrot]─[~]
└──╼ $ip a
...
2: enp55s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether e8:9c:25:d1:3f:f3 brd ff:ff:ff:ff:ff:ff
    
    
[Vu qu'elle n'est pas connectée, je n'ai pas d'IP mais si j'en avais une, elle serait là]
```

🌞 **Si t'as un accès internet normal, d'autres infos sont forcément dispos...**

- affiche l'adresse IP de la passerelle du réseau local
```zsh
┌─[nico@parrot]─[~]
└──╼ $ip route
default via 192.168.0.254 dev wlo1 proto dhcp src 192.168.0.44 metric 600 
192.168.0.0/24 dev wlo1 proto kernel scope link src 192.168.0.44 metric 600 
```
- affiche l'adresse IP du serveur DNS que connaît ton PC
```zsh
┌─[nico@parrot]─[~]
└──╼ $nmcli dev show | grep DNS
IP4.DNS[1]:                             192.168.0.254
```
- affiche l'adresse IP du serveur DHCP que connaît ton PC
```zsh 
┌─[nico@parrot]─[/var/lib/dhcp]
└──╼ $nmcli device show
GENERAL.DEVICE:                         wlo1
...
IP4.ADDRESS[1]:                         192.168.0.44/24
IP4.GATEWAY:                            192.168.0.254
IP4.ROUTE[1]:                           dst = 0.0.0.0/0, nh = 192.168.0.254, mt = 600
IP4.ROUTE[2]:                           dst = 192.168.0.0/24, nh = 0.0.0.0, mt = 600
IP4.DNS[1]:                             192.168.0.254


[Comme on peut le voir, mon serveur DHCP est mon routeur chez moi]
```

🌟 **BONUS** : Détermine s'il y a un pare-feu actif sur ta machine

- toujours à l'aide d'une commande dans votre terminal
- détermine s'il exise un pare-feu actif sur votre machine
- si oui, je veux aussi voir une commande pour lister les règles du pare-feu
- demande à google, ça tombe direct !
```zsh
┌─[nico@parrot]─[/var/lib/dhcp]
└──╼ $sudo iptables -L -v -n
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination 



┌─[nico@parrot]─[/var/lib/dhcp]
└──╼ $sudo ufw status
Status: inactive
```

# II. Utiliser le réseau


🌞 **Envoie un `ping` vers...**

- **toi-même !**
  - fais un `ping` vers ta propre adresse IP
  - vous devriez constater que le temps de l'aller-retour est extrêment court
```zsh
┌─[nico@parrot]─[/var/lib/dhcp]
└──╼ $ping 192.168.0.44
PING 192.168.0.44 (192.168.0.44) 56(84) bytes of data.

--- 192.168.0.44 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1015ms
rtt min/avg/max/mdev = 0.047/0.058/0.070/0.011 ms
```
- **vers l'adresse IP `127.0.0.1`**

```zsh
┌─[nico@parrot]─[/var/lib/dhcp]
└──╼ $ping 127.0.0.1
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.

--- 127.0.0.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.041/0.053/0.066/0.012 ms
```

🌞 **On continue avec `ping`.** Envoie un `ping` vers...

- **ta passerelle**
  - t'as repéré son adresse IP dans la première partie
  - soyez attentifs au temps d'aller-retour
```zsh
┌─[nico@parrot]─[/var/lib/dhcp]
└──╼ $ping 192.168.0.254
PING 192.168.0.254 (192.168.0.254) 56(84) bytes of data.

--- 192.168.0.254 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 3.133/3.658/4.184/0.525 ms
```
- **un(e) pote sur le réseau**
  - demande l'adresse IP de quelqu'un qui est connecté au même réseau local que toi, là, tout de suite
  - fais un `ping` vers son adresse IP
  - vous devriez constater un temps similaire à celui de la passerelle
  - si le `ping` marche pas, je parie que ton pote est sous Windows. Par défaut, le pare-feu de Windows bloque les message `ping` qu'il reçoit, il faudra temporairement le désactiver
```zsh
┌─[✗]─[nico@parrot]─[/var/lib/dhcp]
└──╼ $ping 192.168.0.49
PING 192.168.0.49 (192.168.0.49) 56(84) bytes of data.

--- 192.168.0.49 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 2.864/3.625/4.748/0.810 ms
```
- **un site internet**
  - fais un `ping` vers un site que tu connais
  - par exemple `ping www.thinkerview.com`
  - vous devriez constater que le temps est plus long
```zsh
┌─[nico@parrot]─[~]
└──╼ $ping www.thinkerview.com
PING www.thinkerview.com(2a06:98c1:3121::2 (2a06:98c1:3121::2)) 56 data bytes

--- www.thinkerview.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 13.976/14.250/14.524/0.274 ms
```


🌞 **Faire une requête DNS à la main**

- ça se fait en une seule commande, je te laisse la chercher sur internet
- effectue une requête DNS à la main pour obtenir l'adresse IP qui correspond aux noms de domaine suivants:
  - `www.thinkerview.com`
```zsh
┌─[✗]─[nico@parrot]─[~]
└──╼ $nslookup www.thinkerview.com
Server:		192.168.0.254
Address:	192.168.0.254#53

Non-authoritative answer:
Name:	www.thinkerview.com
Address: 188.114.96.2
Name:	www.thinkerview.com
Address: 188.114.97.2
Name:	www.thinkerview.com
Address: 2a06:98c1:3121::2
Name:	www.thinkerview.com
Address: 2a06:98c1:3120::2
```
  - `www.wikileaks.org`
```zsh
┌─[nico@parrot]─[~]
└──╼ $nslookup www.wikileaks.org
Server:		192.168.0.254
Address:	192.168.0.254#53

Non-authoritative answer:
www.wikileaks.org	canonical name = wikileaks.org.
Name:	wikileaks.org
Address: 51.159.197.136
Name:	wikileaks.org
Address: 80.81.248.21
  - `www.torproject.org`
```
  - `www.torproject.org`
```zsh
┌─[nico@parrot]─[~]
└──╼ $nslookup www.torproject.org
Server:		192.168.0.254
Address:	192.168.0.254#53

Non-authoritative answer:
Name:	www.torproject.org
Address: 204.8.99.144
Name:	www.torproject.org
Address: 204.8.99.146
Name:	www.torproject.org
Address: 116.202.120.165
Name:	www.torproject.org
Address: 95.216.163.36
Name:	www.torproject.org
Address: 116.202.120.166
Name:	www.torproject.org
Address: 2a01:4f9:c010:19eb::1
...
```

# III. Sniffer le réseau

➜ **Refais les commandes `ping` de la partie précédente**

- mais avec Wireshark ouvert
- tu peux saisir "icmp" dans la barre du haut pour filtrer le trafic et n'afficher que les paquets ICMP
- `ping` et `pong` sont des paquets de type ICMP ;)
- tu devrais **voir** les pings et les pongs passer
- pour chaque message, tu devrais voir
  - le type du paquet (ICMP pour le ping)
  - plus spécifiquement, si c'est...
    - un `ping` : tu verras `echo request` ou `ICMP type 8`
    - un `pong` : pour lui c'est `echo reply` ou `ICMP type 0`
  - l'adresse IP source (l'émetteur du message)
  - l'adresse IP de destination (le destinataire du message)
- fais l'effort d'identifier chaque ping envoyé, et chaque pong correspondant

🌞 **J'attends dans le dépôt git de rendu un fichier `ping.pcap`**

- c'est une capture Wireshark
- elle ne doit contenir que les paquets demandés, absolument aucun autre

[lien vers ma capture](./ping.pcap)

J'ai pour mon routeur donc on voit que j'envoie un ping et que je reçois un pong de même pour mon autre pc

[lien vers ma capture](./ping-web.pcap)

On voit que je ping les sites demandés et je reçois les pong

🌞 **Livrez un deuxième fichier : `dns.pcap`**

- il contient une capture des 3 requêtes DNS demandées plus haut
- avec les réponses DNS associées

[lien vers ma capture](./dns1.pcap)

on voit que je ping www.thinkerview.com 

[lien vers ma capture](./dns2.pcap)

on voit que je ping www.wikileaks.org

[lien vers ma capture](./dns3.pcap)

on voit que je ping www.torproject.org

# IV. Network scanning et adresses IP

Le but de cette dernière partie est simple : **faire un scan réseau pour découvrir les autres machines connectées au même réseau que nous**.



🌞 **Effectue un scan du réseau auquel tu es connecté**

- avec une seule commande `nmap`
- je vous recommande de faire un scan comme ça : `nmap -sn -PR <NETWORK_ADDRESS>`
- si vous ne savez pas quoi écrire comme `<NETWORK_ADDRESS>` ou êtes un peu perdus, appelez-moi !
```zsh                                                                        
┌──(oui㉿oui)-[~]
└─$ nmap -sn -PR 192.168.0.254/24
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-27 11:22 CET
Nmap scan report for 192.168.0.6
Host is up (0.30s latency).
Nmap scan report for 192.168.0.22
Host is up (0.35s latency).
Nmap scan report for 192.168.0.31
Host is up (0.44s latency).
Nmap scan report for 192.168.0.41
Host is up (0.0013s latency).
Nmap scan report for 192.168.0.44
Host is up (0.0015s latency).
Nmap scan report for 192.168.0.50
Host is up (0.0065s latency).
Nmap scan report for 192.168.0.254
Host is up (0.0028s latency).
Nmap done: 256 IP addresses (7 hosts up) scanned in 18.19 seconds
```

🌞 **Changer d'adresse IP**

- tu peux faire cette étape avec ton interface graphique si tu veux
- **change l'adresse IP de ta carte Wi-Fi**, choisis-en une que tu sais libre (une que tu n'as pas repérée avec le scan)
- si on te demande un masque, une adresse de passerelle, une adresse de DNS, tu remets les même infos que celles récoltées dans la partie 1, tu changes juste ton adresse IP
- **une fois que c'est fait, utilise une commande pour afficher l'adresse IP sur la carte WiFi** (on devrait voir l'IP que tu as choisi), c'est ça que je veux dans le compte-rendu
ip de base
```zsh                                                                           
┌──(oui㉿oui)-[~]
└─$ ip a           

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:89:a3:6a brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.41/24 brd 192.168.0.255 scope global dynamic noprefixroute eth0
       valid_lft 43196sec preferred_lft 43196sec
    inet6 fe80::35:adfc:9ff0:108/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```
Après le changement
```zsh
┌──(oui㉿oui)-[~]
└─$ ip a   

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:89:a3:6a brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.85/24 brd 192.168.0.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
           inet6 fe80::35:adfc:9ff0:108/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```
