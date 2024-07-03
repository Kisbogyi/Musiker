#!/usr/bin/bash
from typing import List
import discord
from discord.ext.commands import bot
from constants import BOT_TOKEN
import main
from discord import app_commands, message
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='musiker.log', encoding="utf-8", level=logging.DEBUG)

intetns = discord.Intents.default()
intetns.message_content = True

client = discord.Client(intents=intetns)
tree = app_commands.CommandTree(client)
player = main.Player(logger=logger)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=824172801644036117))
    logger.info(f"Logged in as {client.user}")

@tree.command(
    name="hello",
    description="desc",
    guild=discord.Object(id=824172801644036117)
)
async def hello(interaction: discord.Interaction, _: str) -> None:
    await interaction.response.send_message("Hello", ephemeral=True)

@tree.command(
    name="stop",
    description="Stops the current song",
    guild=discord.Object(id=824172801644036117)
)
async def stop(interaction: discord.Interaction) -> None:
    player.stop()
    logger.info("stopping")
    await interaction.response.send_message("playlist stopped", ephemeral=True)

@tree.command(
    name="play",
    description="Starts the current playlist",
    guild=discord.Object(id=824172801644036117)
)
async def start(interaction: discord.Interaction) -> None:
    try:
        logger.info("playlist started")
        await player.play()
        await interaction.response.send_message("Playlist started!", ephemeral=True)
    except Exception as e:
        logger.error(e)

@tree.command(
    name="list",
    description="Lists the songs that are in the playlist",
    guild=discord.Object(id=824172801644036117)
)
async def list(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(player.que, ephemeral=True)


@tree.command(
    name="add",
    description="Add a song to the playlist",
    guild=discord.Object(id=824172801644036117)
)
async def add(interaction: discord.Interaction, music: str) -> None:
    await player.add_to_que(music)
    logger.info("music added")
    await interaction.response.send_message(f"{music} was added to playlist", ephemeral=True)


@tree.command(
    name="status",
    description="ask for status of the player",
    guild=discord.Object(id=824172801644036117)
)
async def status(interaction: discord.Interaction):
    logger.info("status asked")
    await interaction.response.send_message(f"Paused?: {player.paused}", ephemeral=True)

@tree.command(
    name="add_multiple",
    description="ask for status of the player",
    guild=discord.Object(id=824172801644036117)
)
async def add_multiple(interaction: discord.Interaction, m: str):
    logger.info("status asked")
    for musik in m.strip().split(","):
        await player.add_to_que(musik)
    await interaction.response.send_message(f"Paused?: {player.paused}", ephemeral=True)
client.run(BOT_TOKEN)

