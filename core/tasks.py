import random

import typing as t
import requests as r

from social_network.celery import app
from core.constants import TASK_MAX_ITERATION, BOT_INTEREST_LIST
from core.utils import get_random_str
from core.exceptions import SocialNetworkApiException


@app.task()
def bot_factory_task(web_url: str, number_of_users: int, max_posts: int, max_likes: int):
    for _ in range(number_of_users):
        bot_task.delay(web_url, max_posts, max_likes)


@app.task()
def bot_task(web_url: str, max_posts: int, max_likes):
    tokens = bot_authorization_task.delay(web_url)


@app.task()
def bot_authorization_task(web_url: str) -> t.Dict:
    max_iteration = 0
    while max_iteration <= 1:

        login = get_random_str(15)
        password = get_random_str(15)

        registry_url = web_url + "/api/register/"
        try:
            registry_request = r.post(registry_url, data={'username': login,
                                                          'password': password,
                                                          'email': f'{login}@gmail.com',
                                                          'interest': random.choice(BOT_INTEREST_LIST)})
        except:
            raise SocialNetworkApiException
        if registry_request.status_code == 201:
            try:
                token_url = web_url + "/api/token/"
                token_request = r.post(token_url, data={'username': login,
                                                        'password': password})
                json_token_request = token_request.json()

                return {'access': json_token_request['access'],
                        'refresh': json_token_request['refresh']}
            except:
                raise SocialNetworkApiException

        max_iteration += 1
