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
async def first_command(interaction, language):
    await interaction.response.send_message(find_next_meeting(interaction.created_at, language))


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
                await message.channel.send(find_next_meeting(message.created_at, "Bahasa Indonesia"))
            else:
                await message.channel.send(find_next_meeting(message.created_at, "English"))


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
        "Couldn't find a meeting"


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
