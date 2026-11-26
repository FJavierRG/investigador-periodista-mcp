import pytest
from media_cloud_client import MediaCloudClient
from datetime import date 
from unittest.mock import patch
from mediacloud.error import APIResponseError
from requests import Response





def test_get_news():
    mock_page = [
    {
        "id": "12345",
        "title": "Investigación del accidente ferroviario",
        "url": "https://example.com/noticia-1",
        "language": "es",
        "media_name": "Medio A",
        "media_url": "https://example.com",
        "publish_date": date(2026, 10, 15)
    },
    {
        "id": "67890",
        "title": "El Gobierno analiza el accidente",
        "url": "https://example.org/noticia-2",
        "language": "es",
        "media_name": "Medio B",
        "media_url": "https://example.org",
        "publish_date": date(2026, 10, 16)
    }
]

    expected = [
    {
        "url": "https://example.com/noticia-1",
        "medio": "Medio A",
        "title": "Investigación del accidente ferroviario",
        "date": date(2026, 10, 15)
    },
    {
        "url": "https://example.org/noticia-2",
        "medio": "Medio B",
        "title": "El Gobierno analiza el accidente",
        "date": date(2026, 10, 16)
    }
]
    
    mc_client = MediaCloudClient()

    with patch.object(mc_client.client_search, "story_list") as mock_story_list:
        mock_story_list.return_value=(mock_page, None)
        result = mc_client.get_news("test query")
    assert result == expected

def test_get_news_empty():
    mock_page = []
    expected = []
    mc_client = MediaCloudClient()

    with patch.object(mc_client.client_search, "story_list") as mock_story_list:
        mock_story_list.return_value=(mock_page, None)
        result = mc_client.get_news("test query")
    assert result == expected

def test_500():
    mc_client = MediaCloudClient()
    response = Response()
    response.status_code=500
    mock_error = APIResponseError(response=response, params={}, data={'note': 'error'})
    with patch.object(mc_client.client_search, "story_list") as mock_story_list:
        mock_story_list.side_effect=mock_error
        with pytest.raises(APIResponseError):
            mc_client.get_news("test query")


def test_429_retry_success():
    mc_client = MediaCloudClient()

    response = Response()
    response.status_code = 429

    mock_error = APIResponseError(
        response=response,
        params={},
        data={"note": "Rate limit exceeded"}
    )

    mock_page = [
        {
            "url": "https://example.com/noticia-1",
            "media_name": "Medio A",
            "title": "Accidente ferroviario",
            "publish_date": date(2026, 10, 15)
        }
    ]

    expected = [
        {
            "url": "https://example.com/noticia-1",
            "medio": "Medio A",
            "title": "Accidente ferroviario",
            "date": date(2026, 10, 15)
        }
    ]

    with patch.object(mc_client.client_search, "story_list") as mock_story_list:
        with patch("media_cloud_client.time.sleep") as mock_sleep:

            mock_story_list.side_effect = [
                mock_error,
                (mock_page, None)
            ]

            result = mc_client.get_news("test query")

            assert result == expected
            assert mock_story_list.call_count == 2
            assert mock_sleep.call_count == 1

def test_429_max_retries():
    mc_client = MediaCloudClient()

    response = Response()
    response.status_code = 429

    mock_error = APIResponseError(
        response=response,
        params={},
        data={"note": "Rate limit exceeded"}
    )

    with patch.object(mc_client.client_search, "story_list") as mock_story_list:
        with patch("media_cloud_client.time.sleep") as mock_sleep:

            mock_story_list.side_effect = mock_error

            with pytest.raises(APIResponseError):
                mc_client.get_news("test query")

            assert mock_story_list.call_count == 4
            assert mock_sleep.call_count == 3