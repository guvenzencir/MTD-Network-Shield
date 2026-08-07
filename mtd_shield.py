import random
import subprocess
import time
from scapy.all import sniff, IP, TCP, ICMP

# --- AYARLAR ---
INTERFACE = "eth0"     # Wi-Fi ağlarında dinleme yapılacaksa "wlan0" olarak değiştirin
PACKET_THRESHOLD = 50  # Saldırı eşiği (Belirtilen süredeki maksimum şüpheli paket)
TIME_WINDOW = 5        # Saniye cinsinden zaman penceresi
COOLDOWN = 60          # Savunma sonrası bekleme süresi (Sonsuz döngüyü engeller)

packet_counts = {}
last_evasion_time = 0

def change_mac_and_ip(interface):
    print(f"\n[*] {interface} arayüzü kapatılıyor...")
    subprocess.run(["sudo", "ifconfig", interface, "down"])
    
    # Geçerli bir Yerel Unicast MAC adresi üretir (Multicast çakışmalarını önler)
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
        
        # SYN Flood veya ICMP (Ping) Flood kontrolü (eth0 için en yaygın ağ boğma saldırıları)
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
