# PASTA - Port Tarama ve Zafiyet Analiz Araci

Bitirme projesi kapsaminda gelistirilen bu arac,
belirlenen IP adreslerindeki acik portlari tespit eder,
zafiyet analizi yapar ve rapor olusturur.

## Ozellikler

- Nmap ile port tarama ve servis/versiyon tespiti
- NSE script ile zafiyet analizi
- Metasploit ile otomatik exploit denemesi
- Shell ciktisi ve VNC ekran goruntusu ile kanit toplama
- SQLite veritabanina kayit
- Konsol ve GUI arayuz destegi

## Kurulum

pip3 install -r requirements.txt

Ayrica sistemde nmap ve metasploit-framework kurulu olmali.

## Kullanim

Konsol:
    python3 main.py

Grafik Arayuz:
    python3 pasta_gui.py

## Notlar

- Sanal makine ortaminda test edilmistir (Metasploitable 2).
- Hedef IP main.py icinde HEDEF_IP degiskeniyle ayarlanir.
- Tum tarama sonuclari pasta.db dosyasina kaydedilir.
- Kanitlar kanitlar/ klasorune yazilir.

## Proje Yapisi

PASTA/
├── main.py
├── pasta_gui.py
├── scanner.py
├── msf_manager.py
├── exploiter.py
├── screenshot.py
├── reporter.py
├── database.py
├── requirements.txt
├── .gitignore
└── README.md