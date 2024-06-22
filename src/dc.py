#!/usr/bin/bash
import discord
from discord.ext.commands import bot
from constants import BOT_TOKEN
import main
from discord import app_commands, message

intetns = discord.Intents.default()
intetns.message_content = True

client = discord.Client(intents=intetns)
tree = app_commands.CommandTree(client)
player = main.Player()

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=824172801644036117))
    print(f"Logged in as {client.user}")

@tree.command(
    name="hello",
    description="desc",
    guild=discord.Object(id=824172801644036117)
)
async def hello(interaction: discord.Interaction, _: str) -> None:
    await interaction.response.send_message("Hello")

@tree.command(
    name="stop",
    description="Stops the current song",
    guild=discord.Object(id=824172801644036117)
)
async def stop(interaction: discord.Interaction) -> None:
    player.stop()
    await interaction.response.send_message("playlist stopped")

@tree.command(
    name="play",
    description="Starts the current playlist",
    guild=discord.Object(id=824172801644036117)
)
async def start(interaction: discord.Interaction) -> None:
    await player.play()
    await interaction.response.send_message("Playlist started!")

@tree.command(
    name="list",
    description="Lists the songs that are in the playlist",
    guild=discord.Object(id=824172801644036117)
)
async def list(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(player.que)


@tree.command(
    name="add",
    description="Add a song to the playlist",
    guild=discord.Object(id=824172801644036117)
)
async def add(interaction: discord.Interaction, music: str) -> None:
    await player.add_to_que(music)
    await interaction.response.send_message(f"{music} was added to playlist")

client.run(BOT_TOKEN)

