# III. 1. Serveur Web

➜ **Installez et démarrez le service web NGINX**

```bash
# installation du service NGINX
sudo dnf install -y nginx

# démarrage du service NGINX
sudo systemctl enable --now nginx
```

### 3. Analyse et test

☀️ **Déterminer sur quel port écoute le serveur NGINX**

- isolez la ligne intéressante avec un `... | grep <PORT>` une fois que vous avez repéré le port
```
[root@web oui]# ss -lnpt
State     Recv-Q    Send-Q       Local Address:Port        Peer Address:Port    Process                                                                         
LISTEN    0         511                0.0.0.0:80               0.0.0.0:*        users:(("nginx",pid=813,fd=6),("nginx",pid=812,fd=6),("nginx",pid=811,fd=6))   
LISTEN    0         511                   [::]:80                  [::]:*        users:(("nginx",pid=813,fd=7),("nginx",pid=812,fd=7),("nginx",pid=811,fd=7)) 
```

☀️ **Ouvrir ce port dans le firewall**

- bien que NGINX soit en train d'écouter sur le port repéré, et attende la connexion de clients potentiels...
```
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --reload
```
vérification
```
[root@web oui]# firewall-cmd --list-all
public (active)

  ports: 80/tcp

```
- ... ça empêche pas le firewall de bloquer les clients si on ouvre pas le port
```
Je peux accéder à mon serveur depuis mon client.  
Et j'ai refait un autre serveur pour vérifier,  
Le serveur avait comme IP 10.6.2.13
```

☀️ **Visitez le site web !**


- pour le compte-rendu, depuis le terminal de `client1.tp6.b1` : `curl http://10.6.2.11`
```
┌──(kali㉿client1)-[~]
└─$ curl http://10.6.2.11            
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>HTTP Server Test Page powered by: Rocky Linux</title>
    <style type="text/css">
      /*<![CDATA[*/
```
et pour le kiff 
```
┌──(kali㉿client1)-[~]
└─$ curl http://10.6.2.13            
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>HTTP Server Test Page powered by: Rocky Linux</title>
    <style type="text/css">
      /*<![CDATA[*/
```
