import requests
import json
class CodeforcesData:
    def get_rating_by_handle(self,handle: str) -> int:
        url = "https://codeforces.com/api/user.info"
        data = { "handles": handle }
        access_token = requests.post(url, data = data)
        if( access_token.json()['status'] != 'OK' ):
            return 'No User'
        return access_token.json()['result'][0]