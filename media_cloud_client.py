import mediacloud.api
from dotenv import load_dotenv
import os
import datetime as dt
import time
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
        self.start_date = dt.date(2023, 11, 1)
        self.end_date = dt.date(2024, 11, 1)
        self.sources = [34412356, 38002034]
        self.page_size = 150

    def get_urls(self, query: str)-> list:
        pages = []
        more_pages = True
        pagination_token = None
        inicio = time.perf_counter()

        try:
            while more_pages:
                page, pagination_token = self.client_search.story_list(query, self.start_date, self.end_date,
                                                                    collection_ids=self.sources,
                                                                    pagination_token=pagination_token,
                                                                    page_size=self.page_size)
                pages += page
                if pagination_token is not None:
                    more_pages = True
                else:
                    more_pages = False

        except APIResponseError as e:
            logger.error(f"Error al obtener contenido de MediaCloud: {e}")
            raise e

        
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


