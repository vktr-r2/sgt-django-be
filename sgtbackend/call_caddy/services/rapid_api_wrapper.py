import os
import requests
from datetime import datetime
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

logger = logging.getLogger("call_caddy")

class RapidApiWrapperService:

    def __init__(self):
        self.rapid_api_key = os.environ.get("RAPID_API_KEY")
        self.base_url = "https://live-golf-data.p.rapidapi.com/"
        self.headers = {
            "X-RapidAPI-Key": self.rapid_api_key,
            "X-RapidAPI-Host": "live-golf-data.p.rapidapi.com",
        }
    
    # Base authenticated API call function
    def make_request(self, url_path, params=None):
        full_url = f"{self.base_url}{url_path}"

        try:
            response = requests.get(full_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except ConnectionError as conn_err:
            logger.error(f"Connection error occurred: {conn_err}")
        except Timeout:
            logger.error("The request timed out")
        except RequestException as err:
            logger.error(f"An error occurred: {err}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        return None