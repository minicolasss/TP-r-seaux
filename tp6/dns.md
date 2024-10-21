# III. 2. Serveur DNS

- [III. 2. Serveur DNS](#iii-2-serveur-dns)
  - [1. Présentation serveur DNS](#1-présentation-serveur-dns)
  - [2. Dans notre TP](#2-dans-notre-tp)
  - [3. Zé bardi](#3-zé-bardi)
  - [4. Analyse du service](#4-analyse-du-service)
  - [5. Tests manuels](#5-tests-manuels)

## 1. Présentation serveur DNS

➜ **Un *serveur DNS* est une machine sur laquelle s'exécute un programme qu'on appelle *service DNS*.**

Un *service DNS* écoute sur un port, et attend la connexion de clients.

> Par convention, les services DNS écoutent sur les ports 53/tcp et 53/udp.

```bash
[root@dns oui]# ss -lntp
State    Recv-Q   Send-Q     Local Address:Port     Peer Address:Port   Process                                                                                                      
LISTEN   0        10             127.0.0.1:53            0.0.0.0:*       users:(("named",pid=754,fd=34))                                        
LISTEN   0        10             127.0.0.1:53            0.0.0.0:*       users:(("named",pid=754,fd=35))                                        
LISTEN   0        10             10.6.2.12:53            0.0.0.0:*       users:(("named",pid=754,fd=44))                                        
LISTEN   0        10             10.6.2.12:53            0.0.0.0:*       users:(("named",pid=754,fd=45))                                                                          
LISTEN   0        10                 [::1]:53               [::]:*       users:(("named",pid=754,fd=40))                                        
LISTEN   0        10                 [::1]:53               [::]:*       users:(("named",pid=754,fd=41))                                        
```


## 2. Dans notre TP

Notre serveur DNS répondra aux autres VMs du LAN (comme le `client1.tp6.b1`) quand elles auront besoin de connaître des noms. Ainsi, ce serveur pourra :

- **résoudre des noms locaux**
  - vous pourrez `ping web.tp6.b1` et ça fonctionnera
```bash
┌──(kali㉿client1)-[~]
└─$ ping web.tp6.b1

--- web.tp6.b1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.949/1.642/2.335/0.693 ms
```
  - même visiter le site web avec `http://web.tp6.b1` dans un navigateur
```bash
┌──(kali㉿client1)-[~]
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
- **mais aussi résoudre des noms publics**
  - genre `ping www.ynov.com` et votre serveur DNS sera capable de le résoudre aussi
```bash
┌──(kali㉿client1)-[~]
└─$ ping www.ynov.com

--- www.ynov.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 14.876/15.131/15.387/0.255 ms

```
## 3. Zé bardi


La configuration du serveur DNS va se faire dans 3 fichiers essentiellement :

- **un fichier de configuration principal**
  - `/etc/named.conf`
```bash
[root@dns oui]# cat /etc/named.conf 
options {
        listen-on port 53 { 127.0.0.1; any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";

        allow-query     { localhost; any; };
        allow-query-cache { localhost; any; };

        recursion yes;
};

zone "tp6.b1" IN {
     type master;
     file "tp6.b1.db";
     allow-update { none; };
     allow-query {any; };
};

zone "2.6.10.in-addr.arpa" IN {
     type master;
     file "tp6.b1.rev";
     allow-update { none; };
     allow-query { any; };
};
```
- **un fichier de zone**
  - `/var/named/tp6.b1.db`
```bash
[root@dns ~]# cat /var/named/tp6.b1.db 
$TTL 86400
@ IN SOA dns.tp6.b1. admin.tp6.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns.tp6.b1.

; Enregistrements DNS pour faire correspondre des noms à des IPs
web       IN A 10.6.2.11
dns       IN A 10.6.2.12
```
- **un fichier de zone inverse**
  - `/var/named/tp6.b1.rev`
```bash
[root@dns ~]# cat /var/named/tp6.b1.rev 
$TTL 86400
@ IN SOA dns.tp6.b1. admin.tp6.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns.tp6.b1.

; Reverse lookup
11 IN PTR web.tp6.b1.
12 IN PTR dns.tp6.b1.
```


➜ **Une fois ces 3 fichiers en place, démarrez le service DNS**

```bash
# Démarrer le service
$ sudo systemctl enable --now named

[root@dns ~]# systemctl enable --now named

# Obtenir des infos sur le service
$ sudo systemctl status named

[root@dns ~]# systemctl status named
● named.service - Berkeley Internet Name Domain (DNS)
     Loaded: loaded (/usr/lib/systemd/system/named.service; enabled; preset: disabled)
     Active: active (running) since Mon 2024-10-21 18:00:20 CEST; 14min ago


# Obtenir des logs en cas de probème
$ sudo journalctl -xe -u named
```

## 4. Analyse du service

☀️ **Déterminer sur quel(s) port(s) écoute le service BIND9**

- isolez la ligne intéressante avec un `... | grep <PORT>` une fois que vous avez repéré le port
```bash
[root@dns ~]# ss -lnmp | grep named

udp   UNCONN 0      0                                       10.6.2.12:53               0.0.0.0:*    users:(("named",pid=764,fd=43))
udp   UNCONN 0      0                                       10.6.2.12:53               0.0.0.0:*    users:(("named",pid=764,fd=6))
udp   UNCONN 0      0                                       127.0.0.1:53               0.0.0.0:*    users:(("named",pid=764,fd=33))
udp   UNCONN 0      0                                       127.0.0.1:53               0.0.0.0:*    users:(("named",pid=764,fd=32))
udp   UNCONN 0      0                                           [::1]:53                  [::]:*    users:(("named",pid=764,fd=38))
udp   UNCONN 0      0                                           [::1]:53                  [::]:*    users:(("named",pid=764,fd=39))
tcp   LISTEN 0      10                                      10.6.2.12:53               0.0.0.0:*    users:(("named",pid=764,fd=45))
tcp   LISTEN 0      10                                      10.6.2.12:53               0.0.0.0:*    users:(("named",pid=764,fd=44))
tcp   LISTEN 0      4096                                    127.0.0.1:953              0.0.0.0:*    users:(("named",pid=764,fd=31))
tcp   LISTEN 0      10                                      127.0.0.1:53               0.0.0.0:*    users:(("named",pid=764,fd=36))
tcp   LISTEN 0      10                                      127.0.0.1:53               0.0.0.0:*    users:(("named",pid=764,fd=34))
tcp   LISTEN 0      4096                                        [::1]:953                 [::]:*    users:(("named",pid=764,fd=42))
tcp   LISTEN 0      10                                          [::1]:53                  [::]:*    users:(("named",pid=764,fd=40))
tcp   LISTEN 0      10                                          [::1]:53                  [::]:*    users:(("named",pid=764,fd=41))

```

☀️ **Ouvrir ce(s) port(s) dans le firewall**

Commande à réaliser :
```bash
[root@dns ~]# firewall-cmd --permanent --add-port=53/tcp
Warning: ALREADY_ENABLED: 53:tcp
success
[root@dns ~]# firewall-cmd --permanent --add-port=953/tcp
success
[root@dns ~]# firewall-cmd --permanent --add-port=53/udp
success
[root@dns ~]# firewall-cmd --reload
success
```
```bash
[root@dns ~]# firewall-cmd --list-all

  ports: 22/tcp 22/udp 22/sctp 22/dccp 53/tcp 953/tcp 53/udp

```


## 5. Tests manuels

☀️ **Effectuez des requêtes DNS manuellement** depuis le serveur DNS lui-même dans un premier temps


dig web.tp6.b1 @10.6.2.12
```bash
[root@dns ~]# dig web.tp6.b1 @10.6.2.12

; <<>> DiG 9.16.23-RH <<>> web.tp6.b1 @10.6.2.12
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 36211
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

...
```

dig dns.tp6.b1 @10.6.2.12
```bash
[root@dns ~]# dig dns.tp6.b1 @10.6.2.12

; <<>> DiG 9.16.23-RH <<>> dns.tp6.b1 @10.6.2.12
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15263
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

...
```

dig ynov.com @10.6.2.12
```bash
[root@dns ~]# dig ynov.com @10.6.2.12

; <<>> DiG 9.16.23-RH <<>> ynov.com @10.6.2.12
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 65520
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

...
```

dig -x 10.6.2.11 @10.6.2.12
```bash
[root@dns ~]# dig -x 10.6.2.11 @10.6.2.12

; <<>> DiG 9.16.23-RH <<>> -x 10.6.2.11 @10.6.2.12
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 3501
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

...
```
dig -x 10.6.2.12 @10.6.2.12
```bash
[root@dns ~]# dig -x 10.6.2.12 @10.6.2.12

; <<>> DiG 9.16.23-RH <<>> -x 10.6.2.12 @10.6.2.12
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 39796
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

...
```




☀️ **Effectuez une requête DNS manuellement** depuis `client1.tp6.b1`

- pour obtenir l'adresse IP qui correspond au nom `web.tp6.b1`
```bash
┌──(kali㉿client1)-[~]
└─$ dig web.tp6.b1


; <<>> DiG 9.20.0-Debian <<>> web.tp6.b1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 64551
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

...
```

☀️ **Capturez une requête DNS et la réponse de votre serveur**


```bash
┌──(kali㉿client1)-[~]
└─$ sudo tcpdump -w rdns.pcap -i eth0 
```

[lien vers la capture rdns](./rdns.pcap)




