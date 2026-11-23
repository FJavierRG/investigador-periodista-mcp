import mediacloud.api
from dotenv import load_dotenv
import os
import datetime as dt
import pandas as pd
import time

load_dotenv() 

MEDIACLOUD_API_KEY = os.getenv("MEDIACLOUD_API_KEY")
mediacloud_client = mediacloud.api.SearchApi(MEDIACLOUD_API_KEY)
directory_api = mediacloud.api.DirectoryApi(MEDIACLOUD_API_KEY)

class MediaCloudClient:
    def __init__(self):
        self.api_key = MEDIACLOUD_API_KEY
        self.client_search = mediacloud.api.SearchApi(self.api_key)
        self.client_directory = mediacloud.api.DirectoryApi(self.api_key)
        self.start_date = dt.date(2023, 11, 1)
        self.end_date = dt.date(2023, 12, 1)
        self.sources = [34412356, 38002034]
        self.page_size = 150

    def get_urls(self, query: str)-> list:
        pages = []
        more_pages = True
        pagination_token = None

        while more_pages:
            inicio = time.perf_counter()
            page, pagination_token = self.client_search.story_list(query, self.start_date, self.end_date,
                                                                   collection_ids=self.sources,
                                                                   pagination_token=pagination_token,
                                                                   page_size=self.page_size)
            pages += page
            if pagination_token is not None:
                more_pages = True
            else:
                more_pages = False

        fin = time.perf_counter()
        print(f"Tiempo de ejecución: {fin - inicio:.2f} segundos")
        df = pd.DataFrame(pages)
        urls = df['url'].tolist()
        return urls


