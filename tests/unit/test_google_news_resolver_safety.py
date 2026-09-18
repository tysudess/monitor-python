from monitor_noticias.networking.google_news_resolver import is_safe_news_link


def test_rejects_analytics_and_assets():
    assert not is_safe_news_link("https://google-analytics.com/analytics.js")
    assert not is_safe_news_link("https://www.googletagmanager.com/gtag/js?id=G-123")
    assert not is_safe_news_link("https://example.com/static/app.js")
    assert not is_safe_news_link("https://example.com/image.webp")


def test_accepts_article_and_google_news_transport():
    assert is_safe_news_link("https://www.exemplo.com.br/noticias/materia-importante")
    assert is_safe_news_link("https://news.google.com/rss/articles/abc123?oc=5")
    assert not is_safe_news_link(
        "https://news.google.com/rss/articles/abc123?oc=5",
        allow_google_news=False,
    )
