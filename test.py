import json
import os
import socketserver
import threading
from datetime import timedelta

import discord
from discord import app_commands

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

f = open('weeklyBase.json')

meetingDict = json.load(f)


def create_server():
    s = socketserver.TCPServer(("0.0.0.0", 8656), socketserver.BaseRequestHandler)
    s.serve_forever()


th = threading.Thread(target=create_server)
th.start()


@tree.command(name="next-meet", description="Finds the next meet")
async def first_command(interaction, language: str):
    print(interaction.created_at)
    await interaction.response.send_message(find_next_meeting(interaction.created_at, language_parser(language)))


def language_parser(language):
    lang_dict = {"English": ["english", "en"], "Spanish": ["spanish", "es"], "Chinese": ["chinese", "zh"],
                 "Russian": ["russian", "ru"], "Hindi": ["hindi", "hi"], "Bengali": ["bengali", "bn"],
                 "Farsi": ["farsi", "fa"], "Bahasa Indonesia": ["indonesian", "id"]}

    for lang in lang_dict:
        if language in lang_dict.get(lang):
            return lang

@client.event
async def on_message(message):
    if message.content.startswith("!next-meet"):
        split_message = message.content.split()
        if len(split_message) == 1:
            await message.channel.send(find_next_meeting(message.created_at, "English"))
        else:
            await message.channel.send(find_next_meeting(message.created_at, language_parser(split_message[1])))


def increment_day(num):
    if num == 6:
        return 0
    else:
        return num + 1


def find_next_meeting(timestamp, language):
    time = find_next_timestamp(timestamp, language)

    if time:
        return "The next expected {1} meeting is on <t:{0}:D> at <t:{0}:t> which is <t:{0}:R>. You can find the full " \
               "meets schedule at: https://meet.brightid.org/#/".format(time, language)
    else:
        return "Couldn't find a meeting for given language"


def find_next_timestamp(timestamp, language):
    curr = timestamp
    currweekday = curr.weekday()

    for i in range(7):
        meetings = meetingDict.get(str(currweekday))

        for meeting in meetings:
            meetingday = curr + timedelta(days=1 * i)
            meetingday = meetingday.replace(hour=int(meeting[:2]), minute=int(meeting[3:5]))
            if (meetingday - curr).total_seconds() > 0:
                if meetings.get(meeting).get("title") == language:
                    return str(round(meetingday.timestamp()))

        currweekday = increment_day(currweekday)


@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


client.run(os.environ["TOKEN"])