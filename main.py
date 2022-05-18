import requests
import os

LINE_TOKEN = os.environ['LINE_TOKEN']
LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'

def notify_line(text: str)-> str:
    headersAuth = {
        'Authorization': 'Bearer '+ LINE_TOKEN,
    }
    post_result = requests.post(LINE_NOTIFY_URL, {"message": text}, headers=headersAuth)
    return post_result

post_result = notify_line("test with token")

if __name__ == "__main__":
    print(post_result, 'post_result')


""" 
curl -X POST -H 
'Authorization: Bearer <LINE_TOKEN>' 
-F 'message=foobar' 
https://notify-api.line.me/api/notify
"""


"""
curl 'https://api.ieltsweb.idp.com/v1/externalapi/get-ielts-results' \
  -H 'authority: api.ieltsweb.idp.com' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-type: application/json' \
  -H 'origin: https://ielts.idp.com' \
  -H 'referer: https://ielts.idp.com/results/check-your-result' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \   
"""