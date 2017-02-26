import discord
import asyncio
import time
from os import environ
import random
#from flask import Flask

class Song:
    def __init__(self, url, title, client):
        self.url = url
        self.title = title
        self.client = client
        self.game = discord.Game(name=title)

    def set_playing(self):
        self.client.set_presence(self.game)


USSR = ["http://sovmusic.ru/m/montazhn.mp3", "http://sovmusic.ru/m/ussr44.mp3",
        "http://sovmusic.ru/m/marneft.mp3", "http://sovmusic.ru/m/provodi.mp3",
        "http://sovmusic.ru/m/vzarodin.mp3","http://sovmusic.ru/m/msktime.mp3"]
client = discord.Client()
player = None
voiceChannel = None
@client.event
async def on_ready():
    print("READY!")


async def play(song, message):
    channel = message.author.voice_channel
    print(channel)
    if channel:
        global voiceChannel
        global player
        voiceChannel = await client.join_voice_channel(channel)
        player = voiceChannel.create_ffmpeg_player(song)
        player.start()
    else:
        print("oh no")
        client.send_message(message.channel, "You need to be in a voice channel!")

@client.event
async def on_message(message):
    global player
    if os.environ.get('FRIDAY_TRIGGER') in message.content.lower():
        await play("https://ia801700.us.archive.org/20/items/RebeccaBlackFriday/Rebecca%20Black%20%20-%20Friday.mp3", message)
    elif message.content.startswith('!monday'):
        player.stop()
        await voiceChannel.disconnect()

    elif message.content.startswith('!black '):
        url = message.content[7:]
        print(url)
        await play(url, message)

    elif os.environ.get('USSR_TRIGGER') in message.content and not message.content.startswith("o!"):
        await play(random.choice(USSR), message)

    elif os.environ.get('FROZEN_TRIGGER') in message.content and not message.content.startswith("o!"):
        await play("https://ia801400.us.archive.org/28/items/LetItGo_491/DemiLovato.mp3", message)


#app = Flask(__name__)
#app.run(envioron.get('PORT'))
client.run(os.environ.get('TOKEN'))
