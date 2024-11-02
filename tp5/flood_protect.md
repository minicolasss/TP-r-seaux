# Bonus : Flood protection

Bonus dédié à **la protection contre le flood réseau.**

> Le *flood* c'est le fait de spammer de FOU un truc. En l'occurrence, on parle de *flood* réseau, c'est à dire envoyer BEAUCOUP de paquets à une machine donnée.

➜ **Imagine t'as ton p'tit serveur en ligne, t'es heureux.**

T'héberges ton p'tit site web, ou ton p'tit serveur minecraft, ou peu importe.  
Et toutakou, ton serveur reçoit des tonnes de paquets. Tout ce que fait le serveur va être potentiellement ralenti ~~ça va ramer sec Minecraft~~.

Même possible que ton serveur arrête complètement de fonctionner :d

![Flood](./img/flood.png)

➜ **Dans la vie réelle, on peut recevoir du flood sur un serveur dans des situations comme :**

- **bruteforce**
  - quelqu'un tente par exemple des tonnes de mots de passe pour se connecter en SSH
  - le serveur SSH n'est qu'un exemple, on pourrait tenter de bruteforce d'autres services
- **tentative de DOS**
  - si tu flood assez fort, y'a des chances que le serveur arrête de fonctionner
  - trop de paquets, ou trop de connexions simultanées, ou trop de données à traiter, etc..
- casser les couilles ?

➜ **Le but du TP**

- savoir repérer un flood sur le service SSH
- repérer QUI flood (l'adresse IP de la source)
- ban la source du flood (avec le pare-feu)


## Sommaire

- [Bonus : Flood protection](#bonus--flood-protection)
  - [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
- [I. Alatak](#i-alatak)
  - [1. Connexions TCP actives](#1-connexions-tcp-actives)
  - [2. Logs SSH](#2-logs-ssh)
  - [3. Ban this guy](#3-ban-this-guy)
- [II. Fail2ban](#ii-fail2ban)

# 0. Prérequis

- le TP5 avec `routeur.tp5.b1` correctement configuré et allumé
  - il doit avoir l'IP `10.5.1.254` comme demandé dans le TP
- au moins un client, qui jouera le rôle de l'acteur malveillant

☀️ **Lancer [mon super script qui super flood](./flood.sh)**

- depuis le client malveillant
- vous téléchargez le script dans la VM, puis vous l'exécutez
- tu peux le lire, mais c'est plus rigolo pour l'exercice si tu le lis pas :d

```bash
# on télécharge le script
wget <URL>

# exécution du script
bash flood.sh

 # et tu laisses tourner :D
```

# I. Alatak

> *Sur la machine `routeur.tp5.b1`.*

## 1. Connexions TCP actives

Déjà, repérons quel est le type de flood.

Si c'est des connexions répétées sur un port spécifique, on connaît déjà les commandes !

☀️ **Lister les connexions TCP actives**

- repérer s'il y a quelque chose d'anormal
- genre beaucoup de connexions ? :d
- de la même source ?

➜ **Vous devriez aussi repérer le port de destination de ces connexions**

- étant admin du serveur, on sait très bien ce qui tourne derrière ce port...

## 2. Logs SSH

☀️ **Trouver le fichier de logs du service SSH**

- tout programme digne de ce nom écrit dans un fichier texte tout ce qu'il fait
- **on appelle ce fichier un *fichier de log***
- le service SSH écrit dans son *fichier de log* toutes les tentatives de connexions
- et il indique aussi si elles ont réussi ou non
- et évidemmeeeeent l'adresse IP de la personne qui a essayé de se connecter

> Avec un OS GNU/Linux, les fichiers de logs sont généralement stockés dans `/var/log`. Demande à Googueule toute façon où il est le fichier :d

## 3. Ban this guy

☀️ **Repérer et ban la source du flood**

- utiliser une commande `firewall-cmd` pour ban l'adresse IP de la source
- une fois ban, confirmer le ban en essayant une connexion depuis le client

> *Pas dans le mémo cette commande ;d*

➜ HA ! Et il faudrait arrêter le script `flood.sh` aussi, parce qu'il flood toujours ! :d

# II. Fail2ban

Bonus dans le bonus ! Evidemment, il existe des outils qui font ça automatiquement.

Genre on attend pas toute la journée à regarder les logs SSH pour ban des gens.

☀️ **Installer fail2ban sur `routeur.tp5.b1`**

☀️ **Configurer fail2ban**

- il doit repérer les connexions répétées et échouées sur le service SSH
- et ban les adresses IP qui sont la source de ces connexions répétées

![BONK](./img/bonk.png)
