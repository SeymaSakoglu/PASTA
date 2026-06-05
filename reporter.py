from database import tum_taramalar, tarama_detay

def raporlari_yazdir():
    taramalar = tum_taramalar()

    if not taramalar:
        print("Henuz tarama yapilmamis.")
        return

    print("\n=== TARAMA GECMISI ===")
    for t in taramalar:
        print(f"ID: {t[0]} | IP: {t[1]} | Portlar: {t[2]} | Tarih: {t[3]} | Durum: {t[4]}")

    secim = input("\nDetay icin ID gir (0=cikis): ")
    if secim == "0" or not secim.isdigit():
        return

    portlar, zafiyetler = tarama_detay(int(secim))

    print("\n--- PORTLAR ---")
    for p in portlar:
        print(f"  {p[2]}/tcp | {p[3]} {p[4]} {p[5]} | {p[6]}")

    print("\n--- ZAFIYETLER ---")
    if zafiyetler:
        for z in zafiyetler:
            print(f"  Port {z[2]} | {z[3]} | {z[4][:100]}")
    else:
        print("  Zafiyet bulunamadi")