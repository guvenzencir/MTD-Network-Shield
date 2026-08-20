import random
import subprocess
import time
from scapy.all import sniff, IP, TCP, ICMP

INTERFACE = "eth0"     
PACKET_THRESHOLD = 50 
TIME_WINDOW = 5       
COOLDOWN = 60          

packet_counts = {}
last_evasion_time = 0

def change_mac_and_ip(interface):
    print(f"\n[*] {interface} arayüzü kapatılıyor...")
    subprocess.run(["sudo", "ifconfig", interface, "down"])
     hex_chars = "0123456789ABCDEF"
    valid_second_chars = "26AE"
    new_mac = f"{random.choice(hex_chars)}{random.choice(valid_second_chars)}"
    for _ in range(5):
        new_mac += f":{random.choice(hex_chars)}{random.choice(hex_chars)}"
        
    print(f"[*] Yeni MAC Adresi Atanıyor: {new_mac}")
    subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["sudo", "ifconfig", interface, "up"])
    
    print("[*] NetworkManager yeniden başlatılıyor (Yeni IP almak için)...")
    subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"])
    print("[+] Kaçış (Evasion) başarılı! Yeni kimlikle ağa dönüldü.\n")

def detect_attack(packet):
    global last_evasion_time
    
    if time.time() - last_evasion_time < COOLDOWN:
        return

    if IP in packet:
        src_ip = packet[IP].src
        is_suspicious = False
        if TCP in packet and packet[TCP].flags == 'S':
            is_suspicious = True
        elif ICMP in packet:
            is_suspicious = True
            
        if is_suspicious:
            current_time = time.time()
            
            if src_ip not in packet_counts:
                packet_counts[src_ip] = []
            
            packet_counts[src_ip] = [t for t in packet_counts[src_ip] if current_time - t < TIME_WINDOW]
            packet_counts[src_ip].append(current_time)
            
            if len(packet_counts[src_ip]) > PACKET_THRESHOLD:
                print(f"\n[!!!] AĞ SALDIRISI TESPİT EDİLDİ! Kaynak IP: {src_ip}")
                print("[!!!] HAREKETLİ HEDEF SAVUNMASI (MTD) BAŞLATILIYOR...")
                last_evasion_time = time.time()
                packet_counts.clear()
                change_mac_and_ip(INTERFACE)

def start_sniffer():
    print(f"[*] Dinleme başlatıldı ({INTERFACE}). Olası SYN/ICMP Flood saldırıları izleniyor...")
    sniff(iface=INTERFACE, prn=detect_attack, store=False)

if __name__ == "__main__":
    print("-" * 55)
    print("M.T.D (Moving Target Defense) - Dinamik Ağ Savunma Kalkanı")
    print("-" * 55)
    try:
        start_sniffer()
    except KeyboardInterrupt:
        print("\n[*] Kullanıcı tarafından sonlandırıldı.")
    except PermissionError:
        print("\n[!] HATA: Bu script root yetkileriyle (sudo) çalıştırılmalıdır!")
    except Exception as e:
        print(f"\n[!] Beklenmeyen Hata: {e}")
