# from charset_normalizer import CharsetMatches
import requests
import time

# from urllib import parse
# from shutil import which as By
from .td_url import *


class TDAccSession(requests.Session):
    def __init__(self, refresh_token=None, client_id=None):
        super().__init__()
        self._refreshToken = {"token": refresh_token}
        self._accessToken = {
            "token": "",
            "created_at": time.time(),
            "expires_in": -1,
        }  # Set to -1 so that it gets refreshed immediately and its age tracked.
        self._client_id = client_id
        self._headers = {}

    def _set_header_auth(self):
        self._headers.update({"Authorization": "Bearer " + self._accessToken["token"]})

    def request(self, *args, **kwargs):
        self._refresh_token_if_invalid()
        return super().request(headers=self._headers, *args, **kwargs)

    def _is_token_invalid(self):
        if (
            not self._accessToken["token"]
            or self._access_token_age_secs() >= self._accessToken["expires_in"] - 60
        ):
            return True
        else:
            return False

    def _refresh_token_if_invalid(self):
        # Expire the token one minute before its expiration time to be safe
        if self._is_token_invalid():
            token = self.get_access_token(self._refreshToken["token"], self._client_id)
            self._set_access_token(token)

    def _set_access_token(self, token):
        self._accessToken["token"] = token["access_token"]
        self._accessToken["created_at"] = time.time()
        self._accessToken["expires_in"] = token["expires_in"]
        self._set_header_auth()

    def _access_token_age_secs(self):
        return time.time() - self._accessToken["created_at"]

    def get_access_token(self, refresh_token, client_id):
        resp = requests.post(
            "https://api.tdameritrade.com/v1/oauth2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
            },
        )
        if resp.status_code != 200:
            raise Exception("Could not authenticate!")
        return resp.json()


# def get_accountID(access_token):
#     headers = {"Authorization": "Bearer {}".format(access_token)}
#     endpoint = r"https://api.tdameritrade.com/v1/accounts"
#     content = requests.get(url=endpoint, headers=headers)
#     data = content.json()
#     print(data)
#     account_id = data[0]["securitiesAccount"]["accountId"]
#     print(account_id)
#     return account_id


# def authenticate(client_id, redirect_uri):
#     from selenium import webdriver
#     from selenium.webdriver.chrome.service import Service
#     from webdriver_manager.chrome import ChromeDriverManager
#
#     client_id = client_id + "@AMER.OAUTHAP"
#     url = (
#         "https://auth.tdameritrade.com/auth?response_type=code&redirect_uri="
#         + parse.quote(redirect_uri)
#         + "&client_id="
#         + parse.quote(client_id)
#     )
#
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()), options=options
#     )
#
#     driver.get(url)
#
#     input("after giving access, hit enter to continue")
#     code = parse.unquote(driver.current_url.split("code=")[1])
#
#     driver.close()
#
#     resp = requests.post(
#         "https://api.tdameritrade.com/v1/oauth2/token",
#         headers={"Content-Type": "application/x-www-form-urlencoded"},
#         data={
#             "grant_type": "authorization_code",
#             "refresh_token": "",
#             "access_type": "offline",
#             "code": code,
#             "client_id": client_id,
#             "redirect_uri": redirect_uri,
#         },
#     )
#     if resp.status_code != 200:
#         raise Exception("Could not authenticate!")
#     return resp.json()


# def access_token(refresh_token, client_id):
#     resp = requests.post(
#         "https://api.tdameritrade.com/v1/oauth2/token",
#         headers={"Content-Type": "application/x-www-form-urlencoded"},
#         data={
#             "grant_type": "refresh_token",
#             "refresh_token": refresh_token,
#             "client_id": client_id,
#         },
#     )
#     if resp.status_code != 200:
#         raise Exception("Could not authenticate!")
#     print(resp.json())
#     return resp.json()


# def get_quote():
#     endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/quotes".format("GOOG")
#     print(endpoint)
#     payload = {
#         "apikey": "QGA9OVULNR1HOEOH2WULWUWGCOFJKROS",
#     }
#     content = requests.get(url=endpoint, params=payload)
#     data = content.json()
#     print(data)


# if __name__ == "__main__":
#     # print(authentication(client_id='QGA9OVULNR1HOEOH2WULWUWGCOFJKROS', redirect_uri='http://localhost'))
#     # access_token("BCKxdrSBr7JJTnGk3vNeNme/09kDUq5CN6BcM9O3L3rak3e7A25cqpHnYGjtK4Fw1cY44FEsFi36DXuPS0zIQz5Tsi1WemKEkF6btBf/Ik1G75eau4EqrC8iQbz1e0wVd57aWJMayBcznDLyr7sEZ94ONdlMT4DluWrELUZqVQPig34Mzmm/NMBo0Fvirl4wYKUmqpEOr2RbM6VtNIYVeeHWYTLn0fJozJU6KgcXmTYZxhUTX8itDv6fbnvVhCkKnNw/d4tvg42qAtT8DTsTfSlJeUeUW+HcMXI9WBBITOrcuyrqsSoRWH/8+wXQjhnbOt5/sc2TqBeMg3ae856hwzHZO93Xq/ky5jL6Yk6MW2A5tJm/qR27VtxwqiY6J14oXJW0rNyOtCOkH754E7pCMtZ6n6aqg4d7GhPyTh/O2wJKvatOjmROxjxpNsU100MQuG4LYrgoVi/JHHvliX0zLdRKdIHvL1wbnHdMPIzCvdyxLrtZWVpUSdYD7LPIImxLMazHycwvdeKIUXlYKFmigvqNiqjkTe5vWNrQlkMUjrE8OnLBIpUZCIuvyBaEviJbfZ/WJI7hrk3MT7B1+NoMibl+P3wNuunuoHDjc2m5Ju7FiZVPliBWmCqr+liI1AWOkoOXbrU8NMUlMEedYYmGzNRnC39EyKEyRW5JgPGeRkSu6+HB1eGAzcoJ3uXo88lYupyAA+BaI2EvvZy8zc3NQResnojq4jull55TIxXpOv04vji84PuLGURtKn3qiwGtqB8P3kDqKJC93S/Eh9zvMQMEETIipgG0itPrBSNRFqnQPZzLIroTO7CfIUehTYlmhETIbZXzT+E1wyYKcanrg/na1jmyg+hFcOPqE1TkyRu+vZ+8kAe46KhlUoW1A4SFL8ytn85AR3E=212FD3x19z9sWBHDJACbC00B75E",client_id = "QGA9OVULNR1HOEOH2WULWUWGCOFJKROS")
#     get_accountID(
#         "P3hNcGY2RfqgjR6NiqdUS9LBGBUHl6vaFiwp2WTTJrW/Iamyj0ZEnB1tA0alP1ZtqG0gCYckNSDtvEAF3jNuDBaqmM1+M0aBWMqbznI8/MgsBJCDzPep20L2gcHdSd5XygZObAgRq0BMgwM3UzmC9oAJhZ4ElRS/iKczVagmEG4qYXzbDs0somx4XfrjHPCLwph2/mS7hva40rZ+e5P0rU2Q4GYB45XD/w4nP6b5vmZgA5IxTYKzVPQruDiWwF6v1eQPDOJ8TuFu8k8XgOlQ28GPQjDPQmalKhW7O8vYR3OXq9/YUBL0XUogG/GK0BAMHAOOkhPbIvOCaGd0CX+TXHFgxzdROmI7YRYNFCxuPWYHU0QMfSgDgKflM90V1N3mgSTKZZkALLqNYu0fex+GjW8g2V3T1djmAUh34vUsU7GLEKjfY+cwnMVYU82XXbzAVAgdF6xTiekN9GZDAxOGYjc05cJVPWcTmqPLfoHpVqis4jKjuSjuxIGuyOF5ODqNRPTQYc4x0D6Aht8UjBSbDQidBL+rKOPEUi+oSis16vLpwqZpM100MQuG4LYrgoVi/JHHvlD+PHmk20Dn3CHPHIRk/LYJi5gpQWr1L9Sb6a//GZZOlOeTHbMltAcLbYO4jWkSHC3y8goM6VMxjwYHB1WgXY1JBzmB+U59hfrhihhwZKEf3q08YDqnCwwpgKWL1fl0Q/m7TP+nj4qoJRU048f2QKZzQkzLfW9dui57Zu0qOJQE/WJaw4VYcGyo0oqJbkVX97obuhUzaBX6uptgQnwWudXTjRDlhqB6I0V3KzpRTILQq6oHPqhETu01UwDOHNX7ZlLzf+0vlqg9JEXSY25vjle4+E7luyTbihJwfjt1CLbIe0SSvw0g6OL4+yl/sEpv+QQDEtfUUgdG2lsS8n4TVyNgL/iiT3WsL0xlCAejgi4nBq7PJ1oQccSm81+XbBFtLaBfT7htNdNEJWwrcYzQHiu1VnZCXrnZalsfLXXL2jrzNDR1GK/AX+zXhjl+i1Gdjp4rhlmZgMiGSXE1NytTC9buVZI5U7+8feJIpongs8C7LNoqAlaKGZ8ho9ZycXJGyWPEZctpUmeAL4CM6YXKgpdlyPKrWA+3UwV5uIm46R1ZjuLuGg==212FD3x19z9sWBHDJACbC00B75E"
#     )
