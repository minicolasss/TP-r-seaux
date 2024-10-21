from scapy.all import DNS, DNSQR, IP, sr1, UDP

dns_req = IP(dst='1.1.1.1') / \
           UDP(dport=53) / \
           DNS(rd=1, qd=DNSQR(qname='thinkerview.com'))

answer = sr1(dns_req, verbose=0)

if answer and answer.haslayer(DNS) and answer[DNS].ancount > 0:
    ip_address = answer[DNS].an.rdata
    print(f"L'adresse IP de thinkerview.com :  {ip_address}")

