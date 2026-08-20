# 🛡️ Dynamic MAC Evasion (Moving Target Defense)

🌍 **[Türkçe versiyonu için aşağıya kaydırın / Scroll down for Turkish](#-türkçe-sürüm)**

This tool acts as an active Blue Team defense mechanism. It continuously monitors network traffic for SYN/ICMP Flood attacks. Upon detecting an anomaly, it automatically changes the system's MAC address and requests a new IP address, functioning as a Moving Target Defense (MTD) system to evade potential attackers.

## 🚀 Features
*   **Real-Time Sniffing:** Actively monitors incoming packets in real-time using `scapy`.
*   **DDoS/Flood Detection:** Rapidly identifies and classifies SYN and ICMP Flood attacks.
*   **Automated Evasion:** Upon detecting an attack, it brings down the network interface, assigns a secure randomized MAC address (preventing Multicast conflicts), and restarts the network.
*   **Cooldown Mechanism:** Prevents the system from entering an infinite MAC-changing/restarting loop while under heavy attack.

## ⚙️ Installation
Ensure Python 3 is installed on your system before setting up the required libraries.
```bash
git clone [https://github.com/YOUR_USERNAME/MTD-Network-Shield.git](https://github.com/YOUR_USERNAME/MTD-Network-Shield.git)
cd MTD-Network-Shield
pip install -r requirements.txt
```

## 💻 Usage
Since the tool manipulates network interfaces directly, it must be executed with **root (sudo)** privileges.
```bash
sudo python3 mtd_shield.py
```

---

## ⚠️ Known Limitations
This script temporarily manipulates the network interface during its defensive maneuver. When testing in virtualized environments (like VirtualBox or VMware), you might encounter the following limitations:
*   **Scapy Socket Drop:** When the system brings down the `eth0` interface for protection, Scapy's underlying listening socket disconnects, potentially stopping the process with a `Network is down` error.
*   **Hypervisor IP Rejection:** Especially in virtual machines running in **NAT** mode, the hypervisor might not recognize the suddenly assigned new MAC address, refusing to lease a new IP via DHCP. This causes a temporary loss of internet connectivity.

### 🛠️ Workaround & Best Testing Environment
To seamlessly test the defensive potential of this project without hitting virtualization roadblocks, it is recommended to configure your environment as follows:

1.  **Switch to Bridged Mode:** Change your virtual machine's network adapter from NAT to **Bridged Adapter**, connecting it directly to your local network.
2.  **Allow Promiscuous Traffic:** In the advanced network settings of your VM, find the **Promiscuous Mode** option and set it to **Allow All**.
3.  **Use Physical Hardware (Recommended):** For the most stable and realistic Blue Team simulations, running this tool directly on a physical Linux machine (e.g., a networked Raspberry Pi) rather than a VM will yield the best results.

---

## ⚖️ Disclaimer
**For Educational Purposes Only.**
This tool was developed strictly for network security testing and demonstrating the "Moving Target Defense" concept. The developer (Güven Zencir) cannot be held responsible for any misuse or deployment on unauthorized networks.

---
---

<a name="-türkçe-sürüm"></a>
# 🇹🇷 Dinamik MAC Evazyonu (Hareketli Hedef Savunması)

Bu araç, bir Mavi Takım (Blue Team) savunma mekanizması olarak çalışır. Ağ trafiğini SYN/ICMP Flood saldırılarına karşı aktif olarak izler. Bir anomali tespit ettiğinde, sistemin MAC adresini otomatik olarak değiştirir ve yeni bir IP adresi talep ederek, potansiyel saldırganlara karşı bir Hareketli Hedef Savunması (MTD) sistemi olarak işlev görür.

## 🚀 Özellikler
*   **Gerçek Zamanlı Ağ Dinleme:** `scapy` kullanarak gelen paketleri anlık izler.
*   **DDoS/Flood Tespiti:** SYN ve ICMP Flood saldırılarını hızla belirler ve sınıflandırır.
*   **Otomatik Evazyon (Kaçış):** Saldırı tespit edildiğinde ağ arayüzünü kapatır, Multicast çakışmalarını önleyecek güvenli bir rastgele MAC adresi atar ve ağı yeniden başlatır.
*   **Soğuma (Cooldown) Mekanizması:** Yoğun saldırı altında sistemin sonsuz bir MAC değiştirme/yeniden başlatma döngüsüne girmesini engeller.

## ⚙️ Kurulum
Gerekli kütüphanelerin yüklenmesi için sisteminizde Python 3'ün kurulu olduğundan emin olun.
```bash
git clone [https://github.com/KULLANICI_ADIN/MTD-Network-Shield.git](https://github.com/KULLANICI_ADIN/MTD-Network-Shield.git)
cd MTD-Network-Shield
pip install -r requirements.txt
```

## 💻 Kullanım
Araç, doğrudan ağ arayüzlerine (interface) müdahale ettiği için sistem yöneticisi **(root)** yetkileriyle çalıştırılmalıdır.
```bash
sudo python3 mtd_shield.py
```

---

## ⚠️ Bilinen Kısıtlamalar
Bu betik, savunma manevrası sırasında ağ arayüzünü anlık olarak manipüle eder. Bu durum sanal ortamlarda (VirtualBox, VMware) test edilirken şu kısıtlamalara yol açabilir:
*   **Scapy Soket Kapanması:** Sistem, koruma amacıyla `eth0` arayüzünü kapatıp açtığında, Scapy'nin dinleme soketi altındaki bağlantı koptuğu için `Network is down` hatası vererek işlemi durdurabilir. 
*   **Hipervizör IP Reddi:** Özellikle **NAT** modunda çalışan sanal makinelerde, hipervizör aniden atanan yeni MAC adresini tanımayarak DHCP üzerinden yeni bir IP atamayı reddedebilir. Bu durum geçici internet kesintisine neden olur.

### 🛠️ Çözüm ve En İyi Test Ortamı
Bu sanallaştırma engellerine takılmadan projenin savunma potansiyelini kesintisiz olarak test etmek için ortamınızı şu şekilde yapılandırmanız önerilir:

1.  **Köprü Moduna (Bridged) Geçiş Yapın:** Sanal makinenizin ağ ayarlarından bağlantı türünü NAT yerine doğrudan yerel ağınıza bağlanan **Köprü Bağdaştırıcısı** moduna alın.
2.  **Trafiği Serbest Bırakın:** Sanal makine ağ ayarları altındaki Gelişmiş sekmesinden, **Karma Mod (Promiscuous Mode)** ayarını bulup **Tümüne İzin Ver (Allow All)** olarak güncelleyin.
3.  **Fiziksel Donanım Kullanın (Tavsiye Edilen):** En kararlı ve gerçekçi Blue Team simülasyonları için, bu aracı sanal makine yerine doğrudan donanıma kurulu fiziksel bir Linux sistemde (örneğin ağa bağlı bir Raspberry Pi) çalıştırmanız en iyi sonuçları verecektir.

---

## ⚖️ Yasal Uyarı
**Sadece Eğitim Amaçlıdır.**
Bu araç tamamen ağ güvenliği testleri ve "Hareketli Hedef Savunması" (Moving Target Defense) konseptinin gösterimi amacıyla geliştirilmiştir. Aracın yetkisiz ağlarda veya kötü niyetli kullanımından geliştirici (Güven Zencir) sorumlu tutulamaz.
