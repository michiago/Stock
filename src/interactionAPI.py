import requests
import json

class InteractionAPI:

    def __init__(self, url):
        self.url = url

    def getDataFromApi(self):
        try:
            content = requests.get(self.url).content
            return json.loads(content)
        except requests.exceptions.RequestException as e: 
            print('Sorry, an ERROR while calling https://finnhub.io occurred')
            raise SystemExit(e)
            