"""
Media Cloud utiliza búsquedas léxicas con operadores booleanos, no búsquedas semánticas en lenguaje natural
La sintaxis que admite Media Cloud es la siguiente:

AND	Exige ambos términos.
OR	Exige al menos uno.
NOT	Excluye un término.
"etexto"	Busca una expresión exacta.
text*	Busca distintas terminaciones.
(A OR B)	Agrupa condiciones.
"texto"~5	Busca términos próximos entre sí.
article_title:Texto	Busca únicamente en titulares.
language:es	Restringe el idioma al español.

"""

import mediacloud.api
from dotenv import load_dotenv
import os
import datetime as dt
import time
import random
import logging
from mediacloud.error import APIResponseError

load_dotenv() 

MEDIACLOUD_API_KEY = os.getenv("MEDIACLOUD_API_KEY")
logger = logging.getLogger(__name__)

class MediaCloudClient:
    def __init__(self):
        self.api_key = MEDIACLOUD_API_KEY
        self.client_search = mediacloud.api.SearchApi(self.api_key)
        self.client_directory = mediacloud.api.DirectoryApi(self.api_key)
        self.start_date = dt.date(2026, 10, 1)
        self.end_date = dt.date(2026, 11, 1)
        self.sources = [34412356, 38002034]
        self.page_size = 25
        self.max_stories = 50

    def get_news(self, query: str)-> list[dict]:
        query= "Accidente AND Trenes AND Urda AND gobierno"
        pages = []
        more_pages = True
        pagination_token = None
        inicio = time.perf_counter()
        max_retries = 4
        logger.info(f"Fixed date: {self.start_date}/{self.end_date}")
        # Hace falta un elemento intermedio que convierta una petición en lenguaje natural a una query para Media Cloud
        logger.warning(f"Fixed query: {query}")

        for i in range(max_retries):
            try:
                while more_pages and len(pages)<self.max_stories:
                    page, pagination_token = self.client_search.story_list(query, self.start_date, self.end_date,
                                                                        collection_ids=self.sources,
                                                                        pagination_token=pagination_token,
                                                                        page_size=self.page_size
                                                                        )
                    pages += page
                    logger.info("pagina extraída con éxito")
                    if pagination_token is not None:
                        more_pages = True
                    else:
                        more_pages = False
        
            except APIResponseError as e:
                if e.response.status_code == 429:
                    if i+1 == max_retries:
                        logger.error(f"Maximo numero de intentos alcanzados")
                        return []
                    logger.error(f"RateLimit alcanzando, reintentando {i+1}/{max_retries}")
                    delay = 2 ** i + random.uniform(0,1)
                    time.sleep(delay)
                    continue
                logger.error(f"Error al obtener contenido de MediaCloud: {e}")
                return []

        logger.info("Todas las paginas han sido procesadas")
        if len(pages) == 0:
            logger.warning(f"No se encontraron resultados para la búsqueda: {query}")
            return []
        
        fin = time.perf_counter()
        logger.info(f"Tiempo de ejecución: {fin - inicio:.2f} segundos")
        return [{
            "url": pagina['url'],
            "medio": pagina['media_name'],
            "title": pagina['title'],
            "date": pagina['publish_date']
        }for pagina in pages]


