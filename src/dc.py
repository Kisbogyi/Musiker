#!/usr/bin/python3
import discord
import discord.ui.modal
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

@bot.command() # Create a slash command
async def button(interaction):
    await interaction.respond("This is a button!", view=MyView()) # Send a message with our View class that contains the button

class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked

@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(interaction) -> None: # a slash command will be created with the name "ping"
    message = discord.Embed(title="ping", description=f"Pong! Latency is {bot.latency}")
    await interaction.respond(embeds=[message])

@bot.listen()
async def on_connect():
    print('Bot has connected!')
    await bot.sync_commands()
    print("Commands synced")

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])

@bot.slash_command()
async def modal_slash(ctx: discord.ApplicationContext):
    """Shows an example of a modal dialog being invoked from a slash command."""
    modal = MyModal(title="Modal via Slash Command")
    await ctx.send_modal(modal)

bot.run(BOT_TOKEN)
