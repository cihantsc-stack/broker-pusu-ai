import numpy as np


def _pivot_low(df, lookback=35):
    recent = df.tail(lookback)
    return float(recent['Low'].min())


def _pivot_high(df, lookback=55):
    recent = df.tail(lookback)
    return float(recent['High'].max())


def calculate_levels(df):
    """Pratik işlem seviyeleri.

    Stop-loss mantığı: batınca çık değil; son destek aşağı kırılırsa zararı sınırlama.
    Bu yüzden stop, desteğin hemen altına konur ve anlık fiyattan aşırı uzaklaştırılmaz.
    """
    last = float(df['Close'].iloc[-1])
    atr = float(df['ATR'].iloc[-1]) if 'ATR' in df and not np.isnan(df['ATR'].iloc[-1]) else last * 0.025

    support_raw = _pivot_low(df, 35)
    resistance_raw = _pivot_high(df, 55)

    # Destek çok uzaktaysa daha yakın pratik destek kullanılır.
    support = support_raw
    if (last - support) / last > 0.075:
        support = float(df.tail(20)['Low'].min())

    # Stop: desteğin az altı, ama anlık fiyattan aşırı uzak değil.
    stop_by_support = support - atr * 0.25
    stop_max_loss = last * 0.955  # yaklaşık en fazla %4,5 risk alanı
    stop = max(stop_by_support, stop_max_loss)
    stop = min(stop, last * 0.985)  # stop anlık fiyatın üstüne/yakınına taşmasın

    resistance = resistance_raw
    if resistance <= last * 1.01:
        resistance = last + atr * 2.8

    buy_low = max(support, last - atr * 0.6)
    buy_high = min(last + atr * 0.25, resistance)

    return {
        'last': last,
        'support': support,
        'resistance': resistance,
        'stop': stop,
        'atr': atr,
        'buy_low': buy_low,
        'buy_high': buy_high,
    }
