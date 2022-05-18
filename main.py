import requests
import os
import json

LINE_TOKEN = os.environ['LINE_TOKEN']
LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'

IELTS_API_KEY = os.environ['IELTS_API_KEY']
IELTS_SCORE_URL = 'https://api.ieltsweb.idp.com/v1/externalapi/get-ielts-results'

GIVEN_NAME = os.environ['GIVEN_NAME']
FAMILY_NAME = os.environ['FAMILY_NAME']
ID_CARD_NO = os.environ['ID_CARD_NO']
DATE_OF_BIRTH = os.environ['DATE_OF_BIRTH']


class UserInfo:
    def __init__(self, given_name: str, family_name: str, date_of_birth: str, id: str) -> None:
        self.given_name = given_name
        self.family_name = family_name
        self.date_of_birth = date_of_birth
        self.id = id
        

def notify_line(text: str)-> None:
    headersAuth = {
        'Authorization': 'Bearer '+ LINE_TOKEN,
    }
    post_result = requests.post(LINE_NOTIFY_URL, {"message": text}, headers=headersAuth)
    return post_result


def get_ielts_score(user_info: UserInfo):
    ielts_payload = {
        "type": "Results", 
        "details":{
            "givenName": user_info.given_name,
            "familyName": user_info.family_name,
            "ID": user_info.id,
            "DOB": user_info.date_of_birth
        }
    }
    ielts_payload_json = json.dumps(ielts_payload)
    headers={"x-api-key" : IELTS_API_KEY}
    
    post_result = requests.post(IELTS_SCORE_URL, ielts_payload_json, headers = headers)
    return post_result


if __name__ == "__main__":
    ielts_user_info = UserInfo(given_name=GIVEN_NAME, family_name=FAMILY_NAME, id=ID_CARD_NO, date_of_birth=DATE_OF_BIRTH)
    ielts_post_result = get_ielts_score(ielts_user_info)
    
    ielts_post_result_json = ielts_post_result.json()
    print(ielts_post_result, ielts_post_result_json)
    
    if ielts_post_result_json['statusCode'] == 404:
        line_post_result = notify_line(json.dumps(ielts_post_result_json))
        print(ielts_post_result,  line_post_result, 'post_result')