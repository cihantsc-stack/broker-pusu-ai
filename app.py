from datetime import datetime
import streamlit as st

from ui.styles import apply_styles
from ui.charts import candle_chart
from data.market_data import get_history, get_index_snapshot
from data.news import get_news
from data.scanner import get_daily_trade_picks, daily_key
from analysis.indicators import add_indicators, moving_average_report
from analysis.levels import calculate_levels
from analysis.decision_engine import make_decision
from storage.favorites import load_favorites, toggle

st.set_page_config(page_title='Broker Pusu AI v3.4', page_icon='🦅', layout='wide')
apply_styles()


def money(x):
    try: return f'{x:,.2f} TL'.replace(',', 'X').replace('.', ',').replace('X','.')
    except Exception: return '-'


def pct(x):
    return f'{x:+.2f}%'.replace('.', ',')



@st.cache_data(ttl=900, show_spinner=False)
def cached_history(symbol: str):
    return get_history(symbol)


@st.cache_data(ttl=900, show_spinner=False)
def cached_index_snapshot():
    return get_index_snapshot()


@st.cache_data(ttl=3600, show_spinner=False)
def cached_trade_picks(key: str):
    return get_daily_trade_picks(3)


def metric_box(label, value, klass=''):
    st.markdown(f'<div class="metricbox"><div class="metric-label">{label}</div><div class="metric-value {klass}">{value}</div></div>', unsafe_allow_html=True)


def decision_card(decision):
    klass = {'green':'decision-green','yellow':'decision-yellow','red':'decision-red'}[decision['color']]
    icon = {'green':'🟢','yellow':'🟡','red':'🔴'}[decision['color']]
    st.markdown(f'''
    <div class="decision {klass}">
        <div class="decision-title">{icon} {decision['signal']}</div>
        <div class="decision-sub">{decision['subtitle']}</div>
        <div style="margin-top:18px">
            <span class="pill">AI Güven Skoru: {decision['score']}/100</span>
            <span class="pill">Trade: {decision['trade']}</span>
            <span class="pill">Orta Vade: {decision['mid']}</span>
            <span class="pill">Uzun Vade: {decision['long']}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def main():
    with st.sidebar:
        st.markdown('## 🦅 Broker Pusu AI')
        st.markdown('<div class="tiny">Borsadan anlamayan kullanıcı için sade karar ekranı.</div>', unsafe_allow_html=True)
        st.markdown('---')
        if st.button('🔄 Verileri yenile'):
            st.cache_data.clear()
            st.rerun()
        favs = load_favorites()
        st.markdown('### ⭐ İzleme Listem')
        if favs:
            for f in favs: st.markdown(f'- {f}')
        else:
            st.caption('Henüz favori yok.')
        st.markdown('---')
        st.markdown('<div class="ytd">YTD: Bu uygulama yatırım tavsiyesi vermez. Eğitim ve karar destek amaçlıdır. Al/sat kararı ve risk kullanıcıya aittir.</div>', unsafe_allow_html=True)

    st.markdown('<div class="hero"><h1>🦅 Broker Pusu AI v3.4</h1><div class="tiny">Hisseyi seç, uygulama sana sade Türkçe ile risk, destek, direnç, stop ve karar özeti versin.</div></div>', unsafe_allow_html=True)
    st.write('')

    top1, top2, top3, top4 = st.columns(4)
    snap = cached_index_snapshot()
    with top1: metric_box('CANLI SAAT', datetime.now().strftime('%H:%M:%S'), 'blue')
    def idx_text(key):
        item = snap[key]
        if not item.get('ok'):
            return 'Veri alınamadı', 'warn'
        klass = 'good' if item['change'] >= 0 else 'bad'
        return f"{item['value']:,.0f}  {pct(item['change'])}", klass
    t, k = idx_text('BIST100')
    with top2: metric_box('BIST100', t, k)
    t, k = idx_text('BIST30')
    with top3: metric_box('BIST30', t, k)
    t, k = idx_text('VİOP')
    with top4: metric_box('VİOP', t, k)

    st.write('')
    st.markdown('### ☀️ Sabah Günlük Trade Adayları')
    st.caption(f'Liste her gün 09:45 sonrası yeniden hesaplanır. Bugünkü liste anahtarı: {daily_key()}')
    with st.spinner('Günlük trade adayları hazırlanıyor...'):
        picks = cached_trade_picks(daily_key())
    if not picks:
        st.warning('Günlük öneri üretilemedi. Ücretsiz veri kaynağı yanıt vermediğinde sahte öneri gösterilmez.')
    else:
        pc1, pc2, pc3 = st.columns(3)
        for i, pair in enumerate(zip([pc1, pc2, pc3], picks), start=1):
            col, item = pair
            with col:
                st.markdown(f"""
                <div class="tradepick">
                    <b>🔥 {i}. {item['symbol']}</b><br>
                    <span>{item['reason']}</span><hr>
                    📌 <b>Pusu Seviyesi (Giriş):</b> {money(item['entry'])}<br>
                    🦅 <b>Kâr Alma (Hedef):</b> {money(item['target'])}<br>
                    🛡️ <b>Zarar Kes (Stop):</b> {money(item['stop'])}<br>
                    <small>Güç skoru: {item['score']}/100</small>
                </div>
                """, unsafe_allow_html=True)

    st.write('')
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        symbol = st.text_input('Hisse kodu', value='ASELS', placeholder='Örn: ASELS, THYAO, TUPRS').upper().strip()
    with c2:
        capital = st.number_input('İşlem tutarı', min_value=1000, max_value=10_000_000, value=100_000, step=1000)
    with c3:
        st.write('')
        st.write('')
        if st.button('⭐ Favoriye ekle / çıkar', use_container_width=True):
            toggle(symbol)
            st.rerun()

    df_raw, is_demo, msg = cached_history(symbol)
    if df_raw is None or df_raw.empty or len(df_raw) < 60:
        st.error('❌ Gerçek fiyat verisi alınamadı. Bu sürüm sahte/demo fiyat üretmez. Sol menüden yenilemeyi dene veya Yahoo limiti geçince tekrar dene.')
        st.info(msg)
        st.stop()

    df = add_indicators(df_raw)
    levels = calculate_levels(df)
    decision = make_decision(df, levels)

    st.success('✅ ' + msg + ' Otomatik ekran yenileme kapalı; istersen sol menüden yenileyebilirsin.')

    decision_card(decision)

    st.write('')
    m1,m2,m3,m4,m5 = st.columns(5)
    with m1: metric_box('Anlık fiyat', money(levels['last']), 'blue')
    with m2: metric_box('Alış bölgesi', f"{money(levels['buy_low'])}<br>{money(levels['buy_high'])}", 'good')
    with m3: metric_box('Zarar kes', money(levels['stop']), 'bad')
    with m4: metric_box('Hedef / direnç', money(levels['resistance']), 'good')
    with m5: metric_box('Risk / kazanç', f"1 / {decision['rr']:.2f}", 'warn' if decision['rr']<1.7 else 'good')

    qty = int(capital // levels['last']) if levels['last'] else 0
    possible_loss = max(0, (levels['last']-levels['stop']) * qty)
    possible_gain = max(0, (levels['resistance']-levels['last']) * qty)
    st.markdown('<div class="card"><h3>💰 Yatırım olası sonuçları</h3></div>', unsafe_allow_html=True)
    a,b,c,d = st.columns(4)
    with a: metric_box('Alınabilecek lot', f'{qty:,}'.replace(',','.'), 'blue')
    with b: metric_box('Zarar kes çalışırsa olası zarar', money(possible_loss), 'bad')
    with c: metric_box('Hedef gelirse olası kâr', money(possible_gain), 'good')
    with d: metric_box('Sermayeye göre risk', f"%{decision['risk_pct']:.2f}".replace('.',','), 'warn')

    left, right = st.columns([1.35, .65])
    with left:
        st.plotly_chart(candle_chart(df, levels, f'{symbol.upper()} Karar Grafiği'), use_container_width=True)
        st.markdown('<div class="explain"><b>Grafik çizgileri ne demek?</b><br>🔵 Anlık fiyat: Hissenin şu anki seviyesi.<br>🟡 Destek: Fiyatın tutunma ihtimali olan bölge.<br>🟢 Direnç/Hedef: Kâr alınabilecek üst bölge.<br>🔴 Zarar kes: Batınca çıkmak değil; destek bozulursa zararı büyümeden sınırlama seviyesidir.</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="card"><h3>🧠 Neden böyle dedi?</h3></div>', unsafe_allow_html=True)
        for r in decision['good']:
            st.markdown(f'<div class="explain">✅ {r}</div>', unsafe_allow_html=True)
        for r in decision['bad']:
            st.markdown(f'<div class="explain">⚠️ {r}</div>', unsafe_allow_html=True)

    st.markdown('### 📊 Hareketli Ortalamalar Raporu')
    st.dataframe(moving_average_report(df), use_container_width=True, hide_index=True)

    st.markdown('### 🏦 Kurumsal / fon / aracı kurum paneli')
    p1,p2,p3 = st.columns(3)
    with p1: st.markdown('<div class="placeholder"><b>Son 3 aylık fon giriş-çıkış</b><br><br>Gerçek veri için Matriks / Foreks / MKK / Takasbank bağlantısı gerekir. Şimdilik sahte veri gösterilmez.</div>', unsafe_allow_html=True)
    with p2: st.markdown('<div class="placeholder"><b>Kurumsal - bireysel dağılım</b><br><br>Veri kaynağı bağlanınca yüzde dağılımı burada pasta grafik olarak gösterilecek.</div>', unsafe_allow_html=True)
    with p3: st.markdown('<div class="placeholder"><b>En çok alan ilk 3 aracı kurum</b><br><br>AKD verisi bağlanınca kurum adı ve yüzde payı burada listelenecek.</div>', unsafe_allow_html=True)

    st.markdown('### 📰 Önemli piyasa haberleri')
    for n in get_news(6):
        st.markdown(f'- [{n["title"]}]({n["link"]})')

    st.markdown('<br><div class="ytd">YTD: Buradaki AL / ALMA / BEKLE ifadeleri mekanik karar destek çıktısıdır; yatırım tavsiyesi değildir.</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
