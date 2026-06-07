# PASTA — Port Tarama ve Zafiyet Analiz Aracı

Python ile geliştirilmiş bu araç; belirlenen IP adresindeki açık portları tespit eder, çalışan servislerin sürüm bilgilerini analiz eder, zafiyetli portları işaretler ve Metasploit üzerinden exploit denemesi yaparak sonuçları raporlar. Yalnızca eğitim amaçlı, izinli ve kontrollü sanal makine ortamında kullanılmak üzere geliştirilmiştir. Yetkisiz sistemlere karşı kullanılması yasaktır.

***

## Özellikler

- Nmap ile açık port tarama ve servis/sürüm tespiti
- Zafiyetli servis-sürüm eşleşmelerinin otomatik olarak işaretlenmesi
- Metasploit RPC üzerinden kullanıcı onaylı exploit denemesi
- Başarılı oturumlardan kanıt toplama (id, whoami, hostname, uname, ifconfig çıktıları)
- Tüm tarama sonuçlarının SQLite veritabanına kaydedilmesi ve geçmişe dönük görüntüleme
- Hem konsol hem de Tkinter grafik arayüz (GUI) desteği

***

## Kurulum

Önce Python paketlerini yükle:

```bash
pip3 install -r requirements.txt
```

Ardından sistemde Nmap ve Metasploit kurulu olmalı. Kali Linux kullanıyorsan genellikle ikisi de yüklü gelir. Değilse:

```bash
sudo apt install nmap metasploit-framework -y
```

GUI açıldığında Metasploit RPC servisi otomatik başlatılmaya çalışılır. Manuel başlatmak istersen:

```bash
msfrpcd -P sifreniz -S -a 127.0.0.1
```

***

## Kullanım

İki farklı modda çalıştırılabilir:

**Konsol modu** — terminalde adım adım işlem yapar:
```bash
python3 main.py
```

**Grafik arayüz (GUI)** — menülü pencere arayüzü açılır:
```bash
python3 pasta_gui.py
```

GUI açıldığında karşına 5 seçenek çıkar:

```
[1] Metasploitable 2 Tara   →  Ön tanımlı hedefte otomatik tarama + exploit
[2] Özel Tara               →  Kendi IP ve port listeni girerek tarama yap
[3] Raporları Göster        →  Geçmiş taramaları listele ve detay gör
[4] Kanıt Dosyaları         →  Başarılı exploit sonrası elde edilen çıktıları gör
[5] Çıkış                   →  Uygulamayı kapat
```

***

## Notlar

- Proje yalnızca Metasploitable 2 sanal makinesi üzerinde test edilmiştir
- Hedef IP adresini `main.py` içindeki `HEDEF_IP` değişkeninden değiştirebilirsin
- Tüm tarama sonuçları proje klasöründeki `pasta.db` dosyasına kaydedilir
- Exploit sonrası kanıt dosyaları `kanitlar/` klasörüne otomatik olarak yazılır
- Gerçek bir sisteme karşı çalıştırılması etik ve yasal açıdan kabul edilemez

***

## Proje Yapısı

```
PASTA/
├── main.py               # Konsol tabanlı başlatıcı, ana akışı yönetir
├── pasta_gui.py          # Tkinter grafik arayüzü
├── scanner.py            # Nmap tarama ve servis/sürüm ayrıştırma
├── msf_manager.py        # Metasploit RPC bağlantı yönetimi
├── exploiter.py          # Exploit denemesi ve oturum kontrolü
├── screenshot.py         # Kanıt toplama (komut çıktısı + ekran görüntüsü)
├── reporter.py           # Raporlama yardımcı modülü
├── database.py           # SQLite veritabanı işlemleri
├── requirements.txt      # Gerekli Python paketleri
├── .gitignore            # Git tarafından yok sayılacak dosyalar
└── README.md
```

***

## Uygulama Ekran Görüntüleri

![Ana Ekran](app_screenshot/app%20(1).png)
![Exploit Onay](app_screenshot/app%20(2).png)
![Exploit Tamamlandı](app_screenshot/app%20(3).png)
![Özel Tarama](app_screenshot/app%20(4).png)
![Geçmiş Taramalar](app_screenshot/app%20(5).png)
![Tarama Detayı](app_screenshot/app%20(6).png)
![Kanıt Dosyaları](app_screenshot/app%20(7).png)

***

**Geliştirici:** Şeyma SAKOĞLU — Bilgisayar Programcılığı, İstinye Üniversitesi
**Danışman:** Öğr. Gör. Neda Dadashkhani | Haziran 2026
