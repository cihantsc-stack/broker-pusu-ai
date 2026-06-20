import numpy as np


def _pivot_low(df, lookback=35):
    recent = df.tail(lookback)
    return float(recent['Low'].min())


def _pivot_high(df, lookback=55):
    recent = df.tail(lookback)
    return float(recent['High'].max())


def calculate_levels(df):
    """Pratik işlem seviyeleri.

    Mantık: stop-loss "batınca çık" seviyesi değildir. Destek bozulursa zararı
    büyütmeden sınırlama alanıdır. Bu yüzden stop anlık fiyattan gereksiz uzak
    bırakılmaz; ATR + yakın destek + maksimum risk sınırı birlikte kullanılır.
    """
    last = float(df['Close'].iloc[-1])
    atr = float(df['ATR'].iloc[-1]) if 'ATR' in df and not np.isnan(df['ATR'].iloc[-1]) else last * 0.022

    raw_support = _pivot_low(df, 35)
    recent_support = float(df.tail(20)['Low'].min())
    resistance_raw = _pivot_high(df, 55)

    # Kullanılabilir destek: son büyük dip çok uzaktaysa daha yakın 20 günlük dip kullanılır.
    support = raw_support
    if (last - support) / last > 0.065:
        support = recent_support

    # Stop üç güvenlik kuralına göre seçilir:
    # 1) desteğin az altı, 2) ATR ile makul pay, 3) en fazla yaklaşık %3,5-4 risk.
    stop_by_support = support - atr * 0.18
    stop_by_atr = last - atr * 1.25
    max_loss_stop = last * 0.965
    stop = max(stop_by_support, stop_by_atr, max_loss_stop)
    stop = min(stop, last * 0.992)  # stop anlık fiyata yapışmasın ama fiyatın üstüne çıkmasın

    resistance = resistance_raw
    if resistance <= last * 1.012:
        resistance = last + atr * 2.6

    buy_low = max(support, last - atr * 0.45)
    buy_high = min(last + atr * 0.18, resistance * 0.995)

    return {
        'last': last,
        'support': support,
        'resistance': resistance,
        'stop': stop,
        'atr': atr,
        'buy_low': buy_low,
        'buy_high': buy_high,
    }
