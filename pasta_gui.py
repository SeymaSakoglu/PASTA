import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk
import threading
import queue
from datetime import datetime

from msf_manager import msf_baslat, msf_kapat, msf_baglan
from scanner import tara
from exploiter import exploit_calistir
from database import tablo_olustur, tum_taramalar, tarama_detay

BG_COLOR     = "#0a0e27"
FG_COLOR     = "#00ff41"
ACCENT_COLOR = "#00d9ff"
BUTTON_BG    = "#1a2332"
BUTTON_HOVER = "#2d3e50"
HEADER_BG    = "#0d1117"

HEDEF_IP      = "192.168.109.128"
KALI_IP       = "192.168.109.129"
HEDEF_PORTLAR = "21,22,80,139,445,1524,3306,3632,5900,6667"


class PastaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PASTA--")
        self.root.geometry("1450x850")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(True, True)

        self.msf = None
        self.kuyruk = queue.Queue()
        self.exploit_calisiyor = False

        self.baslik_olustur()
        self.altlik_olustur()
        self.menu_olustur()

        tablo_olustur()
        self.msf_baslat_thread()
        self.kuyruk_kontrol()

    def baslik_olustur(self):
        baslik = tk.Frame(self.root, bg=HEADER_BG, height=80)
        baslik.pack(fill=tk.X, side=tk.TOP)
        baslik.pack_propagate(False)

        tk.Label(baslik, text="PASTA",
                 font=("Courier New", 22, "bold"), fg=FG_COLOR, bg=HEADER_BG).pack(side=tk.LEFT, padx=20, pady=15)

        self.durum_label = tk.Label(
            baslik,
            text=f"DURUM: HAZIR | IP: {KALI_IP}",
            font=("Courier New", 12), fg=ACCENT_COLOR, bg=HEADER_BG
        )
        self.durum_label.pack(side=tk.RIGHT, padx=20, pady=15)

    def altlik_olustur(self):
        altlik = tk.Frame(self.root, bg=HEADER_BG, height=40)
        altlik.pack(fill=tk.X, side=tk.BOTTOM)
        altlik.pack_propagate(False)

        self.altlik_label = tk.Label(altlik, text="Hazir...",
                                     font=("Courier New", 12), fg=FG_COLOR, bg=HEADER_BG)
        self.altlik_label.pack(side=tk.LEFT, padx=20, pady=10)

    def menu_olustur(self):
        ana = tk.Frame(self.root, bg=BG_COLOR)
        ana.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        sol = tk.Frame(ana, bg=BG_COLOR, width=430)
        sol.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sol.pack_propagate(False)

        tk.Label(sol, text=f"Hedef: {HEDEF_IP}  |  Kali: {KALI_IP}",
                 font=("Courier New", 12), fg=FG_COLOR, bg=BG_COLOR).pack(pady=(0, 20))

        self.buton_ekle(sol, "1", "Metasploitable 2 Tara",  self.hizli_tara)
        self.buton_ekle(sol, "2", "Ozel Tara",              self.ozel_tara)
        self.buton_ekle(sol, "3", "Raporlari Goster",       self.raporlari_goster)
        self.buton_ekle(sol, "4", "Kanit Dosyalari",        self.kanitleri_goster)
        self.buton_ekle(sol, "5", "Cikis",                  self.cikis)

        sag = tk.Frame(ana, bg=BG_COLOR)
        sag.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(sag, text="TERMINAL",
                 font=("Courier New", 14, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(anchor=tk.W, pady=(0, 5))

        self.terminal = scrolledtext.ScrolledText(
            sag, bg="#000000", fg=FG_COLOR,
            font=("Courier New", 12), insertbackground=FG_COLOR,
            relief=tk.FLAT, borderwidth=2,
            highlightthickness=2, highlightbackground=FG_COLOR
        )
        self.terminal.pack(fill=tk.BOTH, expand=True)
        self.log("Sistem baslatildi.")

    def buton_ekle(self, parent, numara, yazi, komut):
        cerceve = tk.Frame(parent, bg=BUTTON_BG, highlightbackground=FG_COLOR, highlightthickness=1)
        cerceve.pack(fill=tk.X, pady=8, ipady=12, ipadx=15)

        ic = tk.Frame(cerceve, bg=BUTTON_BG)
        ic.pack(fill=tk.X)

        n = tk.Label(ic, text=f"[{numara}]", font=("Courier New", 14, "bold"),
                     fg=ACCENT_COLOR, bg=BUTTON_BG, width=4)
        n.pack(side=tk.LEFT)

        t = tk.Label(ic, text=yazi, font=("Courier New", 14), fg=FG_COLOR, bg=BUTTON_BG, anchor=tk.W)
        t.pack(side=tk.LEFT, fill=tk.X, expand=True)

        for w in [cerceve, ic, n, t]:
            w.bind("<Button-1>", lambda e: komut())
            w.bind("<Enter>",    lambda e: [x.configure(bg=BUTTON_HOVER) for x in [cerceve, ic, n, t]])
            w.bind("<Leave>",    lambda e: [x.configure(bg=BUTTON_BG)    for x in [cerceve, ic, n, t]])

    def log(self, mesaj):
        self.terminal.insert(tk.END, f"[>] {mesaj}\n")
        self.terminal.see(tk.END)

    def durum_guncelle(self, mesaj):
        self.durum_label.config(text=f"DURUM: {mesaj} | IP: {KALI_IP}")
        self.altlik_label.config(text=mesaj)

    def kuyruk_kontrol(self):
        try:
            while True:
                tip, mesaj = self.kuyruk.get_nowait()
                if tip == "log":
                    self.log(mesaj)
                elif tip == "durum":
                    self.durum_guncelle(mesaj)
        except queue.Empty:
            pass
        self.root.after(100, self.kuyruk_kontrol)

    def msf_baslat_thread(self):
        def calis():
            self.kuyruk.put(("log", "[*] Metasploit baslatiliyor..."))
            msf_baslat()
            self.msf = msf_baglan()
            if self.msf:
                self.kuyruk.put(("log", "[+] Metasploit hazir."))
                self.kuyruk.put(("durum", "HAZIR"))
            else:
                self.kuyruk.put(("log", "[-] Metasploit baglantisi basarisiz."))
        threading.Thread(target=calis, daemon=True).start()

    def hizli_tara(self):
        self.log("\n[1] Hizli tarama baslatiliyor...")
        self.durum_guncelle("TARANIYOR")

        def calis():
            try:
                tid, zafiyet_portlari = tara(HEDEF_IP, HEDEF_PORTLAR)
                self.kuyruk.put(("log", f"[+] Tarama bitti. ID: {tid}"))
                self.kuyruk.put(("log", f"[+] Zafiyetler: {zafiyet_portlari if zafiyet_portlari else 'YOK'}"))
                self.kuyruk.put(("durum", "HAZIR"))
                if zafiyet_portlari:
                    self.root.after(100, lambda: self.exploit_sor(HEDEF_IP, zafiyet_portlari))
            except Exception as e:
                self.kuyruk.put(("log", f"[-] Hata: {e}"))
                self.kuyruk.put(("durum", "HATA"))

        threading.Thread(target=calis, daemon=True).start()

    def ozel_tara(self):
        pencere = tk.Toplevel(self.root)
        pencere.title("Ozel Tarama")
        pencere.geometry("400x250")
        pencere.configure(bg=BG_COLOR)

        tk.Label(pencere, text="Hedef IP:", font=("Courier New", 13), fg=FG_COLOR, bg=BG_COLOR).pack(pady=(20, 5))
        ip_giris = tk.Entry(pencere, font=("Courier New", 13), bg=BUTTON_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
        ip_giris.pack(ipadx=10, ipady=4)

        tk.Label(pencere, text="Portlar (orn: 21,80,443):", font=("Courier New", 12), fg=FG_COLOR, bg=BG_COLOR).pack(pady=(15, 5))
        port_giris = tk.Entry(pencere, font=("Courier New", 12), bg=BUTTON_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
        port_giris.pack(ipadx=10, ipady=4)

        def baslat():
            ip = ip_giris.get().strip()
            p  = port_giris.get().strip()
            if not ip or not p:
                messagebox.showerror("Hata", "IP ve port bos olamaz!")
                return
            pencere.destroy()
            self.log(f"[*] Ozel tarama: {ip} -> {p}")
            self.durum_guncelle("TARANIYOR")

            def calis():
                try:
                    tid, zafiyet_portlari = tara(ip, p)
                    self.kuyruk.put(("log", f"[+] Tarama bitti. ID: {tid}"))
                    self.kuyruk.put(("log", f"[+] Zafiyetler: {zafiyet_portlari}"))
                    self.kuyruk.put(("durum", "HAZIR"))
                    if zafiyet_portlari:
                        self.root.after(100, lambda: self.exploit_sor(ip, zafiyet_portlari))
                except Exception as e:
                    self.kuyruk.put(("log", f"[-] Hata: {e}"))
                    self.kuyruk.put(("durum", "HATA"))

            threading.Thread(target=calis, daemon=True).start()

        tk.Button(pencere, text="Tara", command=baslat,
                  bg=BUTTON_BG, fg=FG_COLOR, font=("Courier New", 12), relief=tk.FLAT).pack(pady=20, ipady=5, ipadx=15)

    def exploit_sor(self, ip, zafiyet_portlari):
        if self.exploit_calisiyor:
            return
        cevap = messagebox.askyesno("Exploit", f"Zafiyetli portlar: {zafiyet_portlari}\nExploit denensin mi?")
        if not cevap:
            return

        self.exploit_calisiyor = True
        self.durum_guncelle("EXPLOIT")

        def calis():
            import builtins
            original = builtins.print
            def yeni_print(*args, **kwargs):
                self.kuyruk.put(("log", " ".join(str(a) for a in args)))
                original(*args, **kwargs)
            builtins.print = yeni_print
            try:
                exploit_calistir(self.msf, ip, zafiyet_portlari)
            except Exception as e:
                self.kuyruk.put(("log", f"[-] Exploit hatasi: {e}"))
            finally:
                builtins.print = original
                self.exploit_calisiyor = False
                self.kuyruk.put(("durum", "HAZIR"))

        threading.Thread(target=calis, daemon=True).start()

    def raporlari_goster(self):
        taramalar = tum_taramalar()
        if not taramalar:
            messagebox.showinfo("Raporlar", "Henuz tarama yapilmamis.")
            return

        pencere = tk.Toplevel(self.root)
        pencere.title("Gecmis Taramalar")
        pencere.geometry("900x500")
        pencere.configure(bg=BG_COLOR)

        tk.Label(pencere, text="TARAMA GECMISI",
                 font=("Courier New", 15, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=10)

        stil = ttk.Style()
        stil.theme_use("clam")
        stil.configure("Treeview", background="#1a1a1a", foreground=FG_COLOR,
                       fieldbackground="#1a1a1a", font=("Courier New", 11))
        stil.configure("Treeview.Heading", background=BUTTON_BG,
                       foreground=ACCENT_COLOR, font=("Courier New", 11, "bold"))

        tree = ttk.Treeview(pencere, columns=("ID", "IP", "Portlar", "Tarih", "Durum"), show="headings")
        for col, w in [("ID", 50), ("IP", 140), ("Portlar", 200), ("Tarih", 160), ("Durum", 100)]:
            tree.heading(col, text=col)
            tree.column(col, width=w)
        for t in taramalar:
            tree.insert("", tk.END, values=(t[0], t[1], t[2], t[3], t[4]))
        tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        def detay_goster():
            secim = tree.selection()
            if not secim:
                return
            tid = tree.item(secim[0])["values"][0]
            portlar, zafiyetler = tarama_detay(tid)

            d = tk.Toplevel(pencere)
            d.title(f"Detay - ID {tid}")
            d.geometry("900x600")
            d.configure(bg=BG_COLOR)

            alan = scrolledtext.ScrolledText(d, bg="#000000", fg=FG_COLOR, font=("Courier New", 11))
            alan.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

            alan.insert(tk.END, f"=== TARAMA ID: {tid} ===\n\nPORTLAR:\n")
            for p in portlar:
                alan.insert(tk.END, f"  {p[2]}/tcp | {p[3]} {p[4]} {p[5]} | {p[6]}\n")
            alan.insert(tk.END, "\nZAFIYETLER:\n")
            if zafiyetler:
                for z in zafiyetler:
                    alan.insert(tk.END, f"  Port {z[2]} | {z[3]} | {str(z[4])[:120]}\n")
            else:
                alan.insert(tk.END, "  Zafiyet bulunamadi.\n")
            alan.config(state=tk.DISABLED)

        tk.Button(pencere, text="Detay Goster", command=detay_goster,
                  bg=BUTTON_BG, fg=FG_COLOR, font=("Courier New", 12), relief=tk.FLAT).pack(pady=10)

    def kanitleri_goster(self):
        klasor = "kanitlar"
        if not os.path.exists(klasor):
            messagebox.showwarning("Uyari", "kanitlar klasoru bulunamadi.")
            return

        pencere = tk.Toplevel(self.root)
        pencere.title("Kanit Dosyalari")
        pencere.geometry("1000x600")
        pencere.configure(bg=BG_COLOR)

        sol = tk.Frame(pencere, bg=BG_COLOR)
        sol.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        sag = tk.Frame(pencere, bg=BG_COLOR)
        sag.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        liste = tk.Listbox(sol, width=40, height=30, bg="#000000", fg=FG_COLOR, font=("Courier New", 11))
        liste.pack()

        metin = tk.Text(sag, wrap="word", bg="#000000", fg=FG_COLOR, font=("Courier New", 11))
        metin.pack(fill=tk.BOTH, expand=True)

        resim_label = tk.Label(sag, bg=BG_COLOR)
        resim_label.pack(pady=5)

        for d in sorted(os.listdir(klasor), reverse=True):
            if d.endswith(".txt") or d.endswith(".png"):
                liste.insert(tk.END, d)

        def dosya_ac(e=None):
            secim = liste.curselection()
            if not secim:
                return
            ad  = liste.get(secim[0])
            yol = os.path.join(klasor, ad)
            metin.delete("1.0", tk.END)
            resim_label.config(image="")
            resim_label.image = None

            if ad.endswith(".txt"):
                with open(yol, "r", encoding="utf-8", errors="ignore") as f:
                    metin.insert(tk.END, f.read())
            elif ad.endswith(".png"):
                img = Image.open(yol)
                img.thumbnail((700, 400))
                foto = ImageTk.PhotoImage(img)
                resim_label.config(image=foto)
                resim_label.image = foto

        liste.bind("<<ListboxSelect>>", dosya_ac)

    def cikis(self):
        if self.exploit_calisiyor:
            messagebox.showwarning("Uyari", "Exploit devam ediyor!")
            return
        msf_kapat()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app  = PastaGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.cikis)
    root.mainloop()