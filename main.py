from slackclient import SlackClient
from sqlalchemy.sql import select
from sqlalchemy import create_engine
import os
import config
import time


slack_client = SlackClient(config.apiT)
slack_web_client = SlackClient(config.oauthT)

BOTID = config.botID
AT_BOT = "<@"+BOTID+">"

def grab_user(use):
    api = slack_client.api_call('users.list')
    if api.get('ok'):
        users = api.get('members')
        for user in users:
            if 'name' in user and user.get('id') == use:
                return user['name']

def message(channelid, message):
    slack_client.api_call("chat.postMessage",channel=channelid,
    text=message, as_user=True)


def username_to_id(username):
    api =slack_client.api_call('users.list')
    if (api.get('ok')):
        users = api['members']
     
        for user in users:
        
            if 'id'  in user and user['name'] == username:
                return user['id']


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
       for output in output_list:
           if output and 'text' in output and AT_BOT in output['text']:  
            user_name = grab_user(output['user'])
            return output['text'].split(AT_BOT)[1].strip().lower(), \
                   output['channel'], \
                   output['user'], \
                   user_name

    return None, None, "", ""


def handle_command(command,channel,userid,username):
    dividedCommand = command.split()
     
    if(dividedCommand[0] == "test"):
        message(userid,"Sup diggity dog")

    elif(dividedCommand[0] == "hungry"):
        return

    else:
        message(userid, "I FEED YOU, WHY WOULD YOU ASK FOR ANYTHING OTHER COMMAND?!?!?!? USE THE COMMAND hungry! Thank you :D")










#All functions should be above the main

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("Bot connected and running!")
        while True:
            command, channel, userid, username = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command,channel,userid,username)
            time.sleep(READ_WEBSOCKET_DELAY)
    
    else:
        print("Connection failed...")
