#!/usr/bin/python3
import discord
from constants import BOT_TOKEN
import main
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="musiker.log", encoding="utf-8", level=logging.DEBUG)

bot = discord.Bot()

# bot = discord.Client(intents=intetns)
player = main.Player()


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")


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
        player.play()
        await interaction.response.send_message("Playlist started!", ephemeral=True)
    except Exception as e:
        logger.error(e)


@bot.command(
    description="Lists the songs that are in the playlist",
)
async def list(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(player.playlist, ephemeral=True)


@bot.command(
    description="Add a song to the playlist",
)
async def add(interaction: discord.Interaction, music: str) -> None:
    player.add(music)
    logger.info("music added")
    await interaction.response.send_message(
        f"{music} was added to playlist", ephemeral=True
    )

@bot.command(description="Clears the playlist")
async def clear(interaction):
    player.clear()
    await interaction.response.send_message("Playlist cleared", ephemeral=True)


@bot.command(description="Skip currently playing music")
async def skip(interaction):
    player.skip()
    await interaction.response.send_message("Skipped music", ephemeral=True)


bot.run(BOT_TOKEN)
