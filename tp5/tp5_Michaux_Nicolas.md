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
Last login: Mon Oct 14 13:01:29 2024 from 10.5.1.1
[oui@routeur ~]$ ping ynov.com

--- ynov.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2010ms
rtt min/avg/max/mdev = 17.675/22.902/27.948/4.195 ms
```



☀️ Activez le routage

```
[oui@routeur ~]$ sudo firewall-cmd --add-masquerade --permanent && sudo firewall-cmd --reload
Warning: ALREADY_ENABLED: masquerade
success
success
```



2. Accès internet clients

☀️ Prouvez que les clients ont un accès internet

client1.tp5.b1 : 

ping 1.1.1.1

```
oui@client1:~$ ping 1.1.1.1

--- 1.1.1.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 13.767/14.999/16.164/0.979 ms
```


client2.tp5.b1 : 

ping 1.1.1.1 

```
oui@client2:~$ ping 1.1.1.1

--- 1.1.1.1 ping statistics ---
7 packets transmitted, 7 received, 0% packet loss, time 6079ms
rtt min/avg/max/mdev = 15.563/18.017/23.843/2.655 ms
```



☀️ Montrez-moi le contenu final du fichier de configuration de l'interface réseau

client2.tp5.b1 :

```
oui@client2:~$ cd /etc/netplan
oui@client2:/etc/netplan$ ls
01-netcfg.yaml  50-cloud-init.yaml
```
```
oui@client2:/etc/netplan$ nano 01-netcfg.yaml
```
```
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s8:
      dhcp4: no
      addresses: [10.5.1.12/24]
      gateway4: 10.5.1.254
```


III. Serveur SSH

 ☀️ Installez et configurez un serveur DHCP sur la machine routeur.tp5.b1

 ```
  dnf -y install dhcp-server
```

```
[oui@routeur dhcp]$ sudo nano dhcpd.conf
```
```
option domain-name-servers     1.1.1.1;

authoritative;


subnet 10.5.1.0 netmask 255.255.255.0 {
    range dynamic-bootp 10.5.1.137 10.5.1.237;
    option routers 10.5.1.254;
    option broadcast-address 10.5.1.255;
    option domain-name-servers 1.1.1.1;
}
```
```
[oui@routeur dhcp]$ sudo systemctl enable --now dhcpd
```
```
[oui@routeur dhcp]$ sudo firewall-cmd --add-service=dhcp
Warning: ALREADY_ENABLED: 'dhcp' already in 'public'
success
```
```
[oui@routeur dhcp]$ sudo firewall-cmd --runtime-to-permanent
success
```



B. Test avec un nouveau client


☀️ Créez une nouvelle machine client client3.tp5.b1

```
oui@client3:~$ sudo hostnamectl set-hostname client3.tp5.b1
```

```
oui@client3:~$ ip a

 enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:29:10:13 brd ff:ff:ff:ff:ff:ff
    inet 10.5.1.137/24 brd 10.5.1.255 scope global dynamic noprefixroute enp0s8
       valid_lft 39654sec preferred_lft 39654sec
    inet6 fe80::3421:3234:4086:de10/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
```

on voit que l'ip est 10.5.1.137 donc oui elle est dans .137 et .237

```
oui@client3:~$ ping 1.1.1.1

--- 1.1.1.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 15.241/19.710/22.647/3.212 ms
```


C. Consulter le bail DHCP


☀️ Consultez le bail DHCP qui a été créé pour notre client

```
[oui@routeur dhcpd]$ cat dhcpd.leases
# The format of this file is documented in the dhcpd.leases(5) manual page.
# This lease file was written by isc-dhcp-4.4.2b1

# authoring-byte-order entry is generated, DO NOT DELETE
authoring-byte-order little-endian;

lease 10.5.1.137 {
  starts 1 2024/10/14 20:12:29;
  ends 2 2024/10/15 08:12:29;
  tstp 2 2024/10/15 08:12:29;
  cltt 1 2024/10/14 20:12:29;
  binding state active;
  next binding state free;
  rewind binding state free;
  hardware ethernet 08:00:27:29:10:13;
  uid "\001\010\000')\020\023";
  client-hostname "oui";
}
server-duid "\000\001\000\001.\2405\366\010\000'\251\314\275";

lease 10.5.1.137 {
  starts 1 2024/10/14 21:16:07;
  ends 2 2024/10/15 09:16:07;
  cltt 1 2024/10/14 21:16:07;
  binding state active;
  next binding state free;
  rewind binding state free;
  hardware ethernet 08:00:27:29:10:13;
  uid "\001\010\000')\020\023";
  client-hostname "client3";
}
```
ce qui est interessent cest qu'on observe le changement de hostname de oui a client3


☀️ Confirmez qu'il s'agit bien de la bonne adresse MAC

```
oui@client3:~$ ip a

2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:29:10:13 brd ff:ff:ff:ff:ff:ff
```
```
[oui@routeur dhcpd]$ cat dhcpd.leases

 hardware ethernet 08:00:27:29:10:13;
```

