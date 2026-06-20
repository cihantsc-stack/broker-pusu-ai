# Broker Pusu AI v3.4

Bu sürümde:

- Streamlit Cloud için `runtime.txt` eklendi, Python 3.12 sabitlendi.
- Grafik fiyat etiketleri büyütüldü ve sağ tarafta daha görünür hale getirildi.
- Stop-loss metni “Zarar Kes” olarak güncellendi.
- Stop mantığı daha yakın ve pratik hale getirildi: destek + ATR + maksimum risk sınırı birlikte kullanılır.
- Sabah günlük trade adayları cache edildi; ekran sürekli tarama yapıp yavaşlamaz.
- Ekran otomatik yenilenmez, sabit kalır.

Kurulum:
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```
