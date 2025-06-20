from scapy.all import Ether, IP, UDP, Raw, sendp
import time

# Destination (camera) MAC and IP
target_mac = "30:13:8B:7A:3D:27"       # Your camera's MAC
target_ip = "100.120.67.100"            # Your camera's IP
source_ip = "192.168.1.100"           # Your Raspberry Pi's IP
source_mac = "30:68:93:1D:0E:B8"      # OPTIONAL: Set to your Pi's MAC or leave as is

# Source/destination ports (from your capture)
src_port = 40524
dst_port = 62020

# Raw payload (from your packet capture, truncated for example)
raw_hex = (
    "80e01ac500e3b11018448cd441f5af92bfff0000030000030004ecf105555b00000300000300aa6c843d3934003d5bec916a900000030013cb90f2ae2400000300000300000302035375c9a600000300000300001a4218d238be3a8b04e8042724712e12465a80000003001d5d6cf1c088100003567fbb500000030000068540436000000459f9d00000030000030000f0da608cb780002e0cf41101c739ad171c"
)

# Convert hex to bytes
payload = bytes.fromhex(raw_hex)

# Build full Ethernet+IP+UDP packet
packet = (
    Ether(dst=target_mac, src=source_mac) /
    IP(dst=target_ip, src=source_ip) /
    UDP(sport=src_port, dport=dst_port) /
    Raw(load=payload)
)

# Send packet in a loop
try:
    print(f"[+] Sending spoofed UDP packet to {target_ip} ({target_mac}) every second...")
    while True:
        sendp(packet, iface="tailscale0", verbose=False)  # Change iface if needed
        print("[+] Packet sent.")
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[!] Stopped by user.")
