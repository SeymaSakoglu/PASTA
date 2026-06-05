import subprocess
import time

MSF_SIFRE = "12345"
MSF_PORT  = 55553

msf_proc = None

def msf_baslat():
    global msf_proc
    print("[*] Metasploit baslatiliyor, bu biraz surebilir...")
    msf_proc = subprocess.Popen(
        ["msfrpcd", "-U", "msf", "-P", MSF_SIFRE, "-p", str(MSF_PORT), "-S"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("[*] 20 saniye bekleniyor...")
    time.sleep(20)
    print("[+] Metasploit hazir olmali")
    return True

def msf_baglan():
    try:
        from pymetasploit3.msfrpc import MsfRpcClient
        msf = MsfRpcClient(MSF_SIFRE, port=MSF_PORT, ssl=False)
        print("[+] MSF baglantisi OK")
        return msf
    except Exception as hata:
        print(f"[-] MSF baglantisi basarisiz: {hata}")
        return None

def msf_kapat():
    global msf_proc
    if msf_proc:
        msf_proc.terminate()
        print("[*] MSF kapatildi")