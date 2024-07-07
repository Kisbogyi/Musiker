#!/usr/bin/bash
import discord
from constants import BOT_TOKEN
import main
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="musiker.log", encoding="utf-8", level=logging.DEBUG)

bot = discord.Bot()

# bot = discord.Client(intents=intetns)
player = main.Player(logger=logger)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")


@bot.command(description="test command")
async def hello(interaction: discord.Interaction, _: str) -> None:
    await interaction.response.send_message("Hello", ephemeral=True)


@bot.command(
    description="Stops the current song",
)
async def stop(interaction: discord.Interaction) -> None:
    player.stop()
    logger.info("stopping")
    await interaction.response.send_message("playlist stopped", ephemeral=True)


@bot.command(
    description="Starts the current playlist",
)
async def start(interaction: discord.Interaction) -> None:
    try:
        logger.info("playlist started")
        await player.play()
        await interaction.response.send_message("Playlist started!", ephemeral=True)
    except Exception as e:
        logger.error(e)


@bot.command(
    description="Lists the songs that are in the playlist",
)
async def list(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(player.que, ephemeral=True)


@bot.command(
    description="Add a song to the playlist",
)
async def add(interaction: discord.Interaction, music: str) -> None:
    await player.add_to_que(music)
    logger.info("music added")
    await interaction.response.send_message(
        f"{music} was added to playlist", ephemeral=True
    )


@bot.command(
    description="ask for status of the player",
)
async def status(interaction: discord.Interaction):
    logger.info("status asked")
    await interaction.response.send_message(f"Paused?: {player.paused}", ephemeral=True)


@bot.command(
    description="ask for status of the player",
)
async def add_multiple(interaction: discord.Interaction, m: str):
    logger.info("status asked")
    for musik in m.strip().split(","):
        await player.add_to_que(musik)
    await interaction.response.send_message(f"Paused?: {player.paused}", ephemeral=True)


@bot.command(description="Clears the playlist")
async def clear(interaction):
    await player.clear_songs()
    await interaction.response.send_message("Playlist cleared", ephemeral=True)


@bot.command(description="Skip currently playing music")
async def skip(interaction):
    await player.skip()
    await interaction.response.send_message("Skipped music")


bot.run(BOT_TOKEN)
