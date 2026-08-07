# 🛡️ Dynamic MAC Evasion (Moving Target Defense)

This tool acts as a Blue Team defense mechanism. It actively monitors network traffic for SYN/ICMP Flood attacks. Upon detecting an anomaly, it automatically changes the system's MAC address and requests a new IP address, acting as a Moving Target Defense (MTD) system against potential attackers.

## 🚀 Özellikler (Features)
* **Gerçek Zamanlı Ağ Dinleme:** `scapy` kullanarak gelen paketleri anlık izler.
* **DDoS/Flood Tespiti:** SYN ve ICMP Flood saldırılarını hızla belirler ve sınıflandırır.
* **Otomatik Evazyon (Kaçış):** Saldırı tespit edildiğinde ağ arayüzünü kapatır, Multicast çakışmalarını önleyecek güvenli bir rastgele MAC adresi atar ve ağı yeniden başlatır.
* **Soğuma (Cooldown) Mekanizması:** Yoğun saldırı altında sistemin sonsuz bir MAC değiştirme/yeniden başlatma döngüsüne girmesini engeller.

## ⚙️ Kurulum (Installation)
Gerekli kütüphanelerin yüklenmesi için Python'ın kurulu olduğundan emin olun.
```bash
git clone https://github.com/KULLANICI_ADIN/MTD-Network-Shield.git
cd MTD-Network-Shield
pip install -r requirements.txt
```

## 💻 Kullanım (Usage)
Araç, doğrudan ağ arayüzlerine (interface) müdahale ettiği için sistem yöneticisi (root) yetkileriyle çalıştırılmalıdır.
```bash
sudo python3 mtd_shield.py
```

---

## ⚠️ Bilinen Kısıtlamalar (Known Limitations)
Bu betik, savunma manevrası sırasında ağ arayüzünü anlık olarak manipüle eder. Bu durum sanal ortamlarda (VirtualBox, VMware) test edilirken şu kısıtlamalara yol açabilir:
* **Scapy Soket Kapanması:** Sistem, koruma amacıyla `eth0` arayüzünü kapatıp açtığında, Scapy'nin dinleme soketi altındaki bağlantı koptuğu için `Network is down` hatası vererek işlemi durdurabilir. 
* **Hipervizör IP Reddi:** Özellikle **NAT** modunda çalışan sanal makinelerde, hipervizör aniden atanan yeni MAC adresini tanımayarak DHCP üzerinden yeni bir IP atamayı reddedebilir. Bu durum geçici internet kesintisine neden olur.

### 🛠️ Çözüm ve En İyi Test Ortamı
Bu sanallaştırma engellerine takılmadan projenin savunma potansiyelini kesintisiz olarak test etmek için ortamınızı şu şekilde yapılandırmanız önerilir:

1. **Köprü Moduna (Bridged) Geçiş Yapın:** Sanal makinenizin ağ ayarlarından bağlantı türünü NAT yerine doğrudan yerel ağınıza bağlanan **Köprü Bağdaştırıcısı** moduna alın.
2. **Trafiği Serbest Bırakın:** Sanal makine ağ ayarları altındaki Gelişmiş sekmesinden, **Karma Mod (Promiscuous Mode)** ayarını bulup **Tümüne İzin Ver (Allow All)** olarak güncelleyin.
3. **Fiziksel Donanım Kullanın (Tavsiye Edilen):** En kararlı ve gerçekçi Blue Team simülasyonları için, bu aracı sanal makine yerine doğrudan donanıma kurulu fiziksel bir Linux sistemde (örneğin ağa bağlı bir Raspberry Pi) çalıştırmanız en iyi sonuçları verecektir.

---

## ⚖️ Yasal Uyarı (Disclaimer)
**Sadece Eğitim Amaçlıdır.**
Bu araç tamamen ağ güvenliği testleri ve "Hareketli Hedef Savunması" (Moving Target Defense) konseptinin gösterimi amacıyla geliştirilmiştir. Aracın yetkisiz ağlarda veya kötü niyetli kullanımından geliştirici (Güven Zencir) sorumlu tutulamaz.
