

from social_network.celery import app


@app.task()
def bot_factory_task(number_of_users: int, max_posts: int, max_likes: int):
    pass

def bot_factory(max_posts: int, max_likes):
    pass