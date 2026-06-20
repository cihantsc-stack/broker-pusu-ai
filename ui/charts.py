import plotly.graph_objects as go


def _tl(val):
    return f"{val:,.2f} TL".replace(',', 'X').replace('.', ',').replace('X','.')


def candle_chart(df, levels, title):
    d = df.tail(90).copy()
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=d.index, open=d['Open'], high=d['High'], low=d['Low'], close=d['Close'], name='Mum'
    ))
    lines = [
        ('Anlık fiyat', levels['last'], '#4da3ff', 'solid'),
        ('Destek', levels['support'], '#f7b731', 'dash'),
        ('Hedef / direnç', levels['resistance'], '#18c37e', 'dash'),
        ('Stop-loss', levels['stop'], '#ff5a5f', 'dot'),
    ]
    for name, val, color, dash in lines:
        fig.add_hline(y=val, line_width=2.4, line_dash=dash, line_color=color)
        fig.add_annotation(
            xref='paper', x=1.01, y=val, yref='y',
            text=f'<b>{name}</b><br>{_tl(val)}',
            showarrow=False, xanchor='left', align='left',
            bgcolor='rgba(8,13,21,0.96)', bordercolor=color, borderwidth=1,
            font=dict(color=color, size=12),
        )
    fig.update_layout(
        template='plotly_dark', title=title, height=560,
        margin=dict(l=10, r=210, t=50, b=10),
        xaxis_rangeslider_visible=False,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(8,13,21,1)',
        showlegend=False,
    )
    return fig
