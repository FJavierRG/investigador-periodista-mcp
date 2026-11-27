from media_cloud_client import MediaCloudClient
from utils.web_search import web_search
import logging
from model_calls.input_validator import validate_input
from model_calls.mc_query_generator import generate_mc_query

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    print("iniciando")
    busqueda = input("¿Qué quiere investigar?: ")
    validation_input = validate_input(busqueda)

    if validation_input['parsed'].input_validation == 'Rejected':
        logger.info("Mensaje de usuario Rejected")
        return

    logger.info("Mensaje de usuario Accepted")
    query = generate_mc_query(busqueda)
    parsed_querys = query['parsed'].querys
    logger.info(f"Querys generadas: {parsed_querys}")
    mediacloud_client = MediaCloudClient()
    logger.info("MC cliente creado")

    news = mediacloud_client.get_news(parsed_querys)
    print("busqueda realizada")
    if len(news) == 0:
        return print("No se han encontrado noticias para la búsqueda especificada.")

    news_complete = web_search(news)
    print(f"Se han encontrado {len(news_complete)} noticias con información comprobable")

if __name__ == "__main__":
    main()