from datetime import datetime, timedelta
import socketserver
import threading
import discord
import json
import os

intents = discord.Intents.all()
client = discord.Client(intents=intents)

f = open('weeklyBase.json')

meetingDict = json.load(f)

def create_server():
    s = socketserver.TCPServer(("0.0.0.0", 8656), socketserver.BaseRequestHandler)
    s.serve_forever()


th = threading.Thread(target=create_server)
th.start()


@client.event
async def on_message(message):
    if message.content.startswith("!next-meet"):
        split_message = message.content.split()
        if len(split_message) == 1:
            await message.channel.send(find_next_meeting(message.created_at, "English"))
        else:
            esp_args = ["spanish", "es"]
            chn_args = ["chinese", "zh"]
            rus_args = ["russian", "ru"]
            hin_args = ["hindi", "hi"]
            ben_args = ["bengali", "bn"]
            far_args = ["farsi", "fa"]
            ind_args = ["indonesian", "id"]
            if split_message[1].lower() in esp_args:
                await message.channel.send(find_next_meeting(message.created_at, "Spanish"))
            elif split_message[1].lower() in chn_args:
                await message.channel.send(find_next_meeting(message.created_at, "Chinese"))
            elif split_message[1].lower() in rus_args:
                await message.channel.send(find_next_meeting(message.created_at, "Russian"))
            elif split_message[1].lower() in hin_args:
                await message.channel.send(find_next_meeting(message.created_at, "Hindi"))
            elif split_message[1].lower() in ben_args:
                await message.channel.send(find_next_meeting(message.created_at, "Bengali"))
            elif split_message[1].lower() in far_args:
                await message.channel.send(find_next_meeting(message.created_at, "Farsi"))
            elif split_message[1].lower() in ind_args:
                await message.channel.send(find_next_meeting(message.created_at, "Indonesia"))
            else:
                await message.channel.send(find_next_meeting(message.created_at, "English"))


def increment_day(num):
    if num == 6:
        return 0
    else:
        return num + 1


def find_next_meeting(timestamp, language):
    curr = timestamp
    currweekday = curr.weekday()

    for i in range(7):
        meetings = meetingDict.get(str(currweekday))

        for meeting in meetings:
            meetingday = curr + timedelta(days=1 * i)
            meetingday = meetingday.replace(hour=int(meeting[:2]), minute=int(meeting[3:5]))
            print(meetingday.timestamp())
            if (meetingday - curr).total_seconds() > 0:
                if meetings.get(meeting).get("title") == language:
                    print(meetingday.timestamp())
                    print(str(round(meetingday.timestamp())))
                    return "The next " + language + " meeting is at " + "<t:" + str(round(meetingday.timestamp())) + \
                           ":F> which is in <t:" + str(round(meetingday.timestamp())) + ":R>"

        currweekday = increment_day(currweekday)

    return "Failed to find meeting"


client.run(os.environ["TOKEN"])
