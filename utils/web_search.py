import trafilatura
import logging

logger = logging.getLogger(__name__)

def web_search(news: list[dict]) -> list[dict]:
    for noticia in news:
        logger.info(f"Realizando búsqueda web para la URL: {noticia['url']}")
        html = trafilatura.fetch_url(noticia['url'])
        text = trafilatura.extract(html)
        if text is None:
            logger.warning(f"No se pudo extraer contenido de la URL: {noticia['url']}")
        noticia['contenido'] = text
    none_count = sum(1 for noticia in news if noticia['contenido'] is None)
    clean_news = [noticia for noticia in news if noticia['contenido'] is not None]
    logger.info(f"Se encontraron {none_count} noticias sin contenido extraído de {len(news)}")

    return clean_news