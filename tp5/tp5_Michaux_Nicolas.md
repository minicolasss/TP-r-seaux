☀️ Uniquement avec des commandes, prouvez-que :

client1.tp5.b1:

```
oui@client1:~$ cd /etc/netplan/
oui@client1:/etc/netplan$ sudo nano 01-netcfg.yaml


network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s8:
      dhcp4: no
      addresses: [10.5.1.11/24]
      gateway4: 10.5.1.254
```


Le changement de hostname :

```
oui@client1:/etc/netplan$ sudo hostnamectl set-hostname client1.tp5.b1
```



client2.tp5.b1:

```
oui@client2:/etc/netplan$ sudo nano 01-netcfg.yaml


network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s8:
      dhcp4: no
      addresses: [10.5.1.12/24]
      gateway4: 10.5.1.254
```

Le changement de hostname :

```
oui@client2:~$ sudo hostnamectl set-hostname client2.tp5.b1
```



Le routeur :

```
cd /etc/sysconfig/network-scripts

DEVICE=enp0s3
NAME=lan


ONBOOT=yes
BOOTPROTO=dhcp
```

```
DEVICE=enp0s8
NAME=lan


ONBOOT=yes
BOOTPROTO=static


IPADDR=10.5.1.254
NETMASK=255.255.255.0
```



Et enfin voici les ping:

je ping tout le monde depuis mon pc:

```
PS C:\Users\NICOLAS> ping 10.5.1.11

Ping statistics for 10.5.1.11:
    Packets: Sent = 4, Received = 3, Lost = 1 (25% loss),
bytes=32 Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 1ms, Average = 0ms
```

```
PS C:\Users\NICOLAS> ping 10.5.1.12

Ping statistics for 10.5.1.12:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 4ms, Average = 1ms
```

```
PS C:\Users\NICOLAS> ping 10.5.1.254

Ping statistics for 10.5.1.254:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 0ms, Average = 0ms
```

et je ping le client 2 depuit client 1 pour une derniere verif:

```
oui@client1:/etc/netplan$ ping 10.5.1.12
PING 10.5.1.12 (10.5.1.12) 56(84) bytes of data.

--- 10.5.1.12 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4014ms
rtt min/avg/max/mdev = 0.809/4.180/14.249/5.069 ms
```




☀️ Déjà, prouvez que le routeur a un accès internet

```
PS C:\Users\NICOLAS> ssh oui@10.5.1.254
oui@10.5.1.254's password:
Last login: Mon Oct 14 11:54:18 2024
[oui@localhost ~]$ ping ynov.com

--- ynov.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2005ms
rtt min/avg/max/mdev = 31.579/72.092/113.604/33.494 ms
```
