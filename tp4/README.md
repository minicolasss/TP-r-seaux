# TP4 : DHCP et accès internet


## Sommaire

- [TP4 : DHCP et accès internet](#tp4--dhcp-et-accès-internet)
  - [Sommaire](#sommaire)
- [I. DHCP](#i-dhcp)
  - [1. Les mains dans le capot](#1-les-mains-dans-le-capot)


# I. DHCP


## 1. Les mains dans le capot

☀️ **Capturez un échange DHCP complet**

- capture `dhcp.pcap`
- il y a 4 trames (le DORA) : Discover, Offer, Request, Acknowledge

dans ma capture on retrouve le Discover , Offer , Request , ACK
[lien vers ma capture](dhcp.pcap)

☀️ **Directement dans Wireshark, vous pouvez voir toutes les infos que vous donne  le serveur DHCP**

- retrouvez dans l'échange DHCP les 3 infos dont on parle plus haut :
  - adresse IP proposée
```
DHCP offer

Dynamic Host Configuration Protocol (Offer)

Your (client) IP address: 10.33.76.110
```
  - serveur DNS indiqué
```
Dynamic Host Configuration Protocol (Offer)

Option: (6) Domain Name Server

Domain Name Server: 8.8.8.8
```
  - passerelle du réseau
```
Dynamic Host Configuration Protocol (Offer)

Option: (3) Router

Router: 10.33.79.254
```
