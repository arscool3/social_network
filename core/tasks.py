import random

from social_network.celery import app
from core.constants import BOT_INTEREST_LIST
from core.bot_actions import bot_authorization, bot_add_likes, bot_create_posts, get_favourite_bot_post_ids


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

