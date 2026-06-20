import numpy as np


def make_decision(df, levels):
    last = levels['last']; support = levels['support']; resistance = levels['resistance']; stop = levels['stop']
    rsi = float(df['RSI'].iloc[-1]) if 'RSI' in df else 50
    ema20 = float(df['EMA20'].iloc[-1]); ema50 = float(df['EMA50'].iloc[-1]); ema200 = float(df['EMA200'].iloc[-1]) if not np.isnan(df['EMA200'].iloc[-1]) else ema50
    macd_hist = float(df['MACD_HIST'].iloc[-1])
    vol = float(df['Volume'].iloc[-1]); volma = float(df['VOL_MA20'].iloc[-1]) if not np.isnan(df['VOL_MA20'].iloc[-1]) else vol

    score = 50
    reasons_good, reasons_bad = [], []
    if last > ema20: score += 9; reasons_good.append('Fiyat kısa vadeli ortalamanın üzerinde.')
    else: score -= 8; reasons_bad.append('Fiyat kısa vadeli ortalamanın altında.')
    if ema20 > ema50: score += 10; reasons_good.append('Kısa trend orta trendden güçlü.')
    else: score -= 8; reasons_bad.append('Kısa trend zayıf görünüyor.')
    if last > ema200: score += 8; reasons_good.append('Ana trend yukarı tarafta.')
    else: score -= 6; reasons_bad.append('Ana trend tarafında dikkat gerekiyor.')
    if 35 <= rsi <= 62: score += 8; reasons_good.append('RSI aşırı pahalı bölgede değil.')
    elif rsi > 70: score -= 16; reasons_bad.append('RSI aşırı şişkin bölgede.')
    elif rsi < 30: score += 4; reasons_good.append('RSI ucuz bölgede, tepki ihtimali var.')
    if macd_hist > 0: score += 7; reasons_good.append('MACD momentumu pozitif.')
    else: score -= 5; reasons_bad.append('MACD momentumu zayıf.')
    if vol > volma * 1.2: score += 6; reasons_good.append('Hacim ortalamanın üzerinde, ilgi artmış.')
    distance_to_support = abs(last - support) / last * 100
    if distance_to_support <= 4: score += 8; reasons_good.append('Fiyat destek bölgesine yakın.')
    if last >= resistance * 0.97: score -= 15; reasons_bad.append('Fiyat dirence çok yakın, yeni alım riskli.')

    score = int(max(0, min(100, score)))
    risk_pct = max(0.1, (last - stop) / last * 100)
    reward_pct = max(0.1, (resistance - last) / last * 100)
    rr = reward_pct / risk_pct

    if score >= 72 and rr >= 1.7:
        signal, color, subtitle = 'ALINABİLİR', 'green', 'Ama stop seviyesine sadık kalınmalı.'
    elif score >= 55:
        signal, color, subtitle = 'BEKLE / İZLE', 'yellow', 'Aceleyi bırak, daha iyi giriş beklenebilir.'
    else:
        signal, color, subtitle = 'ALMA', 'red', 'Risk/kazanç dengesi şu an zayıf.'

    trade = 'Uygun' if score >= 68 and rr >= 1.5 else ('Riskli' if score >= 50 else 'Uygun değil')
    mid = 'İzlenebilir' if score >= 55 else 'Zayıf'
    long = 'Güçlü aday' if last > ema200 and score >= 65 else ('Nötr' if score >= 50 else 'Zayıf')

    return {'score': score, 'signal': signal, 'color': color, 'subtitle': subtitle, 'risk_pct': risk_pct, 'reward_pct': reward_pct, 'rr': rr, 'good': reasons_good[:5], 'bad': reasons_bad[:4], 'trade': trade, 'mid': mid, 'long': long}
