import nmap
from database import tarama_ekle, tarama_guncelle, port_ekle, zafiyet_ekle

BILINEN_ZAFIYETLER = {
    21: "vsftpd 2.3.4",
    445: "Samba 3.0.20",
    3306: "MySQL 5.0",
    1524: "Metasploitable"
}

def tara(hedef_ip, portlar="1-1024"):
    print(f"[*] {hedef_ip} taranıyor...")
    tarayici = nmap.PortScanner()

    try:
        tarayici.scan(hedef_ip, portlar, "-sV")
    except Exception as e:
        print(f"[-] Tarama hatasi: {e}")
        return None, []

    if hedef_ip not in tarayici.all_hosts():
        print("[-] Makineye ulasilamadi")
        return None, []

    tid = tarama_ekle(hedef_ip, portlar)
    zafiyet_portlari = []

    for port in tarayici[hedef_ip].get("tcp", {}):
        bilgi = tarayici[hedef_ip]["tcp"][port]
        durum = bilgi["state"]
        servis = bilgi.get("name", "")
        urun = bilgi.get("product", "")
        versiyon = bilgi.get("version", "")

        port_ekle(tid, port, servis, urun, versiyon, durum)

        if durum == "open":
            print(f"  [ACIK] {port}/tcp - {servis} {urun} {versiyon}")

            if port in BILINEN_ZAFIYETLER:
                beklenen = BILINEN_ZAFIYETLER[port]
                tam = f"{urun} {versiyon}"
                if beklenen.lower() in tam.lower():
                    print(f"  [!!!] ZAFIYET BULUNDU: port {port} - {beklenen}")
                    zafiyet_ekle(tid, port, "versiyon", f"Zafiyetli: {tam}")
                    zafiyet_portlari.append(port)
        else:
            print(f"  [KAPALI] {port}/tcp")

    tarama_guncelle(tid, "tamamlandi")
    print(f"[+] Tarama bitti. Zafiyet portlari: {zafiyet_portlari}")
    return tid, zafiyet_portlari