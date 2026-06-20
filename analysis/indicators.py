import numpy as np
import pandas as pd


def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()


def rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    return 100 - (100 / (1 + rs))


def atr(df, period=14):
    high, low, close = df['High'], df['Low'], df['Close']
    prev_close = close.shift(1)
    tr = pd.concat([(high-low), (high-prev_close).abs(), (low-prev_close).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1/period, min_periods=period, adjust=False).mean()


def macd(close):
    line = ema(close, 12) - ema(close, 26)
    signal = line.ewm(span=9, adjust=False).mean()
    hist = line - signal
    return line, signal, hist


def add_indicators(df):
    d = df.copy()
    d['EMA20'] = ema(d['Close'], 20)
    d['EMA50'] = ema(d['Close'], 50)
    d['EMA100'] = ema(d['Close'], 100)
    d['EMA200'] = ema(d['Close'], 200)
    d['RSI'] = rsi(d['Close'])
    d['ATR'] = atr(d)
    macd_line, macd_signal, macd_hist = macd(d['Close'])
    d['MACD'] = macd_line
    d['MACD_SIGNAL'] = macd_signal
    d['MACD_HIST'] = macd_hist
    d['VOL_MA20'] = d['Volume'].rolling(20).mean()
    return d


def moving_average_report(df):
    last = float(df['Close'].iloc[-1])
    rows = []
    for label in ['EMA20','EMA50','EMA100','EMA200']:
        val = float(df[label].iloc[-1]) if label in df and not pd.isna(df[label].iloc[-1]) else np.nan
        rows.append({'Ortalama': label, 'Değer': round(val, 2), 'Durum': 'ÜSTÜNDE ✅' if last > val else 'ALTINDA ⚠️'})
    return pd.DataFrame(rows)
