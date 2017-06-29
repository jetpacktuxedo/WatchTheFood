'''Script to scrape /u/eat_the_food's reddit posts and alert a slack channel
when he posts about artisans'''
import json
import time

import praw
from prawcore.exceptions import RequestException
import requests

with open('keys.json') as keyfile:
    KEYS = json.loads(keyfile.read())

REDDIT_CLIENT_ID = KEYS.get('reddit').get('client_id')
REDDIT_CLIENT_SECRET = KEYS.get('reddit').get('client_secret')

SLACK_WEBHOOK_URL = KEYS.get('slack').get('webhook_url')

AT_USERS = 'platabear theaverageone perniciouspony jtm_sea'

REDDIT = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent='script:watchthefood:v0.1 (by /u/jetpacktuxedo)')


@staticmethod
def slack_post(message):
    '''Post message content to slack'''
    response = requests.post(
        SLACK_WEBHOOK_URL,
        data=json.dumps({'text': message}),
        headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        print('Request to slack returned an error {}, the response is:\n{}'
              .format(response.status_code, response.text))


def check_reddit(redditor):
    '''Check most recent post by a given redditor'''
    try:
        return REDDIT.redditor(redditor).submissions.new().next()
    except RequestException:
        return None


def main():
    '''Check most recent post in a loop, notify slack of changes'''
    prev_submission = check_reddit('eat_the_food')
    while True:
        time.sleep(1)
        submission = check_reddit('eat_the_food')
        if submission is None:
            continue
        if (submission.title.startswith('[Artisan]')
                and submission != prev_submission):
            slack_post('{} {} {}'
                       .format(AT_USERS, submission.title, submission.url))
        prev_submission = submission


if __name__ == '__main__':
    main()
