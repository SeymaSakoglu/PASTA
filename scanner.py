#!/usr/bin/env python3
import nmap
import colorama
from colorama import Fore, Style
from database import tarama_kaydet, sonuc_kaydet

colorama.init()

def port_tara(ip_adresi, port_aralik="1-1024"):
    print(f"\n{Fore.CYAN}[*] Hedef: {ip_adresi} | Port aralik: {port_aralik}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Tarama basliyor...{Style.RESET_ALL}\n")
    
    tarayici = nmap.PortScanner()

    try:
        tarayici.scan(
            hosts=ip_adresi,
            ports=port_aralik,
            arguments="-sV"
        )
    except Exception as e:
        print(f"{Fore.RED}[-] Tarama hatasi: {e}{Style.RESET_ALL}")
        return
    
    if ip_adresi not in tarayici.all_hosts():
        print(f"{Fore.RED}[-] Hedefe ulasilamadi.{Style.RESET_ALL}")
    
    tarama_id = tarama_kaydet(ip_adresi)

    acik_port_sayisi = 0

    for port in tarayici[ip_adresi]["tcp"]:
        bilgi = tarayici[ip_adresi]["tcp"][port]
        durum = bilgi["state"]
        servis = bilgi["name"]
        versiyon = bilgi["version"]

        if durum == "open":
            acik_port_sayisi += 1
            print(f"{Fore.GREEN}[+] Port {port}/tcp ACIK | {servis} {versiyon}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Port {port}/tcp KAPALI{Style.RESET_ALL}")

        sonuc_kaydet(tarama_id, port, servis, versiyon, durum)
    
    print(f"\n{Fore.CYAN}[*] Tarama tamamlandi. {acik_port_sayisi} acik port bulundu.{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}[*] Sonuclar veritabanina kaydedildi. (Tarama ID: {tarama_id}){Style.RESET_ALL}\n")
