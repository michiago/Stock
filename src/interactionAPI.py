import requests
import json

class InteractionAPI:

    def __init__(self, url):
        self.url = url
        try:
            self.response = requests.get(self.url) 
        except requests.exceptions.RequestException as e: 
            print('Sorry, an ERROR while calling https://finnhub.io occurred')
            raise SystemExit(e)


    def hasResponse(self):
        return (self.response.status_code == 200)
            
    def getData(self):         
        if(self.hasResponse()):
            content = self.response.content
            return json.loads(content)
