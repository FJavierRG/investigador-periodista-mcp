from media_cloud_client import MediaCloudClient
from utils.web_search import web_search
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    busqueda = "PSOE cangrejos mesopotamicos"
    mediacloud_client = MediaCloudClient()

    news = mediacloud_client.get_urls(busqueda)
    if len(news) == 0:
        return print("No se han encontrado noticias para la búsqueda especificada.")

    news_complete = web_search(news)
    print(news_complete)

if __name__ == "__main__":
    main()