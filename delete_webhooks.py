'''
    delete all webhooks attached to the bot
    
'''
import urllib.request as urllib2
import json
import ssl
#import re
import requests
#from operator import itemgetter
from config import *
from crayons import *
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
Dest_Room_ID_List=[]
# USED FOR OFF-LINE DEBUG
delete_current_webhook=1 # confirm webhook deletion
  
def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts=False):
    if type(data) == 'str':
        return data.encode('utf-8')
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items()
        }
    return data
    
def delete_webhook(webhook_id):

    url = "https://webexapis.com/v1/webhooks/" + webhook_id

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + bearer
    }

    requests.request("DELETE", url, headers=headers, data=payload)

def get_bot_status():
    url = "https://webexapis.com/v1/rooms"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + bearer
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json_loads_byteified(response.text)
    print(yellow("Bot is currently member of the following Webex Rooms:",bold=True))
    print()
    room_choices=[]
    index=0
    global Dest_Room_ID_List
    if 'items' in data:
        for room in data['items']:
            print(green(f"{index}    ID: {room['title']}",bold=True))
            Dest_Room_ID_List.append(room['id'])
            room_choices.append(room['title']+';'+room['id'])
            index+=1
    print()       
    url = "https://webexapis.com/v1/webhooks"
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json_loads_byteified(response.text)
    print(green("Bot is currently configured with webhooks:",bold=True))   
    if 'items' in data:
        for webhook in data['items']:
            print(" => Webhook ID: {}".format(webhook['id']))
            if delete_current_webhook:
                # for testing : cleaning reseting webhook 
                print(red("    === REMOVING WEBHOOK ===",bold=True))
                delete_webhook(webhook['id'])
                print(red("    === REMOVED ===",bold=True))
            
def main():
    print() 
    print(white(f'==== Delete Webex Bot Webhooks version : {version} ====',bold=True))
    print()
    global webhook_url
    get_bot_status()

if __name__== "__main__":
    main()
