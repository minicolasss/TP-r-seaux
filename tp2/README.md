# TP2 : Hey yo tell a neighbor tell a friend


# Sommaire

- [TP2 : Hey yo tell a neighbor tell a friend](#tp2--hey-yo-tell-a-neighbor-tell-a-friend)
- [Sommaire](#sommaire)
- [I. Simplest LAN](#i-simplest-lan)
  - [1. Quelques pings](#1-quelques-pings)
- [II. Utilisation des ports](#ii-utilisation-des-ports)
- [III. Analyse de vos applications usuelles](#iii-analyse-de-vos-applications-usuelles)
  - [1. Serveur web](#1-serveur-web)
  - [2. Autres services](#2-autres-services)


# I. Simplest LAN


## 1. Quelques pings

🌞 **Prouvez que votre configuration est effective**


```bash
C:\Windows\system32> Get-NetIPAddress -InterfaceAlias "ethernet 3"


IPAddress         : fe80::825f:d4e:e9bf:3afb%16
InterfaceIndex    : 16
InterfaceAlias    : Ethernet 3
AddressFamily     : IPv6
Type              : Unicast
PrefixLength      : 64
PrefixOrigin      : WellKnown
SuffixOrigin      : Link
AddressState      : Preferred
ValidLifetime     :
PreferredLifetime :
SkipAsSource      : False
PolicyStore       : ActiveStore

IPAddress         : 10.234.111.1
InterfaceIndex    : 16
InterfaceAlias    : Ethernet 3
AddressFamily     : IPv4
Type              : Unicast
PrefixLength      : 16
PrefixOrigin      : WellKnown
SuffixOrigin      : Link
AddressState      : Preferred
ValidLifetime     :
PreferredLifetime :
SkipAsSource      : False
PolicyStore       : ActiveStore
```

🌞 **Tester que votre LAN + votre adressage IP est fonctionnel**

- utilise une commande `ping` pour vérifier que tu peux joindre ton collègue branché avec le câble
- vérifiez que ça fonctionne dans les deux sens

```zsh
ping 10.234.111.2

Ping statistics for 10.234.111.2:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 4ms, Maximum = 6ms, Average = 4ms
```

🌞 **Capture de `ping`**

- utilise Wireshark pendant que vous échangez des `ping` dans les deux sens
- livrez une capture `ping.pcap` qui contient uniquement des `ping` entre vos deux PCs

[lien vers ma capture](ping1.pcap)

# II. Utilisation des ports


🌞 **Sur le PC serveur**

- désignez l'un des deux comme serveur, peu importe lequel de vous deux
- utilisez la commande `nc` suivante :

```bash
PS C:\Users\NICOLAS\Desktop\logiciels\netcat-win32-1.11\netcat-1.11> .\nc.exe -l -p 9999
```

🌞 **Sur le PC serveur toujours**

- utiliser une commande pour voir qu'il y a désormais un port en écoute
- on verra que c'est le programme `nc` qui a ouvert le port et qui attend la connexion d'un client
- la commande c'est
  - `netstat -a -b -n` sur Windows (les lignes marquées `LISTENING`)
  - `sudo ss -lnpt` sur Linux
- mettez-moi uniquement la ligne intéressante du résultat dans le rendu
```zsh
PS C:\Windows\system32> netstat -a -n -b

  TCP    0.0.0.0:9999           0.0.0.0:0              LISTENING
 [nc.exe]
```

🌞 **Sur le PC client**

- l'autre, c'est donc le client !
- utilisez la commande `netcat` suivante :

```bash
PS C:\Users\NICOLAS\Desktop\logiciels\netcat-win32-1.11\netcat-1.11> .\nc.exe 10.234.111.2 9999
```


🌞 **Echangez-vous des messages**

- essaie de saisir une phrase/un mot, et appuie sur Entrée
- ton pote devrait voir le message sur son écran
- ça fonctionne dans les deux sens (le serveur peut envoyer des messages au client, et vice-versa)
- vous pouvez désormais vous insulter sans le faire à voix haute, merci :d

```zsh
PS C:\Users\NICOLAS\Desktop\logiciels\netcat-win32-1.11\netcat-1.11> .\nc.exe 10.234.111.2 9999
oui
sedlgdhg
sedefùesf
sf
s
```

🌞 **Utilisez une commande qui permet de voir la connexion en cours**

- **à faire sur le client ET sur le serveur**
- faites-le pendant que la connexion `netcat` est en cours
- isolez la ligne qui concerne la connexion avec `netcat`, ne me mettez pas tout le résultat dans le compte-rendu
- la commande à utiliser c'est :
  - `netstat` sur Windows
  - `ss` sur Linux

```zsh
  TCP    10.234.111.1:52634     10.234.111.2:9999      ESTABLISHED
 [nc.exe]
```

🌞 **Faites une capture Wireshark complète d'un échange**

- la capture doit s'appeler `netcat1.pcap`
  - vous devriez voir vos messages dans l'encart en bas à droite dans Wireshark :D
  - ou en dépliant le volet TCP dans l'encart en bas à gauche
- la capture doit aussi contenir les trois premiers messages échangés entre le client et le serveur à l'établissement de la connexion (3-way handshake)
  - `SYN`
  - `SYN ACK`
  - `ACK`

[lien vers ma capture](netcat1.pcap)

🌞 **Inversez les rôles**

- celui qui avait le rôle du serveur prend le rôle du client, et vice-versa
- allez hop hop, ça devrait pas prendre longtemps la deuxième fois ! :D
- je veux les commandes, le `netstat` ou `ss`, et la capture s'appellera `netcat2.pcap`

```bash
PS C:\Users\NICOLAS\Desktop\logiciels\netcat-win32-1.11\netcat-1.11> .\nc.exe 10.234.111.2 9999
```

[lien vers ma capture](netcat2.pcap)

# III. Analyse de vos applications usuelles



➜ **Connectez-vous à un site en HTTP**


🌞 **Utilisez Wireshark pour capturer du trafic HTTP**

- capture nommée `http.pcap`
- votre requête HTTP, et la réponse HTTP dans la capture
- n'hésitez pas à filtrer le trafic avec un filtre comme `tcp.port == 80` par exemple (puisqu'on sait que par convention, un serveur web écoute sur le port 80)
- capturez aussi le 3-way handshake

[lien vers ma capture](http.pcap)

## 2. Autres services


➜ **Choisissez 5 applications, quelques idées :**

- un navigateur web connecté à un site quelconque
- Steam/un jeu/un launcher
- Spotify/autres
- n'importe quelle application qui a besoin d'internet pour fonctionner en somme !

🌞 **Pour les 5 applications**

- déterminez à quelle adresse IP vous vous connectez
- pour chaque adresse IP, déterminez à quel port vous êtes connecté
- commande `netstat` ou `ss` à l'appui
- capture wireshark à l'appui `service1.pcap`, `service2.pcap`, ..., `service5.pcap`

netstat de discord 

```
  TCP    10.33.76.110:49940     35.186.224.45:443      ESTABLISHED
 [Discord.exe]
```

et voila les package de discord 

[lien veers ma capture](discord.pcap)


ensuite

```
  TCP    10.33.76.110:48183     142.250.201.174:443    ESTABLISHED
 [BsgLauncher.exe]
```

[lien vers ma capture](Bsg.pcap)


la 3eme

```
  TCP    [2a01:e0a:ba4:9e10:ecb8:7aa9:53d3:45e0]:11704  [2620:1ec:bdf::42]:443  ESTABLISHED
 [opera.exe]
 ```

[lien vers ma capture](opera.pcap)


la 4eme

```
  TCP    192.168.0.44:11283     52.123.200.56:443      ESTABLISHED
 [ms-teams.exe]
 ```

[lien vers ma capture](teams.pcap)


et la derniere 

```
  TCP    192.168.0.44:12215     52.182.143.215:443     ESTABLISHED
 [Code.exe]
 ```

[lien vers ma capture](code.pcap)
