import random

import typing as t
import requests as r

from social_network.celery import app
from core.constants import TASK_MAX_ITERATION, BOT_INTEREST_LIST
from core.utils import get_random_str
from core.exceptions import SocialNetworkApiException
from core.models import Post


@app.task()
def bot_factory_task(web_url: str, number_of_users: int, max_posts: int, max_likes: int):
    for _ in range(number_of_users):
        bot_task.delay(web_url, max_posts, max_likes)


@app.task()
def bot_task(web_url: str, max_posts: int, max_likes):
    bot_interest = random.choice(BOT_INTEREST_LIST)
    tokens = bot_authorization(web_url, bot_interest)

    bot_create_posts(web_url, tokens, bot_interest, max_posts)
    favourite_post_ids = get_favourite_bot_post_ids(bot_interest)
    bot_add_likes(web_url, tokens, favourite_post_ids, max_likes)


def get_favourite_bot_post_ids(bot_interest: str) -> t.List:
    favourite_post_ids = []
    favourite_ids_queryset = Post.objects.filter(topic=bot_interest).values('id')
    for favourite_id in favourite_ids_queryset:
        favourite_post_ids.append(favourite_id['id'])
    return favourite_post_ids


def bot_add_likes(web_url: str, tokens: t.Dict, favourite_post_ids: t.List, max_likes: int):
    for i in range(random.randint(1, max_likes)):

        post_number = random.choice(favourite_post_ids)
        like_url = web_url + f"/api/posts/{post_number}/like/"
        headers = {"Authorization": f"Bearer {tokens['access']}"}
        try:
            r.post(like_url, headers=headers)
        except:
            raise SocialNetworkApiException


def bot_create_posts(web_url: str, tokens: t.Dict, bot_interest: str, max_posts: int):
    for _ in range(random.randint(1, max_posts)):
        posts_url = web_url + "/api/posts/"
        text = get_random_str(50)
        headers = {"Authorization": f"Bearer {tokens['access']}"}
        print(headers)
        try:
            r.post(posts_url, headers=headers, data={'topic': bot_interest, 'text': text})
        except:
            raise SocialNetworkApiException


def bot_authorization(web_url: str, bot_interest: str) -> t.Dict:
    max_iteration = 0
    while max_iteration <= TASK_MAX_ITERATION:

        login = get_random_str(15)
        password = get_random_str(15)

        registry_url = web_url + "/api/register/"
        try:
            registry_request = r.post(registry_url, data={'username': login,
                                                          'password': password,
                                                          'email': f'{login}@gmail.com',
                                                          'interest': bot_interest})
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

    raise SocialNetworkApiException
