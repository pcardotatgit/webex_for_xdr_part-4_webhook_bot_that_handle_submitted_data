# XDR ALERT WEBEX BOT ( Part 2 )

This project is the second part of the project [webex_for_xdr_part-3_webhook_bot ](https://github.com/pcardotatgit/webex_for_xdr_part-3_webhook_bot).

As we saw in this previous project, the webhook we created handle only messages sent into the Webex Bot room. It is not able to handle the choices we select into the Alert formular.

The reason of that is because the created webhook is  ot a **resource=attachmentActions** webhook. Only such webhook are able to handle selections in formular.

A webhook can have only **resource** type when we create it. That means that is we want our bot to be able to  handle message sent into the bot room and selection done into the formular at the same time, then we have to create 2 webhooks.
One with the **resource=messages** and the other one with **resource=attachmentActions**.

Depending on the action done into the bot room which can be either a message received or a formular submit action, the 2 webhooks will be invoked separatly.

We can identity which webhooks is invoked. Have a look to the **def do_POST(self):** function into the **webex_bot.py** main script. We check if **webhook["resource"]=='messages':**. If yes we manage the message received into the bot room. If no then we parse the data sent thru the formular.

Parsing submitted date consist first by extracting the **webhook['data']['id']** which identify the answers. And second get the **data.id** answers.

The passed data are into the **inputs** key of this answer. 

The content of these **inputs** key will contains the selected data. It will be keys that are user defined.
These key names are defined into the Card JSON data declared into the **alert_card.py** script.

open the **alert_card.py** and locate into the **create_card_content(alert_message)** function the **cards_content** declaration.

First into the first **Action.ShowCard** chunk ( target list choice ) line 84 :

    {
        "type": "Input.ChoiceSet",
        "id": "targets",
    ...

**targets** is the **id** I decided to assign to this selection.

Then go to line 97 :

    {
        "type":"ActionSet",
        "actions": [
            {
                "type": "Action.Submit",
                "title": "Isolate Selected Systems",
                "data": {
                    "objects": "Targets"
                }
            }
        ]                                
    }

I decided to create a key name **objects** with **Targets** as value in the **data** key
    
And now go to the second **Action.ShowCard** chunk ( observables list choice ).

Based on the same principle you will see that I decided to assign **observables** as the **id** of the observable selection. And I created the **"objects": "observables"** key and value into the **data**

The objects vlaue are what help to understand how to parse submitted data depending on the fact that this is **targets** or **observables**. We do this thanks to an **if statement** into the **def do_POST(self):** function of the **webex_bot.py** script.

    if result['inputs']['objects']=="Targets":
        sent_variables=result['inputs']['targets']
    else:
        sent_variables=result['inputs']['observables']

Final operation is just to make the bot send a confirmation message with selected objects into it's room 

## Install and run the script

The installation is the same as the previous section. In this current repo the **webex_bot.py** is the only file that had been updated.

That means that if you have done the installation for the previous section, then you can just replace the **webex_bot.py** script the one in this repo.

And then run the script 

    python webex_bot.py
    
## Test the bot

Once the script runs, go to Webex and send the **alert_card** message to the bot room.

You should see the alert formular appearing. Then you should be able to select objects either in the target list or in the observables list.
Click on the submit button.

First you should see a message from the bot into the room which confirm you your choices, and second you should see the details of operations into the bot console.  

## Where to go Next : Websocket Bot

This next section is under construction

Go to the previous section

[webex_for_xdr_part-3_webhook_bot ](https://github.com/pcardotatgit/webex_for_xdr_part-3_webhook_bot)

