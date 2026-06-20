# Broker Pusu AI v3.3

Düzeltmeler:
- Ekran otomatik yenilenmez, sabit kalır.
- Stop-loss mantığı daha makul hale getirildi: batınca çık değil, destek bozulursa zararı sınırlama.
- Grafik çizgi fiyat etiketleri sağ tarafta kalıcı görünür.
- BIST100/BIST30/VİOP sonrası günlük trade yapılabilecek 3 aday kartı eklendi.
- Günlük trade adayları her gün 09:45 sonrası yeni günlük anahtarla hesaplanır.
- “Para hesabı” başlığı “Yatırım olası sonuçları” olarak düzeltildi.

Çalıştırma:
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```
