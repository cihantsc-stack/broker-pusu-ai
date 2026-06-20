from __future__ import annotations
import time
from datetime import datetime, timezone
import pandas as pd
import requests
import yfinance as yf


def normalize_symbol(symbol: str) -> str:
    s = (symbol or '').upper().strip().replace(' ', '')
    if not s:
        return 'ASELS.IS'
    return s if s.endswith('.IS') or s.startswith('^') or s.startswith('F_') else f'{s}.IS'


def _empty() -> pd.DataFrame:
    return pd.DataFrame(columns=['Open','High','Low','Close','Volume'])


def _from_yahoo_chart(ticker: str, range_: str = '1y', interval: str = '1d') -> pd.DataFrame:
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'
    params = {'range': range_, 'interval': interval, 'includePrePost': 'false', 'events': 'div,splits'}
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, params=params, headers=headers, timeout=12)
    r.raise_for_status()
    data = r.json()
    result = data.get('chart', {}).get('result') or []
    if not result:
        return _empty()
    res = result[0]
    timestamps = res.get('timestamp') or []
    quote = (res.get('indicators', {}).get('quote') or [{}])[0]
    if not timestamps or not quote:
        return _empty()
    df = pd.DataFrame({
        'Open': quote.get('open'),
        'High': quote.get('high'),
        'Low': quote.get('low'),
        'Close': quote.get('close'),
        'Volume': quote.get('volume'),
    }, index=pd.to_datetime(timestamps, unit='s'))
    df = df.dropna(subset=['Open','High','Low','Close'])
    if 'Volume' in df:
        df['Volume'] = df['Volume'].fillna(0)
    return df


def get_history(symbol: str, period: str='1y', interval: str='1d') -> tuple[pd.DataFrame, bool, str]:
    """Return (df, is_demo, message). v3.2 never produces fake prices.
    If free data fails, it returns an empty dataframe and the UI stops analysis.
    """
    ticker = normalize_symbol(symbol)
    try:
        df = _from_yahoo_chart(ticker, range_=period, interval=interval)
        if df is not None and len(df) >= 60:
            return df, False, f'Gerçek veri kullanılıyor: {ticker}'
    except Exception:
        pass
    try:
        df = yf.Ticker(ticker).history(period=period, interval=interval, auto_adjust=False)
        if df is not None and len(df) >= 60:
            cols = [c for c in ['Open','High','Low','Close','Volume'] if c in df.columns]
            return df[cols].dropna(), False, f'Gerçek veri kullanılıyor: {ticker}'
    except Exception as e:
        return _empty(), False, f'Ücretsiz veri kaynağı geçici yanıt vermedi: {type(e).__name__}'
    return _empty(), False, 'Bu sembol için yeterli gerçek veri alınamadı. Demo fiyat gösterilmedi.'


def get_index_snapshot() -> dict:
    items = {'BIST100':'XU100.IS', 'BIST30':'XU030.IS', 'VİOP':'F_XU0300226.IS'}
    out = {}
    for name, sym in items.items():
        df, demo, msg = get_history(sym, period='5d')
        if len(df) >= 2:
            last = float(df['Close'].iloc[-1]); prev = float(df['Close'].iloc[-2]); ch = (last-prev)/prev*100 if prev else 0
            ok = True
        else:
            last, ch, ok = None, None, False
        out[name] = {'value': last, 'change': ch, 'ok': ok, 'msg': msg}
    return out
