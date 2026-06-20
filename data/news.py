import feedparser


def get_news(limit=6):
    feeds = [
        'https://news.google.com/rss/search?q=Borsa%20Istanbul%20BIST%20hisse%20piyasa&hl=tr&gl=TR&ceid=TR:tr',
        'https://news.google.com/rss/search?q=ekonomi%20borsa%20haberleri&hl=tr&gl=TR&ceid=TR:tr'
    ]
    items=[]
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for e in f.entries[:limit]:
                items.append({'title': e.get('title','Haber'), 'link': e.get('link','#'), 'source': e.get('source',{}).get('title','') if isinstance(e.get('source',{}), dict) else ''})
        except Exception:
            pass
    seen=[]; uniq=[]
    for i in items:
        if i['title'] not in seen:
            seen.append(i['title']); uniq.append(i)
    return uniq[:limit]
