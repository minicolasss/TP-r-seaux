# III. Serveur VPN

Dans cette partie on va mettre en place un serveur VPN. On va utiliser *Wireguard* : opensource, moderne, robuste, rapide, le feu.

Le but : on se connecte à un serveur VPN en tant que client (là ce sera une VM le serveur VPN, mais à l'autre bout du monde ça a le même effet).

Une fois connecté au VPN, on accès à :

- **on peut désigner le serveur VPN comme passerelle**
  - ainsi, notre traffic ira jusqu'au serveur VPN avant de sortir sur internet
- **un réseau local, à distance**
  - là il contiendra un serveur Web

![VPN](./img/vpn.png)

## Sommaire

- [III. Serveur VPN](#iii-serveur-vpn)
  - [Sommaire](#sommaire)
  - [0. Setup](#0-setup)
    - [A. Schéma](#a-schéma)
    - [B. Tableau adressage](#b-tableau-adressage)
  - [1. Install et conf Wireguard](#1-install-et-conf-wireguard)
  - [2. Ajout d'un client VPN](#2-ajout-dun-client-vpn)
  - [3. Proofs](#3-proofs)
  - [4. Private service](#4-private-service)

## 0. Setup

### A. Schéma


### B. Tableau adressage

| Machine          | LAN1 `10.7.1.0/24` | LAN2 `10.7.2.0/24` |
|------------------|--------------------|--------------------|
| `client1.tp7.b1` | `10.7.1.101`       | x                  |
| `vpn.tp7.b1`     | `10.7.1.111`       | `10.7.2.111`       |
| `routeur.tp7.b1` | `10.7.1.254`       | x                  |
| `web.tp7.b1`     | x                  | `10.7.2.11`        |

## 1. Install et conf Wireguard


➜ **Installer Wireguard**

```bash
[root@dns wireguard]# sudo dnf install -y epel-release
sudo dnf install -y wireguard-tools
```

➜ **Générer la paire de clés du serveur**

- après cette commande, la clé publique sera stockée dans le fichier `/etc/wireguard/wg0.pub`
- et la clé privée dans `/etc/wireguard/wg0.priv`

```bash
[root@dns wireguard]# wg genkey | sudo tee /etc/wireguard/wg0.priv | wg pubkey | sudo tee /etc/wireguard/wg0.pub
```

➜ **Ecrire le fichier de configuration du serveur**

- créer le fichier `/etc/wireguard/wg0.conf`
```zsh
[root@dns wireguard]# touch wg0.conf
```
  - il faut remplacer `<CLE_PRIVEE_DU_SERVEUR>` par... la clé privée du serveur
  - `sudo cat /etc/wireguard/wg0.priv` pour l'obtenir
```zsh
[root@dns wireguard]# cat wg0.priv 
KNgeHvZcPU62FHtK0jTz/fkbge+ejT1eydU2j5kz21o=
```

```bash
[Interface]
PrivateKey = KNgeHvZcPU62FHtK0jTz/fkbge+ejT1eydU2j5kz21o=
Address = 10.7.200.1/24
ListenPort = 51820
```

➜ **Démarrez l'interface réseau `wg0`**

```bash
[root@dns wireguard]# systemctl start wg-quick@wg0
```

🌞 **Prouvez que vous avez bien une nouvelle carte réseau `wg0`**

- elle doit porter l'adresse IP indiquée dans le fichier de conf
```zsh
[root@dns wireguard]# ip a

5: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.7.200.1/24 scope global wg0
       valid_lft forever preferred_lft forever
```

🌞 **Déterminer sur quel port écoute Wireguard**

- avec une commande adaptée
- isolez la ligne intéressante
```zsh
[root@dns wireguard]# ss -lnpu | grep 51820
UNCONN 0      0            0.0.0.0:51820      0.0.0.0:*                                    
UNCONN 0      0               [::]:51820         [::]:*
```

🌞 **Ouvrez ce port dans le firewall**

```zsh
[root@dns wireguard]# sudo firewall-cmd --permanent --add-port=51820/udp
sudo firewall-cmd --reload
success
success
```
vérification
```zsh
[root@dns wireguard]# sudo firewall-cmd --list-all | grep 51820
  ports: 51820/udp
```

➜ **Enfin, activez le routage avec** :

- oublie pas ça, important pour la suite :d
```zsh
[root@dns wireguard]# sudo firewall-cmd --add-masquerade --permanent
sudo firewall-cmd --reload
success
success
```

```bash
# on active le forwarding : on accepte de faire passer des paquets
[root@dns wireguard]# sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl -w net.ipv6.conf.all.forwarding=1
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1

# on active le masquerading : permettre d'être la passerelle internet des clients
[root@dns wireguard]# sudo firewall-cmd --add-interface=wg0 --zone=public --permanent
sudo firewall-cmd --add-masquerade --permanent
sudo firewall-cmd --reload
success
Warning: ALREADY_ENABLED: masquerade
success
success
```

## 2. Ajout d'un client VPN


➜ **Installer Wireguard**

- allez, je donne pas la commande, demande à google pour savoir comment le faire sur le client !s

➜ **Générer la paire de clés du client**

- même commande que sur le serveur

➜ **Ecrire le fichier de configuration du client**

- créer le fichier `/etc/wireguard/wg0.conf`
  - remplacez les clés par les bonnes valeurs
  - il faut `sudo cat` sur les clés pour les afficher et les insérer
- avec le contenu :

```bash
[Interface]
PrivateKey = <CLE_PRIVEE_DU_CLIENT>
Address = 10.7.200.11/24

[Peer]
PublicKey = <CLE_PUBLIQUE_DU_SERVEUR>
AllowedIPs = 0.0.0.0/0
Endpoint = 10.7.1.111:51820
PersistentKeepalive = 25
```

➜ **Allumer l'interface `wg0` du client**

```bash
sudo wg-quick up wg0
```

---

> *De retour sur le serveur `vpn.tp7.b1`.*

➜ **Modifier le fichier de configuration du serveur**

- on ajoute une section `[Peer]` pour indiquer
  - l'IP du client
  - sa clé publique

```bash
[Interface]
PrivateKey = <CLE_PRIVEE_DU_SERVEUR>
Address = 10.7.200.1/24
ListenPort = 51820


[Peer]
PublicKey = <CLE_PUBLIQUE_DU_CLIENT>
AllowedIps = 10.7.200.11/32
```

➜ **Redémarrer l'interface du serveur après l'ajout du client**

```bash
sudo systemctl restart wg-quick@wg0
```

➜ **Vérifier qu'on voit bien un nouveau client**

```bash
sudo wg show
```

## 3. Proofs

🌞 **Ping ping ping !**

- depuis le client, faites un `ping` vers l'IP du serveur VPN au sein du réseau virtuel
- donc `ping 10.7.200.1`

🌞 **Capture `ping1_vpn.pcap`**

- capturez ces pings
- ne vous attendez pas à vraiment voir directement des pings... vous regardez du trafic VPN

➜ **Sur le `client1.tp7.b1`**

- ajoutez `10.7.200.1` comme votre passerelle, temporairement :

```bash
# on supprime la passerelle actuelle manuellement
sudo ip route delete default

# on ajoute une passerelle qui passe par le serveur VPN
sudo ip route add default via 10.7.200.1
```

🌞 **Prouvez que vous avez toujours un accès internet**

- mais on va pas utiliser `ping`
- vous allez utiliser `traceroute`
- l'avantage, c'est que lui, il affiche tous les intermédiaires entre vous et la destination
- `traceroute 1.1.1.1` dans le compte-rendu

> On devrait voir que pour aller sur internet, vous passez par le serveur VPN.

## 4. Private service

> *Sur `web.tp7.b1`.*

Last but not least, le serveur Web. Il est isolé dans un LAN (potentiellement à l'autre bout du monde), impossible d'y accéder... sauf si on est connectés au VPN.

Pour ce faire :

- recycler la machine web de la partie d'avant
- branchez-le au nouveau host-only
- attribuez-lui la nouvelle IP `10.7.2.11`
- installer wireguard, et ajouter la machine comme nouveau client (même manip que sur `client1.tp7.b1`)
  - l'IP de `web.tp7.b1` doit être `10.7.200.37`
- modifier la configuration NGINX pour qu'il écoute uniquement sur l'IP `10.7.200.37`

🌞 **Visitez le service Web à travers le VPN**

- site web privé accessible uniquement à ceux qui sont connectés au VPN
- `curl https://https://sitedefou.tp7.b1` en ayant modifié votre fichier hosts pour que pointe vers `10.7.200.37`

Et on a donc *virtuellement* obtenu ce réseau LAN :

![VPN be like](./img/vpn.svg)
