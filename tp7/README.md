# TP7 : On dit chiffrer pas crypter


## Sommaire

- [TP7 : On dit chiffrer pas crypter](#tp7--on-dit-chiffrer-pas-crypter)
  - [Sommaire](#sommaire)
  - [I. Setup](#i-setup)
  - [II. Serveur Web](#ii-serveur-web)
  - [III. Serveur VPN](#iii-serveur-vpn)


# I. Setup

➜ Pour chaque machine

- donnez une IP statique
- pour l'accès internet
  - activer le routage sur le routeur
  - carte NAT sur le routeur
  - définir le routeur comme passerelle pour les autres
  - aussi, n'oubliez pas d'indiquer `1.1.1.1` en serveur DNS partout
- nommez vos machines (configuration du hostname)

le routeur :
```zsh
[root@routeur dhcp]# cat /etc/sysconfig/network-scripts/ifcfg-enp0s8 
DEVICE=enp0s8
NAME=lan


ONBOOT=yes


IPADDR=10.7.1.254
NETMASK=255.255.255.0
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
PREFIX=24
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=no
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
UUID=00cb8299-feb9-55b6-a378-3fdc720e0bc6
ZONE=public
```
j'ai aussi fait un DHCP dessus pour le fun :
```zsh
[root@routeur dhcp]# cat dhcpd.conf 
option domain-name-servers     1.1.1.1; 

subnet 10.7.1.0 netmask 255.255.255.0 {
    # specify the range of lease IP address
    range dynamic-bootp 10.7.1.100 10.7.1.200;
    # specify broadcast address
    option broadcast-address 10.7.1.255;
    # specify gateway
    option routers 10.7.1.254;
}
```  
le serveur wer
```zsh
[root@web oui]# cat /etc/sysconfig/network-scripts/ifcfg-enp0s3 
DEVICE=enp0s3
NAME=lan


ONBOOT=yes
BOOTPROTO=static


IPADDR=10.7.1.11
NETMASK=255.255.255.0
GATEWAY=10.7.1.254
DNS1=1.1.1.1
```
et enfin le serveur vpn :
```zsh
[root@dns oui]# cat /etc/sysconfig/network-scripts/ifcfg-enp0s3 
DEVICE=enp0s3
NAME=lan


ONBOOT=yes
BOOTPROTO=static


IPADDR=10.7.1.12
NETMASK=255.255.255.0
GATEWAY=10.7.1.254
DNS1=1.1.1.1
```
# II. Serveur Web

[Document dédié à la partie II. Serveur Web.](./web.md)

# III. Serveur VPN

[Document dédié à la partie III. Serveur VPN](./vpn.md)
