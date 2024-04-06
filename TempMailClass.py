import json
import random
import requests as req
from tempmail import EMail
from bs4 import BeautifulSoup

class Temp_Mail:

    def __init__(self) -> None:
        self.get_user_agent()
        self.email = EMail()
        print(self.email.address)
        api_key =  self.signup()
        return api_key


    url = "https://www.criminalip.io/api"
    password = "@Test12345678!"
    headers = {
        "Cookie": "_locale=en;",
        "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "Dnt": "1",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
    }

    def get_user_agent(self):
        path = "user-agent.txt"
        with open(path, "r+", encoding="utf-8") as file:
            user_aganets = file.readlines()
            random_number = random.randrange(0, user_aganets.__len__())
            user_aganet = user_aganets[random_number].removesuffix("\n")
            self.headers["User-Agent"] = user_aganet

    

    def signup(self):
        url_signup = self.url + "/auth/user/signup"
        data = {
            "account_type": "not_social",
            "email": f"{self.email}",
            "uid": "",
            "name": f"{self.email}",
            "pw": self.password,
            "pp_agree_code": 1,
            "tos_agree_code": 1,
            "ad_agree_code": 1,
        }
        response = req.api.post(url_signup, headers=self.headers, json=data)
        if response.status_code == 200:
            return self.send_verfiy(response)
        raise

    def send_verfiy(self, last_response):
        url_authentication = self.url + "/email/authentication"
        self.headers["Cookie"] = (
            self.headers["Cookie"]
            + last_response.headers["set-cookie"].split(";")[0]
            + ";"
        )
        data = {}
        response = req.api.post(url_authentication, headers=self.headers, json=data)

        self.headers["Cookie"] = (
            self.headers["Cookie"] + response.headers["set-cookie"].split(";")[0] + ";"
        )
        
        if response.status_code == 200:
           return self.get_token_verify()
        raise

    def get_token_verify(self):
        msg = self.email.wait_for_message(timeout=70)
        html_doc = msg.html_body
        soup = BeautifulSoup(html_doc, "html.parser")
        a_tags = soup.find_all("a")
        url_verify = a_tags[0].get("href")
        response = req.get(url_verify, headers=self.headers)
        if response.status_code == 200:
            token = url_verify.split("token=")[1]
            return self.verfiy(token)
        raise

    def verfiy(self, token):
        url_authToken = self.url + "/auth/user/authToken"
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = {
            "auth_token": f"{token}",
        }
        response = req.post(url_authToken, headers=self.headers, data=data)
        self.headers["Content-Type"] = "application/json"
        if response.status_code == 200:
            return self.login()
        raise

    def login(self):
            url_login = self.url + "/auth/user/login"
            data = {
                "account_type": "not_social",
                "email": f"{self.email}",
                "pw": self.password,
            }
            self.headers["Content-Type"] = "application/x-www-form-urlencoded"
            response = req.post(url_login, headers=self.headers, data=data)
            self.headers["Content-Type"] = "application/json"
            if response.status_code == 200:
               return self.get_apikey()
            raise


    def get_apikey(self):
        url_get_apikey = "https://www.criminalip.io/_next/data/GUaF3eRxYyfwS36Zg9Dej/en/mypage/information.json"
        response = req.get(url_get_apikey, headers=self.headers)
        if response.status_code == 200:
            dict_result = json.loads(response.text)
            api_key = dict_result["pageProps"]["dehydratedState"]["queries"][0][
                "state"
            ]["data"]["data"]["api_key"]

            return api_key
        raise

def main():
    api_key = Temp_Mail()
    return api_key