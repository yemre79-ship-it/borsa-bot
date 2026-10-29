import requests
import yfinance as yf

# 1. Telegram Ayarları
TELEGRAM_TOKEN = "9059337535:AAGOV1YLbc38UIMdzzF_sHRQwF8y8pg-oGY"
CHAT_ID = "8786222371"

# 2. Taranacak BIST Hisseleri (50 TL Altı Fırsat Adayları ve Öncüler)
bist_hisseleri = [
    "AKBNK.IS", "YKBNK.IS", "ISCTR.IS", "EKGYO.IS", "SASA.IS", 
    "HEKTS.IS", "EREGL.IS", "KRDMD.IS", "PETKM.IS", "ODAS.IS", 
    "SKBNK.IS", "TSKB.IS", "HALKB.IS", "GARAN.IS", "THYAO.IS", "TUPRS.IS"
]

# Özel Derin Analiz Yapılacak Kilit Hisse
kilit_hisse = "ASELS.IS"
kilit_hisse_bilgi = ""
firsat_hisseleri = []

print("BIST taraması ve özel analiz gerçekleştiriliyor...")

# 3. Kilit Hisse (ASELSAN) Derin Analizi
try:
    asels_data = yf.download(kilit_hisse, period="6mo", interval="1d", progress=False)
    if len(asels_data) > 15:
        asels_data["SMA_10"] = asels_data["Close"].rolling(10).mean()
        asels_fiyat = float(asels_data["Close"].iloc[-1].item())
        asels_sma = float(asels_data["SMA_10"].iloc[-1].item())
        
        durum_asels = "SMA10 Üzerinde (Pozitif Eğilim)" if asels_fiyat > asels_sma else "SMA10 Altında (Temkinli)"
        kilit_hisse_bilgi = f"⭐ Kilit Takip ({kilit_hisse})\n• Fiyat: {asels_fiyat:.2f} TL\n• 10 Günlük Ort: {asels_sma:.2f} TL\n• Durum: {durum_asels}"
except Exception as e:
    kilit_hisse_bilgi = f"⭐ Kilit Takip ({kilit_hisse}): Veri alınamadı."

# 4. 50 TL Altı Fırsat Taraması
for hisse in bist_hisseleri:
    try:
        data = yf.download(hisse, period="6mo", interval="1d", progress=False)
        if len(data) > 15:
            data["SMA_10"] = data["Close"].rolling(10).mean()
            
            son_fiyat = float(data["Close"].iloc[-1].item())
            sma_10 = float(data["SMA_10"].iloc[-1].item())
            
            # Kriter: Fiyat 50 TL'den az VE 10 günlük ortalamanın üstünde
            if son_fiyat < 50 and son_fiyat > sma_10:
                firsat_hisseleri.append(f"🟢 {hisse}: {son_fiyat:.2f} TL (SMA10: {sma_10:.2f} TL)")
    except Exception as e:
        print(f"{hisse} taranamadı: {e}")

# 5. Telegram Mesajı Birleştirme
mesaj_parcalari = ["🤖 Forever Sinyal Botu - Günlük Analiz Raporu\n"]

if kilit_hisse_bilgi:
    mesaj_parcalari.append(kilit_hisse_bilgi)
    mesaj_parcalari.append("----------------------------")

if firsat_hisseleri:
    liste_str = "\n".join(firsat_hisseleri)
    mesaj_parcalari.append(f"📌 50 TL Altındaki Fırsat Adayları (SMA10 Üstü):\n\n{liste_str}")
else:
    mesaj_parcalari.append("📌 50 TL altında ve SMA10 üzerinde kriterlere uyan hisse bulunamadı.")

mesaj = "\n".join(mesaj_parcalari)

# 6. Telegram'a Gönderme Komutu
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": mesaj
}
response = requests.post(url, json=payload)

print("Telegram Yanıtı:", response.text)