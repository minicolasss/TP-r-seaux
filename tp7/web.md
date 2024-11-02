# Serveur Web

- [Serveur Web](#serveur-web)
  - [0. Setup](#0-setup)
    - [A. Schéma](#a-schéma)
    - [B. Tableau adressage](#b-tableau-adressage)
  - [1. HTTP](#1-http)
    - [A. Install](#a-install)
    - [B. Configuration](#b-configuration)
    - [C. Tests client](#c-tests-client)
    - [D. Analyze](#d-analyze)
  - [2. On rajoute un S](#2-on-rajoute-un-s)
    - [A. Config](#a-config)
    - [B. Test test test analyyyze](#b-test-test-test-analyyyze)

## 0. Setup

### A. Schéma

### B. Tableau adressage

| Machine          | LAN1 `10.7.1.0/24` |
|------------------|--------------------|
| `client1.tp7.b1` | `10.7.1.101`       |
| `web.tp7.b1`     | `10.7.1.11`        |
| `routeur.tp7.b1` | `10.7.1.254`       |

## 1. HTTP

### A. Install

➜ **Installer le service NGINX**

```zsh
[root@web oui]# dnf install -y nginx
```

### B. Configuration

➜ **Créer un fichier de configuration pour un nouveau site web**

- créer un fichier dans le dossier `/etc/nginx/conf.d/` qui a l'extension `.conf`
```zsh
[root@web sitedefou]# ls /etc/nginx/conf.d/
sitedefou.conf
```
- on va créer `/etc/nginx/conf.d/sitedefou.tp7.b1.conf`
- avec le contenu suivant (remplacez `<ADRESSE_IP>` par l'adresse IP du serveur web)

```zsh
[root@web sitedefou]# cat /etc/nginx/conf.d/sitedefou.conf 
server {
    # le nom que devront taper les clients pour visiter le site
    server_name   sitedefou.tp7.b1;

    # on indique sur quelle adresse IP et quel port écouter
    listen        10.7.1.11:80;

    location      / {
        # "root" pour "racine" : l'emplacement de la racine web
        # c'est à dire le dossier qui contient le site web
        root      /var/www/sitedefou.tp7.b1;
    }
}
```

➜ **Créer un nouveau site web :d**

```bash
[root@web conf.d]# mkdir -p /var/www/sitedefou

[root@web www]# echo "meow !" | sudo tee /var/www/sitedefou/index.html
meow !

[root@web conf.d]# chown nginx:nginx -R /var/www/sitedefou
```

➜ **On démarre le service web NGINX**

```bash
[root@web conf.d]# systemctl start nginx
```

🌞 **Lister les ports en écoute sur la machine**

- avec une commande adaptée (voir mémo)
- isolez la ligne qui concerne le service NGINX
```zsh
[root@web sitedefou]# ss -lnmp | grep nginx
tcp   LISTEN 0      511                                       0.0.0.0:80               0.0.0.0:*    users:(("nginx",pid=1713,fd=6),("nginx",pid=1712,fd=6),("nginx",pid=1711,fd=6))
tcp   LISTEN 0      511                                          [::]:80                  [::]:*    users:(("nginx",pid=1713,fd=7),("nginx",pid=1712,fd=7),("nginx",pid=1711,fd=7))
```

🌞 **Ouvrir le port dans le firewall de la machine**

```zsh
[root@web sitedefou]# firewall-cmd --permanent --add-port=80/tcp
success
[root@web sitedefou]# firewall-cmd --reload
success
[root@web sitedefou]# sudo firewall-cmd --list-all | grep 80
  ports: 80/tcp
```

### C. Tests client

➜ **Ajoutez la ligne suivante au fichier `/etc/hosts`**

```zsh
┌──(kali㉿kali)-[~]
└─$ cat /etc/hosts
...
10.7.1.11 sitedefou.tp7.b1
```

🌞 **Vérifier que ça a pris effet**

- faites un `ping` vers `sitedefou.tp7.b1`
```zsh
┌──(kali㉿kali)-[~]
└─$ ping sitedefou.tp7.b1

--- sitedefou.tp7.b1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 1.507/1.577/1.647/0.070 ms
```
- visitez `http://sitedefou.tp7.b1`
```zsh
┌──(kali㉿kali)-[~]
└─$ curl http://sitedefou.tp7.b1
meow !
```
- **vous devriez avoir la page "meow !" quand vous visitez le site**

### D. Analyze

🌞 **Capture `tcp_http.pcap`**

- **capturer une session TCP complète**

[lien vers ma capture](./tcp_http.pcap)

🌞 **Voir la connexion établie**

- utilisez une commande `ss` sur le client pour voir le tunnel TCP établi
- il faut taper la commande au moment où vous visitez le site web (ou juste après :d)

Dans un premier temps j'ouvre le site web dans mon navigateur

et ensuite : 
```zsh
┌──(kali㉿kali)-[~]
└─$ ss -pnt                                          
State    Recv-Q    Send-Q         Local Address:Port            Peer Address:Port    Process                                                                              
ESTAB    0         0                 10.7.1.102:45048          34.107.243.93:443      users:(("firefox-esr",pid=23825,fd=111))                                            
ESTAB    0         0                 10.7.1.102:43264         34.149.100.209:443      users:(("firefox-esr",pid=23825,fd=119))                                            
ESTAB    0         0                 10.7.1.102:48534          172.217.19.35:80       users:(("firefox-esr",pid=23825,fd=117))                                            
ESTAB    0         0                 10.7.1.102:48526          172.217.19.35:80       users:(("firefox-esr",pid=23825,fd=91))                                             
ESTAB    0         0                 10.7.1.102:58648         34.117.188.166:443      users:(("firefox-esr",pid=23825,fd=107))                                            
ESTAB    0         0                 10.7.1.102:57574           2.16.149.148:80       users:(("firefox-esr",pid=23825,fd=102))                                            
ESTAB    0         0                 10.7.1.102:45036          34.107.243.93:443      users:(("firefox-esr",pid=23825,fd=115))                                            
ESTAB    0         0                 10.7.1.102:58634         34.117.188.166:443      users:(("firefox-esr",pid=23825,fd=82)) 
```

## 2. On rajoute un S

### A. Config

> *Sur `web.tp7.b1`.*

➜ **Générer une paire de clé pour le chiffrement**

- l'une des deux sera stocké dans un certificat
- suivez juste le guide :d

```bash
# générer une paire de clé
[root@web ~]# openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout server.key -out server.crt

# il existe sur tous les OS destinés à stocker des clés de chiffrement
[root@web ssl]# mkdir private
[root@web ssl]# ls
cert.pem  certs  ct_log_list.cnf  openssl.cnf  private
[root@web ~]# mv server.key /etc/ssl/private/sitedefou.tp7.b1.key

# idem pour le certificat (qui contient la clé publique)
[root@web ~]# mv server.crt /etc/ssl/certs/sitedefou.tp7.b1.crt

# gestion des permissions
[root@web ~]# sudo chown nginx:nginx /etc/ssl/private/sitedefou.tp7.b1.key
sudo chown nginx:nginx /etc/ssl/certs/sitedefou.tp7.b1.crt
```

![One lock](./img/one_lock.jpg)

➜ **Modifier la configuration NGINX**

- go modifier votre fichier `/etc/nginx/conf.d/sitedefou.tp7.b1.conf`

```nginx
[root@web ~]# cat /etc/nginx/conf.d/sitedefou.conf 
server {
    # le nom que devront taper les clients pour visiter le site
    server_name   sitedefou.tp7.b1;

    # on indique sur quelle adresse IP et quel port écouter
    listen        10.7.1.11:443 ssl;

    ssl_certificate /etc/ssl/certs/sitedefou.tp7.b1.crt;
    ssl_certificate_key /etc/ssl/private/sitedefou.tp7.b1.key;

    location      / {
        # "root" pour "racine" : l'emplacement de la racine web
        # c'est à dire le dossier qui contient le site web
        root      /var/www/sitedefou;
    }
}
```

➜ **Redémarrer le service web NGINX !**

```bash
sudo systemctl restart nginx
```

### B. Test test test analyyyze


➜ **Tu devrais pouvoir visiter `https://sitedefou.tp7.b1` (bien `https` avec le 's')**

🌞 **Capture `tcp_https.pcap`**

[lien vers ma capture](./tcp_https.pcap)

- **capturer une session TCP complète**
  - le début (SYN, SYN ACK, ACK)
  - des données échangées (PSH, PSH ACK)
    - en l'occurence ce sera votre échange TLS
      - Wireshark affichera "TLS" dans la colonne protocole, mais si vous cliquez dessus, vous verrez que c'est bien contenu dans du TCP PSH
    - puis les données HTTP... chiffrées
  - une fin de session (ça dépend, le plus souvent : FIN, FIN ACK ou RST)
- cette session TCP doit être celle de l'échange HTTPS pour récupérer la page du serveur web
- il faut donc capturer pendant que tu visites le site web en HTTPS


