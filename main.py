from media_cloud_client import MediaCloudClient
from utils.web_search import web_search
import logging
from input_validator import validate_input

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    print("iniciando")
    busqueda = "El accidente de Urda es culpa del gobierno"
    validation_input = validate_input(busqueda)

    if validation_input['parsed'].input_validation == 'Rejected':
        logger.info("Mensaje de usuario Rejected")
        return

    logger.info("Mensaje de usuario Accepted")
    mediacloud_client = MediaCloudClient()
    logger.info("MC cliente creado")

    news = mediacloud_client.get_news(busqueda)
    print("busqueda realizada")
    if len(news) == 0:
        return print("No se han encontrado noticias para la búsqueda especificada.")

    news_complete = web_search(news)
    print(f"Se han encontrado {len(news_complete)} noticias con información comprobable")

if __name__ == "__main__":
    main()