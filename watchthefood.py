import json
import praw
import requests
import time

with open('keys.json') as keyfile:
    keys = json.loads(keyfile.read())

REDDIT_CLIENT_ID = keys.get('reddit').get('client_id')
REDDIT_CLIENT_SECRET = keys.get('reddit').get('client_secret')

SLACK_WEBHOOK_URL = keys.get('slack').get('webhook_url')

AT_USERS = 'platabear theaverageone perniciouspony jtm_sea'

def slack_post(message):
    response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps({'text': message}), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise ValueError('Request to slack returned an error {}, the response is:\n{}'.format(response.status_code, response.text))


def main():
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent='script:watchthefood:v0.1 (by /u/jetpacktuxedo)')
    prev_submission = reddit.redditor('eat_the_food').submissions.new().next()
    while True:
        submission = reddit.redditor('eat_the_food').submissions.new().next()
        if submission.title.startswith('[Artisan]') and submission != prev_submission:
            slack_post('{} {} {}'.format(AT_USERS, submission.title, submission.url))
        time.sleep(1)
        prev_submission = submission

if __name__ == '__main__':
    main()
