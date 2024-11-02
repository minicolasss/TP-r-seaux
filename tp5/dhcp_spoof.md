# Bonus : DHCP spoofing

L'idée du DHCP spoofing est d'usurper la place du serveur DHCP dans un réseau local. L'attaquant se fait passer pour un serveur DHCP, et répond aux clients à la place du serveur DHCP légitime.

> Il est évident que vous ne réalisez pas cette attaque sur le réseau de l'école, genre jamais :) Y'a de toute façon des choses bien plus avancées et intéressantes à faire et explorer !

## Sommaire

- [Bonus : DHCP spoofing](#bonus--dhcp-spoofing)
  - [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
- [I. La théorie](#i-la-théorie)
  - [1. DHCP vulnerable by design](#1-dhcp-vulnerable-by-design)
  - [2. DHCP spoofing](#2-dhcp-spoofing)
- [II. Alataaaak](#ii-alataaaak)

# 0. Prérequis

➜ **Machine `routeur.tp5.b1` up&runnin**

- elle doit avoir le service DHCP actif
- testez de nouveau qu'un client peut bien récupérer une adresse IP pour être sûrs qu'il fonctionne :d

➜ **Deux clients**

- un qui sera la victime
- le deuxième sera l'attaquant

# I. La théorie

## 1. DHCP vulnerable by design

➜ **Le protocole DHCP est un protocole vulnérable *by design*.**

C'est à dire qu'un attaquant peut mettre à profit une configuration normale d'un serveur DHCP.

C'est à dire que dans n'importe quel réseau, sans protections additionnelles, un serveur DHCP est *forcément* vulnérable.

➜ **L'idée est la même que pour l'attaque *ARP spoofing* : le problème est la première trame envoyée en *broadcast*.**

En effet, lors d'un échange légitime DHCP, 4 trames sont échangées entre le client et le serveur (le DORA).

La première trame, le Discover, est envoyée par le client.

Le client vient de se connecter au réseau, il envoie une trame Discover en broadcast, afin d'essayer de trouver un serveur DHCP au sein du réseau.

➜ **Une machine déjà connectée au LAN, contrôlée par un acteur malveillant, pourrait choisir de répondre à cette trame, et continuer l'échange DORA avec le client, en se faisant passer pour le serveur DHCP.**

On parle alors de ***DHCP spoofing*** : l'attaquant se fait passer pour un serveur DHCP.

![DHCP now](./img/dhcpnow.png)

## 2. DHCP spoofing

➜ **L'attaquant va donc continuer l'échange DHCP, et répondre un *Offer*.**

Il choisit et propose alors au client :

- une adresse IP valide
- une adresse de passerelle
- une adresse de serveur DNS

Evidemment, l'attaquant est libre de mettre sa propre adresse IP en tant que passerelle et/ou en tant que serveur DNS...

➜ **Pour que ça marche :**

- il faut que l'attaquant réponde AVANT le serveur DHCP légitime
- **on parle de *race condition*** : l'attaquant fait la course avec un autre programme

➜ **Pour que ce soit transparent pour le client :**

- **il faut que l'adresse IP proposée soit valide et libre**
  - on peut genre scan le réseau avant !
- **si l'adresse de passerelle filée est celle de l'attaquant**
  - il faut que la machine de l'attaquant se comporte comme un routeur
  - comme ça elle fait vraiment passer les paquets vers internet
- **si l'adresse du serveur DNS filée est celle de l'attaquant**
  - il faut répondre des DNS answer correctes, donc faire tourner un serveur DNS sur la machine de l'attaquant par exemple
  - l'idée sera d'intercepter certaines requêtes, et répondre de fausses adresses IP
  - pour rediriger le client sur les serveurs de notre choix

# II. Alataaaak

☀️ **Installer et configurer un serveur DHCP sur la machine attaquante**

- désignez l'un des clients comme attaquant
- je vous conseille d'utiliser Dnsmasq comme serveur DHCP
- définissez une vraie passerelle et un vrai serveur DNS
- définissez une range d'adresse proposées bien remarquable genre `.240` à `.250`

☀️ **Depuis un autre client, demander un adresse IP en DHCP**

- déterminer si vous avez une adresse IP proposée par le vrai serveur DHCP ou la machine de l'attaquant
- lancer Wireshark ou `tcpdump` pour capturer l'échange et constater la *race condition*
- la capture doit s'appeler `dhcp_spoof.pcapng` et ne doit contenir QUE les trames DHCP

☀️ **Pour que ça marche mieux, il faut flood le serveur DHCP réel**

- si l'attaquant flood le serveur DHCP réel, il peut le ralentir suffisamment...
- suffisamment pour gagner la *race condition*
- il faut flood par exemple :
  - le port utilisé par le serveur DHCP
  - ou simplement avec de l'ICMP (genre des `ping`)
  - on s'en fout, faut flood hard
- utilisez un tool, sinon en quelques lignes de `bash` ça se fait

> 💡 *Rien ne sert de courir vite pour gagner la course, si tu peux tirer une balle dans les jambes de ton adversaire.*

![DHCP gun](./img/dhcp_gun.png)
