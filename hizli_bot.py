import yfinance as yf
import pandas as pd
import requests

TOKEN = "9059337535:AAGOV1YLbc38UIMdzzF_sHRQwF8y8pg-oGY"
CHAT_ID = "8786222371"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {e}")

def hizli_al_sat_taramasi():
    hizli_takip_listesi = [
        "THYAO.IS", "ASELS.IS", "EREGL.IS", "KCHOL.IS", 
        "SAHOL.IS", "YKBNK.IS", "AKBNK.IS", "KRDMD.IS", "PETKM.IS", "SISE.IS"
    ]
    
    rapor = "🚀 **GÜNLÜK HIZLI AL-SAT & HACİM PATLAMASI RAPORU**\n"
    rapor += "━━━━━━━━━━━━━━━━━━━\n\n"
    patlama_sayisi = 0
    
    for hisse in hizli_takip_listesi:
        try:
            data = yf.download(hisse, period="10d", interval="1d", progress=False)
            if len(data) >= 5:
                c_col = data['Close']
                v_col = data['Volume']
                son_fiyat = float(c_col.iloc[-1].item() if hasattr(c_col.iloc[-1], 'item') else c_col.iloc[-1])
                gunluk_hacim = float(v_col.iloc[-1].item() if hasattr(v_col.iloc[-1], 'item') else v_col.iloc[-1])
                ortalama_hacim = float(v_col.tail(5).mean().item() if hasattr(v_col.tail(5).mean(), 'item') else v_col.tail(5).mean())
                
                if gunluk_hacim > (ortalama_hacim * 1.5):
                    rapor += f"🔥 `{hisse}`: **Hacim Patlaması!**\n"
                    rapor += f"   • Fiyat: `{son_fiyat:.2f} TL`\n"
                    rapor += f"   • Hacim: Normalin Üzerinde ⚡\n\n"
                    patlama_sayisi += 1
                else:
                    rapor += f"▫️ `{hisse}`: `{son_fiyat:.2f} TL` (Normal)\n"
        except Exception:
            continue
            
    if patlama_sayisi == 0:
        rapor += "• Bugün belirgin bir hacim patlaması tespit edilmedi.\n\n"
        
    rapor += "━━━━━━━━━━━━━━━━━━━\n"
    rapor += "🤖 *GitHub Actions - İkinci Tarama Botu*"
    return rapor

if __name__ == "__main__":
    print("Hızlı al-sat tarama botu çalıştırılıyor...")
    mesaj = hizli_al_sat_taramasi()
    send_telegram_message(mesaj)
    print("Hızlı tarama raporu Telegram'a gönderildi.")
