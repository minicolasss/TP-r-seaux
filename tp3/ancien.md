I. ARP basics


☀️ Avant de continuer...

```
Wireless LAN adapter Wi-Fi:

  Physical Address. . . . . . . . . : 28-C5-D2-EA-30-53
```


☀️ Affichez votre table ARP


 Pour afficher une table ARP, on exécute la commande : 

 ```
 PS C:\Users\NICOLAS> arp -a
 ```


 Et voici le resultat

 ```
 Interface: 10.33.76.110 --- 0x8
  Internet Address      Physical Address      Type
  10.33.65.63           44-af-28-c3-6a-9f     dynamic
  10.33.73.77           98-8d-46-c4-fa-e5     dynamic
  10.33.77.159          f8-54-f6-ba-c5-1a     dynamic
  10.33.77.160          c8-94-02-f8-ab-97     dynamic
  10.33.79.254          7c-5a-1c-d3-d8-76     dynamic
  10.33.79.255          ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static

Interface: 169.254.141.7 --- 0x10
  Internet Address      Physical Address      Type
  169.254.255.255       ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static
  ```


☀️ Déterminez l'adresse MAC de la passerelle du réseau de l'école


J'ai juste regardé dans la table ARP, et voici : 

```
 10.33.79.254          7c-5a-1c-d3-d8-76     dynamic
```


☀️ Supprimez la ligne qui concerne la passerelle

J'ai exécuté la commande en même temps, et voici ma ligne :

```
PS C:\Windows\system32> arp -d 10.33.79.254 ; arp -a
```


☀️ Prouvez que vous avez supprimé la ligne dans la table ARP

voici ma table arp 

```
PS C:\Windows\system32> arp -d 10.33.79.254 ; arp -a

Interface: 10.33.76.110 --- 0x8
  Internet Address      Physical Address      Type
  10.33.65.63           44-af-28-c3-6a-9f     dynamic
  10.33.73.77           98-8d-46-c4-fa-e5     dynamic
  10.33.77.159          f8-54-f6-ba-c5-1a     dynamic
  10.33.77.160          c8-94-02-f8-ab-97     dynamic
  10.33.79.255          ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static

Interface: 169.254.141.7 --- 0x10
  Internet Address      Physical Address      Type
  169.254.255.255       ff-ff-ff-ff-ff-ff     static
  224.0.0.22            01-00-5e-00-00-16     static
  224.0.0.251           01-00-5e-00-00-fb     static
  224.0.0.252           01-00-5e-00-00-fc     static
  239.255.255.250       01-00-5e-7f-ff-fa     static
  255.255.255.255       ff-ff-ff-ff-ff-ff     static
  ```

☀️ Wireshark

[lien vers ma capture](arp1.pcap)



II. ARP dans un réseau local

1. Basics

☀️ Déterminer

voici les information du serveur :

```
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.231.2
   DNS Servers . . . . . . . . . . . : 192.168.231.2
   NetBIOS over Tcpip. . . . . . . . : Enabled


   192.168.231.2         e6-0f-c1-06-f5-1d     dynamic
```

pour cela j'ai executer les commande :

```
PS C:\Windows\system32> arp -a
PS C:\Windows\system32> ipconfig /all
```


☀️ DIY

mon ip de base

```
PS C:\Windows\system32> ipconfig

   IPv4 Address. . . . . . . . . . . : 192.168.231.44
```

et voici ma nouvelle ip :

```
PS C:\Windows\system32> ipconfig

   IPv4 Address. . . . . . . . . . . : 192.168.231.56
```


☀️ Pingz !

voici un ping 

```
PS C:\Windows\system32> ping 192.168.231.25

Ping statistics for 192.168.231.25:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 8ms, Maximum = 1821ms, Average = 461ms
```

et voici le 2eme ping

```
PS C:\Windows\system32> ping 192.168.231.7

Ping statistics for 192.168.231.7:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 8ms, Maximum = 64ms, Average = 32ms
```


2. ARP


☀️ Affichez votre table ARP !

voici un morceau du arp -a ou on peut voir le serveur et mon ami qui à l'ip 192.168.231.25 et 192.168.231.7

```
PS C:\Windows\system32> arp -a

PS C:\Windows\system32> arp -a

Interface: 192.168.231.56 --- 0x8
  Internet Address      Physical Address      Type
  192.168.231.2         e6-0f-c1-06-f5-1d     dynamic
  192.168.231.7         58-cd-c9-22-43-fd     dynamic
  192.168.231.25        f8-54-f6-ba-c5-1a     dynamic
```


☀️ Capture arp2.pcap

[lien vers ma capture](arp2.pcap)


3. Bonus : ARP poisoning


