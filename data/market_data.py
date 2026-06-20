from __future__ import annotations

import pandas as pd
import requests
import yfinance as yf


def normalize_symbol(symbol: str) -> str:
    s = (symbol or "").upper().strip().replace(" ", "")
    if not s:
        return "ASELS.IS"
    return s if s.endswith(".IS") or s.startswith("^") or s.startswith("F_") else f"{s}.IS"


def _empty() -> pd.DataFrame:
    return pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])


def _from_yahoo_chart(ticker: str, range_: str = "1y", interval: str = "1d") -> pd.DataFrame:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"

    params = {
        "range": range_,
        "interval": interval,
        "includePrePost": "false",
        "events": "div,splits",
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, params=params, headers=headers, timeout=15)
    r.raise_for_status()

    data = r.json()

    result = data.get("chart", {}).get("result") or []

    if not result:
        return _empty()

    res = result[0]

    timestamps = res.get("timestamp") or []

    quote = (res.get("indicators", {}).get("quote") or [{}])[0]

    if not timestamps:
        return _empty()

    df = pd.DataFrame(
        {
            "Open": quote.get("open"),
            "High": quote.get("high"),
            "Low": quote.get("low"),
            "Close": quote.get("close"),
            "Volume": quote.get("volume"),
        },
        index=pd.to_datetime(timestamps, unit="s"),
    )

    df = df.dropna(subset=["Open", "High", "Low", "Close"])

    if "Volume" in df.columns:
        df["Volume"] = df["Volume"].fillna(0)

    return df


def get_history(symbol: str, period: str = "1y", interval: str = "1d"):
    ticker = normalize_symbol(symbol)

    try:
        df = _from_yahoo_chart(ticker, range_=period, interval=interval)

        if len(df) >= 20:
            return df, False, f"Gerçek veri: {ticker}"

    except Exception:
        pass

    try:
        df = yf.Ticker(ticker).history(
            period=period,
            interval=interval,
            auto_adjust=False,
        )

        if len(df) >= 20:
            cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
            return df[cols].dropna(), False, f"Gerçek veri: {ticker}"

    except Exception:
        pass

    return _empty(), False, "Veri alınamadı"


def _try_symbols(symbols):
    for sym in symbols:

        try:
            df = _from_yahoo_chart(sym, range_="10d", interval="1d")

            if len(df) >= 2:
                return df, sym

        except Exception:
            pass

        try:
            df = yf.Ticker(sym).history(
                period="10d",
                interval="1d",
                auto_adjust=False,
            )

            if len(df) >= 2:
                cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
                return df[cols].dropna(), sym

        except Exception:
            pass

    return _empty(), None


def get_index_snapshot():

    sources = {
        "BIST100": ["^XU100", "XU100.IS"],
        "BIST30": ["^XU030", "XU030.IS"],
        "VİOP": ["F_XU0300226.IS", "^XU030", "XU030.IS"],
    }

    result = {}

    for name, symbols in sources.items():

        df, used = _try_symbols(symbols)

        if len(df) >= 2:

            last = float(df["Close"].iloc[-1])
            prev = float(df["Close"].iloc[-2])

            change = ((last - prev) / prev) * 100 if prev else 0

            result[name] = {
                "value": last,
                "change": change,
                "ok": True,
                "msg": f"Son kapanış ({used})",
            }

        else:

            result[name] = {
                "value": None,
                "change": None,
                "ok": False,
                "msg": "Veri alınamadı",
            }

    return result
