from scapy.all import IP, ICMP, send

gateway = "10.6.1.254"

packet = IP(dst=gateway)/ICMP()

send(packet)

print(f"Ping envoyé à {gateway}")

