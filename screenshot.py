import os
import time

KLASOR = "kanitlar"

def klasor_hazirla():
    if not os.path.exists(KLASOR):
        os.mkdir(KLASOR)

def komut_calistir(oturum, komut):
    oturum.write(komut + "\n")
    time.sleep(2)
    return oturum.read()

def kanit_topla(msf, hedef_ip, session_id):
    klasor_hazirla()
    dosya_adi = f"{KLASOR}/{hedef_ip}_session{session_id}.txt"

    try:
        oturum = msf.sessions.session(str(session_id))
    except Exception as e:
        print(f"[-] Session acilamadi: {e}")
        return None

    print(f"[*] Komutlar calistiriliyor (session {session_id})...")

    id_cikti       = komut_calistir(oturum, "id")
    hostname_cikti = komut_calistir(oturum, "hostname")
    uname_cikti    = komut_calistir(oturum, "uname -a")
    ifconfig_cikti = komut_calistir(oturum, "ifconfig")

    with open(dosya_adi, "w") as f:
        f.write(f"Hedef: {hedef_ip}\n")
        f.write(f"Session: {session_id}\n\n")
        f.write("--- id ---\n" + id_cikti + "\n")
        f.write("--- hostname ---\n" + hostname_cikti + "\n")
        f.write("--- uname -a ---\n" + uname_cikti + "\n")
        f.write("--- ifconfig ---\n" + ifconfig_cikti + "\n")

    print(f"[+] Kanit kaydedildi: {dosya_adi}")
    return dosya_adi