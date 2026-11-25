"""
Se utilizará BIGQUERY para búsqueda de noticias similares a partir de las detectadas con MediaCloud. Queda en pausa.
"""

import requests
import logging
from datetime import datetime
import random
import time

logger = logging.getLogger(__name__)

class GDELTClient:
    def __init__(self):
        self.base_url: str = "https://api.gdeltproject.org/api/v2/doc/doc"
        self.query: str = ""
        self.sourcelang: str = "spanish"
        self.mode: str = "artlist"
        self.startdatetime: str = ""
        self.enddatetime:str = ""
        self.maxrecords: int = 200

        start_date = datetime(2023, 11, 1)
        end_date = datetime(2024, 11, 1)
        self.startdatetime = start_date.strftime("%Y%m%d%H%M%S")
        self.enddatetime = end_date.strftime("%Y%m%d%H%M%S")

    def get_news(self, query: str)->list[dict]:

        if len(query) ==0:
            logger.error("Error. Mensaje enviado a GDELT vacío.")
            return []
        
        max_retries = 4
        safe_fixed_time = 6 # Obligatorio por la DOC de la API. 1 petición cada 5 segundos
        params = {"query": f"{query} sourcelang:{self.sourcelang}",
                  # "sourcelang": self.sourcelang, Parece que va dentro de query como sourcelang:spanish"
                  "mode": self.mode,
                  "startdatetime": self.startdatetime,
                  "enddatetime": self.enddatetime,
                  "maxrecords": self.maxrecords,
                  "format": ""
                  }
        for i in range(max_retries):
            try:
                time.sleep(safe_fixed_time)
                response = requests.get(url=self.base_url, params=params, timeout=30)
                response.raise_for_status()
                break

            except requests.exceptions.HTTPError as e:
                if e.response.status_code != 429:
                    logger.error(f"Error HTTP: {e}")
                    return []
                
                logger.warning(f"No se ha podido conectar con GDELT [{e.response.status_code}], reintentando {i+1}/{max_retries}")
                if i+1 == max_retries:
                    logger.error("Error al conectar con GDELT. Numero maximo de intentos alcanzados")
                    return []
                delay = 2 ** i + 1 + random.uniform(0,1)
                time.sleep(delay)

        logger.warning(f"RESPUESTA DE GDELT: {response.text}")
        try:
            response = response.json()
        except requests.exceptions.JSONDecodeError as e:
            logger.error(f"Error al procesar la respuesta de GDELT al convertir a JSON: {e}")
            return []
        
        print("RESULTADO DE LA BÚSQUEDA: "+ response)
        return response


gdelt_client = GDELTClient()
noticias = gdelt_client.get_news(query="Corrupción PSOE (OR corrupción del partido socialista OR corrupción pedro sánchez)")
