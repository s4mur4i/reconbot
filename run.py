from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import os

import schedule
import time
import sqlite3

from reconbot.tasks import esi_notification_task
from reconbot.notifiers.caching import CachingNotifier
from reconbot.notifiers.discord import DiscordNotifier
from reconbot.notifiers.stdout import StdOutNotifier
from reconbot.notifiers.discordwebhook import DiscordWebhookNotifier
from reconbot.notifiers.splitter import SplitterNotifier
from reconbot.notifiers.filter import FilterNotifier
from reconbot.apiqueue import ApiQueue
from reconbot.esi import ESI
from reconbot.sso import SSO

# Configuration

# ESI notification endpoint cache timer in minutes
notification_caching_timer = 10

# Discord bot integration API key and channel
discord = {
    'test-server': {
        'url': os.environ.get('DISCORD_URL')
    }
}

# Eve online SSO application Client ID and Secret Key, used to get access
# tokens for ESI API. Get them on:
# https://developers.eveonline.com/applications
sso_app = {
    'client_id': os.environ.get('CLIENT_ID'),
    'secret_key': os.environ.get('CLIENT_SECRET')
}

# A dictionary of API key groups.
# Get refresh tokens for your characters by following Fuzzwork's guide:
# https://www.fuzzwork.co.uk/2017/03/14/using-esi-google-sheets/
eve_apis = {
    'all': {
        'notifications': {
            'whitelist': None, # allow all notification types
        },
        'characters': {
            's4mur4ri-test': {
                'character_name': os.environ.get('CHARACTER_NAME'),
                'character_id': int(os.environ.get('CHARACTER_ID')),
                'refresh_token': os.environ.get('CHARACTER_REFRESH_TOKEN')
            }
        },
    }
}

my_discord_channels = CachingNotifier(
    SplitterNotifier([
        DiscordWebhookNotifier(
            discord['test-server']['url']
        ),
        StdOutNotifier()
    ]),
    duration=3600
)

def api_to_sso(api):
    return SSO(
        sso_app['client_id'],
        sso_app['secret_key'],
        api['refresh_token'],
        api['character_id']
    )

api_queue_all = ApiQueue(list(map(api_to_sso, eve_apis['all']['characters'].values())))

def notifications_job_all():
    esi_notification_task(
        eve_apis['all']['notifications'],
        api_queue_all,
        'discord',
        my_discord_channels
    )



def run_and_schedule(characters, notifications_job):
    """
    Runs a job immediately to avoid having to wait for the delay to end,
    and schedules the job to be run continuously.
    """
    notifications_job()
    schedule.every(notification_caching_timer/len(characters)).minutes.do(notifications_job)

run_and_schedule(eve_apis['all']['characters'], notifications_job_all)

while True:
    schedule.run_pending()
    time.sleep(1)
