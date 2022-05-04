import requests
import requests as r

from rest_framework.request import Request

from social_network.celery import app


@app.task()
def bot_factory_task(web_url: str, number_of_users: int, max_posts: int, max_likes: int):
    for _ in range(number_of_users):
        bot_factory.delay(web_url, max_posts, max_likes)


@app.task()
def bot_factory(web_url: str, max_posts: int, max_likes):
    post_url = web_url + "/api/register/"
    req = requests.post(post_url, data={'username': 'abcde',
                                        'password': '12345ArslanYersain',
                                        'email': 'abcde@gmail.com',
                                        'interest':'tech'})
    print(req.json())