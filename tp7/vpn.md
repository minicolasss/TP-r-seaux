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

```zsh
┌──(oui㉿oui)-[~]
└─$ sudo apt install wireguard
```

➜ **Générer la paire de clés du client**

```zsh
┌──(oui㉿oui)-[~]
└─$ wg genkey | sudo tee /etc/wireguard/wg0.priv | wg pubkey | sudo tee /etc/wireguard/wg0.pub

4pYiU8qjoLR2B2QlKzTfpJfTy7/RmfJY5MctvEjZUxQ=
```

```zsh
┌──(oui㉿oui)-[~]
└─$ sudo cat /etc/wireguard/wg0.priv
[sudo] password for oui: 
eGphtM6W+EBIwavVk4gZHtFvHH8u8zF9uJYfvqQg6nI=
                                                                             
┌──(oui㉿oui)-[~]
└─$ sudo cat /etc/wireguard/wg0.pub 
4pYiU8qjoLR2B2QlKzTfpJfTy7/RmfJY5MctvEjZUxQ=
```

➜ **Ecrire le fichier de configuration du client**


```bash
┌──(oui㉿oui)-[~]
└─$ sudo cat /etc/wireguard/wg0.conf
[Interface]
PrivateKey = eGphtM6W+EBIwavVk4gZHtFvHH8u8zF9uJYfvqQg6nI=
Address = 10.7.200.11/24

[Peer]
PublicKey = XvFnMbp/P2vYWYjER44EXv85MXb6gJLBz2ntNZT4P3I=
AllowedIPs = 0.0.0.0/0
Endpoint = 10.7.1.111:51820
PersistentKeepalive = 25
```

➜ **Allumer l'interface `wg0` du client**

```bash
┌──(oui㉿oui)-[~]
└─$ sudo wg-quick up wg0
```

---


➜ **Modifier le fichier de configuration du serveur**


```bash
[root@dns oui]# cat /etc/wireguard/wg0.conf 
[Interface]
PrivateKey = KNgeHvZcPU62FHtK0jTz/fkbge+ejT1eydU2j5kz21o=
Address = 10.7.200.1/24
ListenPort = 51820


[Peer]
PublicKey = 4pYiU8qjoLR2B2QlKzTfpJfTy7/RmfJY5MctvEjZUxQ=
AllowedIps = 10.7.200.11/32
```

➜ **Redémarrer l'interface du serveur après l'ajout du client**

```bash
[root@dns oui]# sudo systemctl restart wg-quick@wg0
```

➜ **Vérifier qu'on voit bien un nouveau client**

```bash
[root@dns oui]# sudo wg show
interface: wg0
  public key: XvFnMbp/P2vYWYjER44EXv85MXb6gJLBz2ntNZT4P3I=
  private key: (hidden)
  listening port: 51820

peer: 4pYiU8qjoLR2B2QlKzTfpJfTy7/RmfJY5MctvEjZUxQ=
  endpoint: 10.7.1.172:36950
  allowed ips: 10.7.200.11/32
  latest handshake: 30 seconds ago
  transfer: 212 B received, 92 B sent
```

## 3. Proofs

🌞 **Ping ping ping !**

```zsh
┌──(oui㉿oui)-[~]
└─$ ping 10.7.200.1
PING 10.7.200.1 (10.7.200.1) 56(84) bytes of data.

--- 10.7.200.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 1.662/2.101/2.540/0.439 ms
```

🌞 **Capture `ping1_vpn.pcap`**

[lien vers ma Capture](./ping1_vpn.pcap)

➜ **Sur le `client1.tp7.b1`**


```bash
┌──(oui㉿oui)-[~]
└─$ sudo ip route delete default


┌──(oui㉿oui)-[~]
└─$ sudo ip route add default via 10.7.200.1
```

🌞 **Prouvez que vous avez toujours un accès internet**

```zsh
┌──(oui㉿oui)-[~]
└─$ traceroute 1.1.1.1
traceroute to 1.1.1.1 (1.1.1.1), 30 hops max, 60 byte packets


 1  10.7.200.1 (10.7.200.1)  1.395 ms  1.357 ms  1.327 ms  // "Cette ligne-là nous montre qu'on passe par le VPN"


 2  * * *
 3  10.0.2.2 (10.0.2.2)  2.573 ms  2.565 ms  2.550 ms
 4  192.168.0.254 (192.168.0.254)  7.000 ms  6.990 ms  6.965 ms
 5  * * *
 6  station3.multimania.isdnet.net (194.149.174.100)  18.480 ms *  15.697 ms
 7  prs-b3-link.ip.twelve99.net (62.115.46.68)  16.620 ms  15.597 ms  15.584 ms
 8  cloudflare-ic-382666.ip.twelve99-cust.net (213.248.75.93)  16.415 ms  26.158 ms  26.304 ms
 9  141.101.67.79 (141.101.67.79)  16.385 ms 141.101.67.83 (141.101.67.83)  22.333 ms 141.101.67.54 (141.101.67.54)  16.072 ms
10  one.one.one.one (1.1.1.1)  15.992 ms  16.303 ms  16.625 ms
```

## 4. Private service

Pour ce faire :

- branchez-le au nouveau host-only
- attribuez-lui la nouvelle IP `10.7.2.11`
```zsh
[root@web oui]# ip a
...
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:87:29:0a brd ff:ff:ff:ff:ff:ff
    inet 10.7.2.11/24 brd 10.7.2.255 scope global noprefixroute enp0s3
...
```
- installer wireguard, et ajouter la machine comme nouveau client (même manip que sur `client1.tp7.b1`)
```zsh
[root@web oui]# sudo dnf install -y epel-release
sudo dnf install -y wireguard-tools


[root@web oui]# wg genkey | sudo tee /etc/wireguard/wg0.priv | wg pubkey | sudo tee /etc/wireguard/wg0.pub
pQA60jKo4RmhH5c1oNrBk97Bho18BpyuQlrBeu7wV00=




[root@web oui]# cat /etc/wireguard/wg0.conf
[Interface]
PrivateKey = oGbDyC/fId/hWYxOETGNVvB3rMsSBv1aE5nl7lACgVo=
Address = 10.7.200.11/24

[Peer]
PublicKey = XvFnMbp/P2vYWYjER44EXv85MXb6gJLBz2ntNZT4P3I=
AllowedIPs = 0.0.0.0/0
Endpoint = 10.7.1.111:51820
PersistentKeepalive = 25



[root@web oui]# sudo wg-quick up wg0
```
  - l'IP de `web.tp7.b1` doit être `10.7.200.37`
  ```zsh
  [root@web oui]# ip a
...
3: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.7.200.11/24 scope global wg0
       valid_lft forever preferred_lft forever
```

et sur le serveur
```zsh
[root@dns oui]# cat /etc/wireguard/wg0.conf 
...
[Peer]
PublicKey = pQA60jKo4RmhH5c1oNrBk97Bho18BpyuQlrBeu7wV00=
AllowedIps = 10.7.200.11/32
```

```zsh
[root@web oui]# traceroute 1.1.1.1
traceroute to 1.1.1.1 (1.1.1.1), 30 hops max, 60 byte packets
 1  10.7.200.1 (10.7.200.1)  1.968 ms  1.828 ms  1.785 ms
...
```
- modifier la configuration NGINX pour qu'il écoute uniquement sur l'IP `10.7.200.37`
```zsh
[root@web oui]# cat /etc/nginx/conf.d/sitedefou.conf 
server {
    # le nom que devront taper les clients pour visiter le site
    server_name   sitedefou.tp7.b1;

    # on indique sur quelle adresse IP et quel port écouter
    listen        10.7.200.37:443 ssl;
...
```

🌞 **Visitez le service Web à travers le VPN**

- site web privé accessible uniquement à ceux qui sont connectés au VPN
- `curl https://https://sitedefou.tp7.b1` en ayant modifié votre fichier hosts pour que pointe vers `10.7.200.37`
```zsh
┌──(oui㉿oui)-[~]
└─$ curl -k https://sitedefou.tp7.b1

meow !
```
