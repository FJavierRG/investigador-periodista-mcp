from media_cloud_client import MediaCloudClient


busqueda = input("Información a contrastar: ")
mediacloud_client = MediaCloudClient()
urls = mediacloud_client.get_urls(busqueda)
print(urls)