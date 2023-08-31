from urllib.parse import quote
from time import sleep
import requests
from cloudscraper import create_scraper
from urllib3 import disable_warnings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

# Variables for the shorter site and shorter API
shortener_site = ''
shortener_api = ''


def short_url(longurl, attempt=0):
    try:
        cget = create_scraper().request
        disable_warnings()

        # Check if shortener_site and shortener_api are empty strings
        if shortener_site == '' or shortener_api == '':
            # Use the second API request site
            res = cget('GET', f'https://api.shrtco.de/v2/shorten?url={quote(longurl)}').json()
            shrtco_link = res.get('result', {}).get('full_short_link', None)
        else:
            # Request short URL from the shortener site service
            # Request short URL from the shortener site service
            res = cget('GET', f'{shortener_site}/api?api={shortener_api}&url={longurl}').json()
            shorted = res['shortenedUrl']
            # Use shrtco.de API to get a shorter URL
            shrtco_res = cget('GET', f'https://api.shrtco.de/v2/shorten?url={quote(shorted)}').json()
            shrtco_link = shrtco_res.get('result', {}).get('full_short_link', None)

        if not shrtco_link:
            shrtco_link = longurl

        return shrtco_link

    except requests.exceptions.RequestException as req_ex:
        LOGGER.error(f"Request error: {req_ex}")
        raise req_ex
    
    except (KeyError, ValueError) as json_ex:
        LOGGER.error(f"JSON parsing error: {json_ex}")
        raise json_ex

    except Exception as ex:
        LOGGER.error(f"Unknown error occurred: {ex}")
        raise ex

    if attempt < 3:
        try:
            # Retry after a short delay
            sleep(1)
            return short_url(longurl, attempt + 1)
        
        except Exception as ex:
            LOGGER.error(f"Unknown error occurred during retry: {ex}")
            raise ex

    else:
        LOGGER.error("Maximum retries reached.")
        return longurl

# URL to be shortened
longurl = ""
shortened_url = short_url(longurl)
LOGGER.info(f"Shortened URL: {shortened_url}")
