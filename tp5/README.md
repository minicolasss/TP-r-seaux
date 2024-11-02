# TP5 : Un ptit LAN à nous

## Sommaire

- [TP5 : Un ptit LAN à nous](#tp5--un-ptit-lan-à-nous)
  - [Sommaire](#sommaire)
- [I. Setup](#i-setup)
- [II. Accès internet pour tous](#ii-accès-internet-pour-tous)
  - [1. Accès internet routeur](#1-accès-internet-routeur)
  - [2. Accès internet clients](#2-accès-internet-clients)
- [III. Serveur SSH](#iii-serveur-ssh)
- [IV. Serveur DHCP](#iv-serveur-dhcp)

  - [3. Rendu attendu](#3-rendu-attendu)
    - [A. Installation et configuration du serveur DHCP](#a-installation-et-configuration-du-serveur-dhcp)
    - [B. Test avec un nouveau client](#b-test-avec-un-nouveau-client)
    - [C. Consulter le bail DHCP](#c-consulter-le-bail-dhcp)
- [Bonus](#bonus)



# I. Setup

➜ **Ptit tableau avec les adresses IP**

| Nom de la machine | IP dans le LAN `10.5.1.0/24` |
|-------------------|------------------------------|
| Votre PC          | `10.5.1.1`                   |
| `client1.tp5.b1`  | `10.5.1.11`                  |
| `client2.tp5.b1`  | `10.5.1.12`                  |
| `routeur.tp5.b1`  | `10.5.1.254`                 |


➜ **Il faut donc, sur votre PC :**

- créer un host-only (réseau privé-hôte en français)
- définir l'IP `10.5.1.1/24` pour le PC depuis l'interface de VBox
```zsh
5: vboxnet1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether 0a:00:27:00:00:01 brd ff:ff:ff:ff:ff:ff
    inet 10.5.1.1/24 brd 10.5.1.255 scope global vboxnet1
       valid_lft forever preferred_lft forever
```

➜ **Ensuite, pour chaque VM...**

- **configurer l'adresse IP demandée**
  - ça se fait depuis la VM directement : chaque client choisit sa propre IP comme toujours !
  - mettez l'IP indiquée dans le tableau, et le même masque pour tout le monde
```zsh
le routeur


[root@vbox oui]# ip a

2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000

    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s3

3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000

    inet 10.5.1.254/24 brd 10.5.1.255 scope global noprefixroute enp0s8



client1

┌──(oui㉿oui)-[~]
└─$ ip a

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000

    inet 10.5.1.11/24 brd 10.5.1.255 scope global noprefixroute eth0




client2

┌──(oui㉿oui)-[~]
└─$ ip a

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000

    inet 10.5.1.12/24 brd 10.5.1.255 scope global noprefixroute eth0
```


- **configurer un *hostname* pour la VM**
  - comme ça, quand on est dans un terminal, le nom de la machin est affiché, et on sait où on est !
  - c'est affiché dans le prompt dans votre terminal : `[it4@localhost]$`
  - le nom par défaut c'est `localhost` et c'est pourri !

```zsh

[oui@routeur ~]$ hostname
routeur.tp5.b1

┌──(oui㉿client1)-[~]
└─$ hostname                  
client1.tp5.b1

┌──(oui㉿client2)-[~]
└─$ hostname
client2.tp5.b1
```

☀️ **Uniquement avec des commandes, prouvez-que :**

- vous avez bien configuré les adresses IP demandées (un `ip a` suffit hein)
```zsh
[oui@routeur ~]$ ip a

2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000

    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s3

3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000

    inet 10.5.1.254/24 brd 10.5.1.255 scope global noprefixroute enp0s8



┌──(oui㉿client1)-[~]
└─$ ip a

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000

    inet 10.5.1.11/24 brd 10.5.1.255 scope global noprefixroute eth0



┌──(oui㉿client2)-[~]
└─$ ip a

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000

    inet 10.5.1.12/24 brd 10.5.1.255 scope global noprefixroute eth0

```
- vous avez bien configuré les *hostnames* demandés

```zsh

[oui@routeur ~]$ hostname
routeur.tp5.b1

┌──(oui㉿client1)-[~]
└─$ hostname                  
client1.tp5.b1

┌──(oui㉿client2)-[~]
└─$ hostname
client2.tp5.b1
```
- tout le monde peut se ping au sein du réseau `10.5.1.0/24`
```zsh
[oui@routeur ~]$ ping 10.5.1.11

--- 10.5.1.11 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2069ms
rtt min/avg/max/mdev = 0.614/1.010/1.368/0.309 ms
[oui@routeur ~]$ ping 10.5.1.12

--- 10.5.1.12 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1003ms
rtt min/avg/max/mdev = 1.267/1.582/1.898/0.315 ms


┌──(oui㉿client2)-[~]
└─$ ping 10.5.1.254

--- 10.5.1.254 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1012ms
rtt min/avg/max/mdev = 1.107/1.250/1.393/0.143 ms

```

# II. Accès internet pour tous

➜ **Actuellement, tout le monde est connecté, mais les clients n'ont pas internet !**

Pour ça :

- il faut que notre machine `routeur.tp5.b1` accepte de router des paquets
- il faut que chaque client
  - connaisse `routeur.tp.b1` comme sa passerelle (`10.5.1.254`)
  - connaisse l'adresse d'un serveur DNS (pour résoudre des noms comme `www.ynov.com` afin de connaître l'adresse IP associée à ce nom)

## 1. Accès internet routeur


☀️ **Déjà, prouvez que le routeur a un accès internet**

- une seule commande `ping` suffit à prouver ça, vers un nom de domaine que vous connaissez, genre `www.ynov.com` (ou autre de votre choix :d)
```zsh
[oui@routeur ~]$ ping ynov.com

--- ynov.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2005ms
rtt min/avg/max/mdev = 13.367/15.290/16.748/1.419 ms
```
☀️ **Activez le routage**

- toujours sur `routeur.tp5.b1`
- la commande est dans le mémo toujours !

```zsh
[root@routeur oui]# sudo firewall-cmd --add-masquerade --permanent
sudo firewall-cmd --reload
Warning: ALREADY_ENABLED: masquerade
success
success

```
## 2. Accès internet clients

➜ **Définir l'adresse IP du routeur comme passerelle pour les clients**

- il sera peut-être nécessaire de redémarrer l'interface réseau pour que ça prenne effet

➜ **Vérifier que les clients ont un accès internet**

- avec un `ping` vers une adresse IP publique vous connaissez
- à ce stade, vos clients ne peuvent toujours pas résoudre des noms, donc impossible de visiter un site comme `www.ynov.com`
```zsh
┌──(oui㉿client1)-[~]
└─$ ping 1.1.1.1

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 15.716/17.859/20.002/2.143 ms

┌──(oui㉿client2)-[~]
└─$ ping 1.1.1.1

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 16.197/16.585/16.973/0.388 ms
```


➜ **Définir `1.1.1.1` comme serveur DNS que peuvent utiliser les clients**

- redémarrez l'interface réseau si nécessaire pour que ça prenne effet
- ainsi vos clients pourront spontanément envoyer des requêtes DNS vers `1.1.1.1` afin d'apprendre à quelle IP correspond un nom de domaine donné

☀️ **Prouvez que les clients ont un accès internet**

- avec de la résolution de noms cette fois
- une seule commande `ping` suffit
```zsh
┌──(oui㉿client1)-[~]
└─$ ping ynov.com 

--- ynov.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2001ms
rtt min/avg/max/mdev = 16.053/18.557/23.434/3.448 ms


┌──(oui㉿client2)-[~]
└─$ ping ynov.com

--- ynov.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 16.787/16.903/17.019/0.116 ms
```

☀️ **Montrez-moi le contenu final du fichier de configuration de l'interface réseau**

- celui de `client2.tp5.b1` me suffira
- pour le compte-rendu, une simple commande `cat` pour afficher le contenu du fichier

```zsh
┌──(oui㉿client1)-[~]
└─$ cat /etc/netplan/01-netcfg.yaml     
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: no
      addresses: [10.5.1.12/24]
      gateway4: 10.5.1.254
      nameservers:
        addresses: [1.1.1.1]
```

# III. Serveur SSH


☀️ **Sur `routeur.tp5.b1`, déterminer sur quel port écoute le serveur SSH**

- pour le serveur SSH, le nom du programme c'est `sshd`
  - il écoute sur un port TCP
- dans le compte rendu je veux que vous utilisiez une syntaxe avec `... | grep <PORT>` pour isoler la ligne avec le port intéressant
  - par exemple si, vous repérez le port 8888, vous ajoutez ` | grep 8888` à votre commande, pour me mettre en évidence le por que vous avez repéré

```zsh
[root@routeur oui]# ss -lnpt | grep 22
LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=734,fd=3))
LISTEN 0      128             [::]:22           [::]:*    users:(("sshd",pid=734,fd=4))
```

☀️ **Sur `routeur.tp5.b1`, vérifier que ce port est bien ouvert**

- la commande est dans [le mémooooo](../../cours/memo/rocky.md) pour voir la configuration du pare-feu

```zsh
[root@routeur oui]# firewall-cmd --list-all | grep 22
  ports: 22/tcp
```
# IV. Serveur DHCP

### A. Installation et configuration du serveur DHCP

```zsh
[root@routeur oui]# dnf -y install dhcp-server

[root@routeur oui]# vim /etc/dhcp/dhcpd.conf 

[root@routeur oui]# cat /etc/dhcp/dhcpd.conf 
subnet 10.5.1.0 netmask 255.255.255.0 {
	range dynamic-bootp 10.5.1.137 10.5.1.237;
	option broadcast-address 10.5.1.255;
	option routers 10.5.1.254;
	option domain-name-servers 1.1.1.1;
}

[root@routeur oui]# systemctl enable --now dhcpd
[root@routeur oui]# firewall-cmd --add-service=dhcp
success
[root@routeur oui]# firewall-cmd --runtime-to-permanent
success
```

☀️ **Installez et configurez un serveur DHCP sur la machine `routeur.tp5.b1`**

- je veux toutes les commandes réalisées
- et le contenu du fichier de configuration
- le fichier de configuration doit :
  - indiquer qu'on propose aux clients des adresses IP entre `10.5.1.137` et `10.5.1.237`
  - indiquer aux clients que la passerelle dans le réseau ici c'est `10.5.1.254`
  - indiquer aux clients qu'un serveur DNS joignable depuis le réseau c'est `1.1.1.1`

```zsh
[root@routeur oui]# dnf -y install dhcp-server

[root@routeur oui]# vim /etc/dhcp/dhcpd.conf 

[root@routeur oui]# cat /etc/dhcp/dhcpd.conf 
subnet 10.5.1.0 netmask 255.255.255.0 {
	range dynamic-bootp 10.5.1.137 10.5.1.237;
	option broadcast-address 10.5.1.255;
	option routers 10.5.1.254;
	option domain-name-servers 1.1.1.1;
}

[root@routeur oui]# systemctl enable --now dhcpd
[root@routeur oui]# firewall-cmd --add-service=dhcp
success
[root@routeur oui]# firewall-cmd --runtime-to-permanent
success
```

### B. Test avec un nouveau client

> *Cette section B. est à réaliser sur une nouvelle machine Ubuntu fraîchement clonée : `client3.tp5.b1`. Vous pouvez éteindre `client1.tp5.b1` et `client2.tp5.b1` pour économiser des ressources.*

☀️ **Créez une nouvelle machine client `client3.tp5.b1`**

- définissez son *hostname*
- définissez une IP en DHCP
- vérifiez que c'est bien une adresse IP entre `.137` et `.237`
- prouvez qu'il a immédiatement un accès internet

```zsh
┌──(oui㉿client1)-[~]
└─$ ip a

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000

    inet 10.5.1.137/24 brd 10.5.1.255 scope global dynamic noprefixroute eth0
```
### C. Consulter le bail DHCP

➜ **Côté serveur DHCP, à chaque fois qu'une adresse IP est proposée à quelqu'un, le serveur crée un fichier texte appelé *bail DHCP*** (ou *DHCP lease* en anglais).

Il contient toutes les informations liées à l'échange avec le client, notamment :

- adresse MAC du client qui a demandé l'IP
- adresse IP proposée au client
- heure et date précises de l'échange DHCP
- durée de validité du *bail DHCP*

☀️ **Consultez le *bail DHCP* qui a été créé pour notre client**

- à faire sur `routeur.tp5.b1`
- toutes les données du serveur DHCP, comme les *baux DHCP*, sont stockés dans le dossier `/var/lib/dhcpd/`
- afficher le contenu du fichier qui contient les *baux DHCP*
- on devrait y voir l'IP qui a été proposée au client, ainsi que son adresse MAC

```zsh
[root@routeur oui]# cat /var/lib/dhcpd/dhcpd.leases 
authoring-byte-order little-endian;

server-duid "\000\001\000\001.\270\333\321\010\000'A\203,";

lease 10.5.1.137 {
  starts 6 2024/11/02 12:47:22;
  ends 0 2024/11/03 00:47:22;
  cltt 6 2024/11/02 12:47:22;
  binding state active;
  next binding state free;
  rewind binding state free;
  hardware ethernet 08:00:27:58:a8:58;
  uid "\001\010\000'X\250X";
  client-hostname "client1";
}
lease 10.5.1.138 {
  starts 6 2024/11/02 12:47:37;
  ends 0 2024/11/03 00:47:37;
  cltt 6 2024/11/02 12:47:37;
  binding state active;
  next binding state free;
  rewind binding state free;
  hardware ethernet 08:00:27:d8:78:0d;
  uid "\001\010\000'\330x\015";
  client-hostname "client2";
}
```
☀️ **Confirmez qu'il s'agit bien de la bonne adresse MAC**

- à faire sur `client3.tp5.b1`
- consultez l'adresse MAC du client
- on peut consulter les adresses MAC des cartes réseau avec un simple `ip a` 

```zsh                                                                         
┌──(oui㉿client1)-[~]
└─$ ip a

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:58:a8:58 brd ff:ff:ff:ff:ff:ff
    inet 10.5.1.137/24 brd 10.5.1.255 scope global dynamic noprefixroute eth0

```
# Bonus

Deux ptits TP bonus, qui font écho à tout ce qu'on a vu jusqu'à maintenant :

- [DHCP spoofing](./dhcp_spoof.md)
- [Protection face à un bruteforce/flood](./flood_protect.md)
