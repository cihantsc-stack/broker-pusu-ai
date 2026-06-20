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
        ('ANLIK', levels['last'], '#4da3ff', 'solid'),
        ('DESTEK', levels['support'], '#f7b731', 'dash'),
        ('HEDEF', levels['resistance'], '#18c37e', 'dash'),
        ('ZARAR KES', levels['stop'], '#ff5a5f', 'dot'),
    ]
    for name, val, color, dash in lines:
        fig.add_hline(y=val, line_width=2.8, line_dash=dash, line_color=color)
        fig.add_annotation(
            xref='paper', x=1.015, y=val, yref='y',
            text=f'<b>{name}</b><br><span style="font-size:15px">{_tl(val)}</span>',
            showarrow=False, xanchor='left', align='left',
            bgcolor='rgba(5,10,18,0.98)', bordercolor=color, borderwidth=2,
            font=dict(color=color, size=14),
        )

    fig.update_layout(
        template='plotly_dark', title=title, height=585,
        margin=dict(l=10, r=250, t=50, b=10),
        xaxis_rangeslider_visible=False,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(8,13,21,1)',
        showlegend=False,
        yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,.18)'),
        xaxis=dict(showgrid=False),
    )
    return fig
