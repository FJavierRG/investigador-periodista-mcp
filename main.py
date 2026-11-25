from media_cloud_client import MediaCloudClient
from utils.web_search import web_search
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    print("iniciando")
    busqueda = "Adamuz AND accidente AND trenes"
    mediacloud_client = MediaCloudClient()
    print("cliente de mediacloud creado")

    news = mediacloud_client.get_news(busqueda)
    print("busqueda realizada")
    if len(news) == 0:
        return print("No se han encontrado noticias para la búsqueda especificada.")

    news_complete = web_search(news)
    print(f"Se han encontrado {len(news_complete)} noticias con información comprobable")

if __name__ == "__main__":
    main()