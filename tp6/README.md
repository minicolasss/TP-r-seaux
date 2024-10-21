# TP6 : Des bo services dans des bo LANs

## Sommaire

- [TP6 : Des bo services dans des bo LANs](#tp6--des-bo-services-dans-des-bo-lans)
  - [Sommaire](#sommaire)
- [I. Le setup](#i-le-setup)
  - [1. Tableau d'adressage](#1-tableau-dadressage)
  - [2. Marche à suivre](#2-marche-à-suivre)
  - [II. LAN clients](#ii-lan-clients)
  - [1. Serveur DHCP](#1-serveur-dhcp)
  - [2. Client](#2-client)
- [III. LAN serveurzzzz](#iii-lan-serveurzzzz)
  - [1. Serveur Web](#1-serveur-web)
  - [2. Serveur DNS](#2-serveur-dns)
  - [3. Serveur DHCP](#3-serveur-dhcp)
  - [4. Bonus : forger des trames](#4-bonus--forger-des-trames)

# I. Le setup


## 1. Tableau d'adressage

| Machine          | LAN1 `10.6.1.0/24` | LAN2 `10.6.2.0/24` |
|------------------|--------------------|--------------------|
| `dhcp.tp6.b1`    | `10.6.1.253`       | x                  |
| `client1.tp6.b1` | DHCP               | x                  |
| `routeur.tp6.b1`  | `10.6.1.254`       | `10.6.2.254`       |
| `web.tp6.b1`     | x                  | `10.6.2.11`        |
| `dns.tp6.b1`     | x                  | `10.6.2.12`        |
| Votre PC         | `10.6.1.1`         | `10.6.2.1`         |

## 2. Marche à suivre

➜ **Créez deux nouveaux host-only**

```
Dans VirtualBox Manager, dans l'onglet tools et network.

On crée de host-only 

Vboxnet 1 : 10.6.1.1
Vboxnet 2 : 10.6.2.1
```


☀️ **Prouvez que...**

- une machine du LAN1 peut joindre internet (ping un nom de domaine)
```zsh
┌──(kali㉿client1)-[~]
└─$ ping ynov.com 

--- ynov.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 17.579/18.944/20.309/1.365 ms

```
- une machine du LAN2 peut joindre internet (ping nom de domaine)
```zsh
[root@dns ~]# ping ynov.com

--- ynov.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2359ms
rtt min/avg/max/mdev = 15.478/16.956/19.654/1.910 ms

```
- une machine du LAN1 peut joindre une machine du LAN2 (ping une adresse IP)
```zsh
┌──(kali㉿client1)-[~]
└─$ ping 10.6.2.12

--- 10.6.2.12 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 1.877/2.411/2.754/0.382 ms

```

## II. LAN clients

## 1. Serveur DHCP

```zsh
[root@dhcp oui]# cat /etc/dhcp/dhcpd.conf 
subnet 10.6.1.0 netmask 255.255.255.0 {
	range dynamic-bootp 10.6.1.37 10.6.1.137;
	option broadcast-address 10.6.1.255;
	option routers 10.6.1.254;
	option domain-name-servers 1.1.1.1;
}
```
les commande à realiser
```zsh
dnf -y install dhcp-server 

systemctl enable --now dhcpd 

firewall-cmd --add-service=dhcp 

firewall-cmd --runtime-to-permanent
```

## 2. Client

> *A faire sur `client1.tp6.b1`.*

➜ **Allumez `client1.tp6.b1` et configurez sa carte réseau en DHCP**

- il devrait récupérer automatiquement une adresse IP auprès de votre serveur DHCP
```zsh
┌──(kali㉿client1)-[~]
└─$ ip a

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000

    inet 10.6.1.37/24 brd 10.6.1.255 scope global dynamic noprefixroute eth0
```
- et apprendre l'adresse de la passerelle de ce réseau
```zsh
┌──(kali㉿client1)-[~]
└─$ ip route | grep default

default via 10.6.1.254 dev eth0 proto dhcp src 10.6.1.37 metric 100 
```
- et l'adresse d'un DNS utilisable
```zsh
┌──(kali㉿client1)-[~]
└─$ nmcli -p device show 

IP4.DNS[1]:                             10.6.2.12
```
☀️ **Prouvez que...**

- le client a bien récupéré une adresse IP en DHCP
  - avec un `ip a` le mot-clé `dynamic` doit être écrit sur la ligne qui contient l'adresse IP
```zsh
┌──(kali㉿client1)-[~]
└─$ ip a | grep dynamic
    inet 10.6.1.37/24 brd 10.6.1.255 scope global dynamic noprefixroute eth0
```
- vous avez bien `1.1.1.1` en DNS
```zsh
┌──(kali㉿client1)-[~]
└─$ nmcli -p device show 
============================================================================>
                             Device details (eth0)
============================================================================>
GENERAL.DEVICE:                         eth0
---------------------------------------------------------------------------->
[...]
IP4.DNS[1]:                             1.1.1.1
[...]
```

- vous avez bien la bonne passerelle indiquée
```zsh
┌──(kali㉿client1)-[~]
└─$ ip route | grep default

default via 10.6.1.254 dev eth0 proto dhcp src 10.6.1.37 metric 100 
```
- que ça `ping` un nom de domaine public sans problème magueule
```zsh
┌──(kali㉿client1)-[~]
└─$ ping ynov.com

--- ynov.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 18.716/21.230/23.744/2.514 ms

```

# III. LAN serveurzzzz

## 1. Serveur Web

[**Document dédié au serveur Web**](./web.md)

## 2. Serveur DNS

[**Document dédié au setup serveur DNS**](./dns.md)

## 3. Serveur DHCP

➜ **Editez la configuration du serveur DHCP sur `dhcp.tp6.b1`**

- faut qu'il file l'adresse IP `10.6.2.12` comme DNS à tous les nouveaux clients !
```bash
[root@dhcp oui]# cat /etc/dhcp/dhcpd.conf 
subnet 10.6.1.0 netmask 255.255.255.0 {
	range dynamic-bootp 10.6.1.37 10.6.1.137;
	option broadcast-address 10.6.1.255;
	option routers 10.6.1.254;
	option domain-name-servers 10.6.2.12;
}
```

☀️ **Créez un nouveau client `client2.tp6.b1` vitefé**

- récupérez une IP en DHCP sur ce nouveau `client2.tp6.b1`
```zsh
┌──(kali㉿kali)-[~]
└─$ ip a
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state 
    inet 10.6.1.38/24 brd 10.6.1.255 scope global dynamic noprefixroute
```

- vérifiez que vous avez bien `10.6.2.12` comme serveur DNS à contacter
```zsh
┌──(kali㉿kali)-[~]
└─$ nmcli -p device show
============================================================================>
                             Device details (eth0)
===========================================================================
IP4.DNS[1]:                             10.6.2.12
```

➜ **Vous devriez pouvoir visiter `http://web.tp6.b1` avec le navigateur, ça devrait fonctionner sans aucune autre action.**
```zsh
┌──(kali㉿kali)-[~]
└─$ curl http://web.tp6.b1            
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>HTTP Server Test Page powered by: Rocky Linux</title>
    <style type="text/css">
      /*<![CDATA[*/
```
## 4. Bonus : forger des trames

[Ptit TP bonus orienté dév et sécu](./scapy.md), pour jouer à forger des trames et des paquets à la main. ~~Dans le but de faire des trucs complètement legitimes.~~
