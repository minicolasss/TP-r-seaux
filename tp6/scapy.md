# Bonus Scapy

- [Bonus Scapy](#bonus-scapy)
  - [1. Play it legit](#1-play-it-legit)
  - [2. Maybe not](#2-maybe-not)
    - [A. DHCP starvation](#a-dhcp-starvation)
    - [B. Rogue DHCP](#b-rogue-dhcp)

## 1. Play it legit

🌞 **`ping.py`**

- construit et envoie un paquet ICMP comme la commande `ping`
- envoie un `ping` vers la passerelle (routeur)

[mon ping.py](ping.py)

```zsh
┌──(kali㉿kali)-[~/Desktop]
└─$ sudo python3 ping.py 
.
Sent 1 packets.
Ping envoyé à 10.6.1.254
```

🌞 **`dns_request.py`**

- construit et envoie une requête DNS pour résoudre le nom `thinkerview.com`

[lien vers dns_request.py](./dns_request.py)

- capture la réponse, et affiche l'IP correspondant au nom

```zsh
┌──(kali㉿kali)-[~/Desktop]
└─$ sudo python3 dns_request.py
L'adresse IP de thinkerview.com :  188.114.96.2
```

🌞 **`dhcp request.py`**

- construit et envoie un DHCP Request au serveur DHCP
- je vous conseille de demander la même IP que celle que vous avez déjà
  - envoyer un DHCP Request légitime quoi
- capture la réponse (un Acknowledge) et affichez `ACK reçu` si elle et est bien reçue

## 2. Maybe not

### A. DHCP starvation

➜ **Lors d'un échange DHCP avec un client, le serveur DHCP identifie le cliet avec son adresse MAC.**

Il enregistre dans un *bail DHCP* les traces de l'échange : il a proposé adresse IP à un client qui est identifié par son adresse MAC.

Si on est capables de forger et envoyer des trames à la main, on peut écrire ce qu'on veut en MAC src, et donc se faire passer pour d'autres machines.

➜ **L'attaque *DHCP starvation* consiste à demander toutes les adresses IP possibles du réseau.**

Demander au serveur DHCP de multiples adresses IP, en effectuant de nombreux Request, mais en le faisant systématiquement avec des MAC src différentes.

Le but est de faire croire au serveur DHCP que le réseau est plein de clients, et ainsi atteindre le nombre de max d'adresses disponibles dans le réseau.

⚠️⚠️⚠️⚠️⚠️ **Il est rigoureusement hors de question de faire ça dans le réseau de l'école ou un réseau public.**

🌞 **`dhcp_starvation.py`**

- le script **DOIT** être exécuté dans le réseau du TP6, et cibler votre serveur DHCP
- le script met en place l'attaque DHCP starvation
- il envoie des Request répétés, en changeant d'adresse MAC src jusqu'à atteindre la taille max du réseau
- lorsqu'il n'y a plus d'adresses disponibles d'après le serveur, il ne renvoie plus de DHCP Ack en réponse à un DHCP Request (il renvoie un autre message DHCP)
- vous pouvez détecter ce message pour savoir que l'attaque a été menée à bien

![DHCP starvation](./img/ate_all_ip.png)

### B. Rogue DHCP

Pour mettre en place l'attaque de DHCP spoofing du TP précédent, il fallait monter nous-mêmes un serveur DHCP.

Comme dit dans le TP précédent, il est nécessaire de gagner une *race condition*. Autrement dit, il faut que notre serveur DHCP réponde avant le serveur DHCP légitime.

Une bonne chose pour essayer d'y parvenir est d'avoir un serveur DHCP performant.

Python n'est pas idéal, mais vu que notre programme ne fera QUE répondre à des requêtes DHCP, il y a des chances qu'il présente de bonnes performances.

🌞 **`simplest_dhcp_server.py`**

- le script doit attendre la réception d'un DHCP Discover
  - il répond automatiquement un Offer s'il en reçoit un
- le script doit attendre la réception d'un DHCP Request
  - il répond automatiquement un DHCP ACK
- testez le script en vous faisant attribuer une adresse IP avec un client

> *Ce serveur DHCP simpliste est suffisant pour mener une attaque DHCP spoofing avec d'assez bons résultats.*

![ur dora my dora](./img/urdora.jpg)