from database import tablo_olustur
from scanner import tara
from exploiter import exploit_calistir
from reporter import raporlari_yazdir
from msf_manager import msf_baslat, msf_baglan, msf_kapat

HEDEF = "192.168.109.128"
PORTLAR = "21,22,80,139,445,1524,3306,3632,5900,6667"

tablo_olustur()

print("[*] Metasploit baslıyor...")
msf_baslat()
msf = msf_baglan()

while True:
    print("\n--- PASTA MENU ---")
    print("1) Metasploitable 2 Tara")
    print("2) Ozel Tara")
    print("3) Raporlari Goster")
    print("4) Cikis")

    secim = input("Secim: ")

    if secim == "1":
        tid, zafiyet_portlari = tara(HEDEF, PORTLAR)
        if zafiyet_portlari:
            cevap = input("Exploit denensin mi? (e/h): ")
            if cevap == "e":
                exploit_calistir(msf, HEDEF, zafiyet_portlari)

    elif secim == "2":
        ip = input("Hedef IP: ")
        p  = input("Portlar (orn: 21,80,443): ")
        tid, zafiyet_portlari = tara(ip, p)
        if zafiyet_portlari:
            cevap = input("Exploit denensin mi? (e/h): ")
            if cevap == "e":
                exploit_calistir(msf, ip, zafiyet_portlari)

    elif secim == "3":
        raporlari_yazdir()

    elif secim == "4":
        msf_kapat()
        print("Cikiliyor...")
        break

    else:
        print("Yanlis secim!")