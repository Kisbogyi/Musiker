#!/usr/bin/bash
import discord
from constants import BOT_TOKEN
import main

intetns = discord.Intents.default()
intetns.message_content = True

client = discord.Client(intents=intetns)
player = main.Player()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == ("play"):
        await player.play()
        await message.channel.send("playing")
    if message.content.startswith("add"):
        url = message.content.strip().split()[1]
        await player.add_to_que(url)
        await message.channel.send(player.que)
    if message.content.startswith("$hello"):
        await message.channel.send("hello")
    if message.content == "list":
        await message.channel.send(player.que)
    if message.content == "stop":
        player.stop()

client.run(BOT_TOKEN)

