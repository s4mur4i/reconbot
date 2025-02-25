Reconbot for Eve Online [![CircleCI](https://circleci.com/gh/flakas/reconbot.svg?style=svg)](https://circleci.com/gh/flakas/reconbot)
=======================

Reconbot is a notification relay bot for an MMO game [Eve Online](http://secure.eveonline.com/signup/?invc=905e73a0-eb57-49ab-8fe5-9759c2ba5e99&action=buddy).
It fetches character notifications from the EVE API, filters irrelevant ones out and sends relevant ones to set Slack or Discord channels.
Notifications like SOV changes, SOV/POS/POCO/Citadel attacks.

# Setup

Reconbot was intended to be used as a base for further customizations, or integration with other systems, but it can be run via `run.py` as well. Check it out for an example.

## 1. EVE Developer Application

This tool is ready to be used with [Eve's ESI API](https://esi.tech.ccp.is/). You will need to register your application on [EVE Developers page](https://developers.eveonline.com/applications).

When registering your EVE Application, please pick `Authentication & API Access` connection type, and make sure your application requests these permissions:

- `esi-universe.read_structures.v1` - necessary to fetch names of any linked structures;
- `esi-characters.read_notifications.v1` - necessary to fetch character level notifications.

Reconbot does not provide a way to authenticate an account to an application, so you will need to do so via some other means. First two sections of Fuzzysteve's guide on [Using ESI with Google Sheets](https://www.fuzzwork.co.uk/2017/03/14/using-esi-google-sheets/) explain how to do that via [Postman](https://www.getpostman.com/).

When registering the application take note of the `Client ID` and `Secret Key`, as they are necessary for Reconbot to establish communication with ESI API.

## 2.Discord chat tools

### Discord

__If you wish to use a Discord webhook:__

Webhooks are the easiest way to integrate Reconbot with Discord. Simply follow [this Discord guide](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks) to create a webhook for your channel.
You should now have a URL like this:
```
https://discordapp.com/api/webhooks/496014874437332490/5783au24jzyEFIaWnfTvJn0gFzh5REEEE3ee3e3eNKeFee3We2cIe_6e7e36ugUj5zEm
```
Use it with `DiscordWebhookNotifier` as seen in `run.py` example.

__If you wish to use a Discord bot user:__ (not recommended)

To add a Discord integration, check out [this Discord documentation page on Bot accounts](https://discordapp.com/developers/docs/topics/oauth2#bots).
You will need to [create an application](https://discordapp.com/developers/applications/me#top) and add it to your discord server.
See [this guide](https://github.com/Chikachi/DiscordIntegration/wiki/How-to-get-a-token-and-channel-ID-for-Discord) for more visual step-by-step instructions.
You will need a `Token` for your Bot User, and `Channel ID` where to post messages in.
Use it with `DiscordNotifier` as seen in `run.py` example.

## 3. Reconbot setup

1. Clone this repository
2. Create a virtualenv environment: `virtualenv -p python3 venv`
3. Activate the virtualenv environment: `source venv/bin/activate`. This will isolate reconbot's dependencies from the rest of your system's dependencies.
4. Install Python depdendencies: `pip3 install -r requirements.txt`
5. Modify `run.py` with your EVE API keys, key groups and Slack/Discord accounts/channels.
  `whitelist` should contain notification types you're interested in (or `None` to allow all supported types), and `characters` should contain entries for API keys of individual characters.
6. Execute `python3 run.py` and wait for notifications to arrive! After the character gets a notification in-game, `reconbot` may take up to 10 minutes to detect the notification.

# Other notes

Reconbot by default will try to evenly spread out checking API keys over the cache expiry window (which is 10 minutes for ESI), meaning that with 2 API keys in rotation an API key will be checked every ~5 minutes (with 10 keys - every minute), which can be useful to detect alliance or corporation-wide notifications more frequently than only once every 10 minutes.

## Supported notifications

As of writing this tool there is little documentation about the types of notifications available and their contents. The following list has been assembled from working experience, is not fully complete and may be subject to change as CCP changes internals:

- AllWarDeclaredMsg
- DeclareWar
- AllWarInvalidatedMsg
- AllyJoinedWarAggressorMsg
- CorpWarDeclaredMsg
- EntosisCaptureStarted
- SovCommandNodeEventStarted
- SovStructureDestroyed
- SovStructureReinforced
- StructureUnderAttack
- OwnershipTransferred
- StructureOnline
- StructureDestroyed
- StructureFuelAlert
- StructureWentLowPower
- StructureWentHighPower
- StructureFuelAlert
- StructureAnchoring
- StructureUnanchoring
- StructureServicesOffline
- StructureLostShields
- StructureLostArmor
- TowerAlertMsg
- TowerResourceAlertMsg
- StationServiceEnabled
- StationServiceDisabled
- OrbitalReinforced
- OrbitalAttacked
- SovAllClaimAquiredMsg
- SovStationEnteredFreeport
- AllAnchoringMsg
- InfrastructureHubBillAboutToExpire
- SovAllClaimLostMsg
- SovStructureSelfDestructRequested
- SovStructureSelfDestructFinished
- StationConquerMsg
- MoonminingExtractionStarted
- MoonminingExtractionCancelled
- MoonminingExtractionFinished
- MoonminingLaserFired
- MoonminingAutomaticFracture
- CorpAllBillMsg
- BillPaidCorpAllMsg
- CharAppAcceptMsg
- CorpAppNewMsg
- CharAppWithdrawMsg
- CharLeftCorpMsg
- CorpNewCEOMsg
- CorpVoteMsg
- CorpVoteCEORevokedMsg
- CorpTaxChangeMsg
- CorpDividendMsg
- BountyClaimMsg
- KillReportVictim
- KillReportFinalBlow
- AllianceCapitalChanged

## Docker 

following env variables are needed

| Variable  | Function |
| ------------- | ------------- |
| DISCORD_URL  | Webhook url for posting messages  |
| CLIENT_ID  | eve application client id  |
| CLIENT_SECRET  | eve application client secret  |
| CHARACTER_NAME  | Character name  |
| CHARACTER_ID  |  Character id |
| CHARACTER_REFRESH_TOKEN  | refresh token  |

Refresh token can be goten with following guide: https://www.fuzzwork.co.uk/2017/03/14/using-esi-google-sheets/

## How to use

Create a file named `.env` with content in root place:
```angular2html
DISCORD_URL=https://discord.com/api/webhooks/xxxx
CLIENT_ID=xxx
CLIENT_SECRET=xxx
CHARACTER_NAME=xxx
CHARACTER_ID=xxx
CHARACTER_REFRESH_TOKEN=xxx-xxx
```

Build the local container
```angular2html
docker build -t reconbot .
```
 
Run the container
```angular2html
docker run -d reconbot
```

If you want to run dockerhub version:
```angular2html
docker run -d -e DISCORD_URL=https://discord.com/api/webhooks/xxx -e CLIENT_ID=xxx -e CLIENT_SECRET=xxx -e CHARACTER_NAME=xxx -e CHARACTER_ID=xxx -e CHARACTER_REFRESH_TOKEN=xxx-xxx  s4mur4i/reconbot
```