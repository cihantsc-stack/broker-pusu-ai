from __future__ import annotations
from datetime import datetime, time, timedelta
import pandas as pd

from data.market_data import get_history
from analysis.indicators import add_indicators
from analysis.levels import calculate_levels

# Tam BIST100 taraması ücretsiz kaynaklarda yavaş/rate-limit yapabilir.
# Bu liste günlük trade için likit ve sık işlem gören aday havuzudur.
SCAN_SYMBOLS = [
    'THYAO','ASELS','TUPRS','KCHOL','AKBNK','GARAN','ISCTR','YKBNK','EREGL','BIMAS',
    'FROTO','TOASO','SAHOL','SISE','PETKM','KOZAL','PGSUS','TCELL','ENKAI','ARCLK',
    'EKGYO','DOAS','ALARK','HEKTS','SASA','KRDMD','GUBRF','ODAS','MGROS','ULKER'
]


def daily_key(now: datetime | None = None) -> str:
    now = now or datetime.now()
    # Her gün 09:45 sonrası yeni liste; 09:45 öncesi önceki iş gününün anahtarı.
    if now.time() < time(9, 45):
        d = now.date() - timedelta(days=1)
    else:
        d = now.date()
    return d.isoformat()


def _score_symbol(symbol: str):
    df, is_demo, msg = get_history(symbol, period='6mo', interval='1d')
    if df is None or df.empty or len(df) < 60:
        return None
    df = add_indicators(df)
    levels = calculate_levels(df)
    last = levels['last']
    rsi = float(df['RSI'].iloc[-1])
    ema20 = float(df['EMA20'].iloc[-1])
    ema50 = float(df['EMA50'].iloc[-1])
    vol = float(df['Volume'].iloc[-1])
    volma = float(df['VOL_MA20'].iloc[-1]) if not pd.isna(df['VOL_MA20'].iloc[-1]) else vol
    high20_prev = float(df['High'].shift(1).tail(20).max())

    momentum = 0
    reason = 'Teknik görünüm izleniyor'
    if last > ema20:
        momentum += 20
    if ema20 > ema50:
        momentum += 20
    if vol > volma * 1.15:
        momentum += 20
        reason = 'Hacim destekli hareket bekleniyor'
    if last >= high20_prev * 0.985:
        momentum += 25
        reason = 'Momentum kırılımı bekleniyor'
    if 38 <= rsi <= 65:
        momentum += 15
    if rsi > 72:
        momentum -= 20
        reason = 'Yükseliş var ama şişkinlik riski izlenmeli'

    return {
        'symbol': symbol,
        'reason': reason,
        'entry': levels['buy_high'],
        'target': levels['resistance'],
        'stop': levels['stop'],
        'score': int(max(0, min(100, momentum))),
    }


def get_daily_trade_picks(limit=3):
    picks = []
    for sym in SCAN_SYMBOLS:
        try:
            item = _score_symbol(sym)
            if item:
                picks.append(item)
        except Exception:
            continue
    picks = sorted(picks, key=lambda x: x['score'], reverse=True)
    return picks[:limit]
