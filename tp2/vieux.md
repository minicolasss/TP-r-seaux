Michaux Nicolas

1. Quelques pings

🌞 Prouvez que votre configuration est effective

```
C:\Windows\system32> Get-NetIPAddress -InterfaceAlias "ethernet 3"
```

```
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

IPAddress         : 169.254.141.7
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

J'ai vérifié que j'avais bien changé mon adresse IP en 10.234.111.1



🌞 Tester que votre LAN + votre adressage IP est fonctionnel

j'ai ping mon copain :

```
ping 10.234.111.2
```

résultat :

```
Ping statistics for 10.234.111.2:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 4ms, Maximum = 6ms, Average = 4ms
```


On peut voir que j'ai bien reçu une réponse.


🌞 Capture de ping

[lien vers ma capture](ping1.pcap)

Sur la capture, on voit clairement que j'ai reçu et envoyé des pings.




II. Utilisation des ports


🌞 Sur le PC serveur

```
PS C:\Users\NICOLAS\Desktop\logiciels\netcat-win32-1.11\netcat-1.11> .\nc.exe -l -p 9999
```



🌞 Sur le PC serveur toujours

```
PS C:\Windows\system32> netstat -a -n -b
```

```
  TCP    0.0.0.0:9999           0.0.0.0:0              LISTENING
 [nc.exe]
```

Grâce à cette ligne, je m'assure que mon serveur est bien ouvert.


🌞 Sur le PC client

```
PS C:\Users\NICOLAS\Desktop\logiciels\netcat-win32-1.11\netcat-1.11> .\nc.exe 10.234.111.2 9999
```

La commande pour me connecter à mon ami inclut bien la spécification du port.

```
PS C:\Users\NICOLAS\Desktop\logiciels\netcat-win32-1.11\netcat-1.11> .\nc.exe 10.234.111.2 9999
oui
sedlgdhg
sedefùesf
sf
s
```

On peut voir tous les messages envoyés.


🌞 Utilisez une commande qui permet de voir la connexion en cours


```
  TCP    10.234.111.1:52634     10.234.111.2:9999      ESTABLISHED
 [nc.exe]
```

Grâce à cela, on voit que je suis bien connecté à mon ami.


🌞 Faites une capture Wireshark complète d'un échange

[lien vers ma capture](netcat1.pcap)

On peut voir tous les paquets échangés pendant l'échange de messages.



🌞 Inversez les rôles

[lien vers ma capture](netcat2.pcap)

Et voici la même chose, mais cette fois où je suis le serveur.



III. Analyse de vos applications usuelles


🌞 Utilisez Wireshark pour capturer du trafic HTTP

[lien vers ma capture](http.pcap)


🌞 Pour les 5 applications

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