import discord
import env
import asyncio

from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ui import Button, View


ffmpeg_path = 'C:\ffmpeg\bin\ffmpeg.exe'
discord.FFmpegPCMAudio.executable = ffmpeg_path


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents = discord.Intents.default()
intents.message_content = True
voice_client = None

bot = commands.Bot(command_prefix='!', intents=intents)

token = env.token
buttons_data = env.buttons_data

@bot.event
async def on_message(message):
    # Ignora los mensajes del bot
    if message.author == bot.user:
        return

    # Borra el mensaje anterior del bot
    async for msg in message.channel.history(before=message):
        if msg.author == bot.user:
            await msg.delete()

    message.content = '!menu'
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name}')


@bot.command()
async def menu(ctx):
    global buttons_data
    view = View()

    for button_data in buttons_data:
        button = Button(label=button_data["label"], style=button_data["style"])

        async def button_callback(interaction, sound=button_data["sound"]):
            await sonido(ctx, sound)
            await interaction.response.defer()

        button.callback = button_callback
        view.add_item(button)
    await ctx.send(view=view)


@bot.command()
async def sonido(ctx, sonido):
    global voice_client
    
    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel
    
    if ctx.author.voice is None:
        await ctx.send("You must be in a voice channel to use this command.")
        return

    if voice_client and voice_client.is_connected():
        await voice_client.move_to(voice_channel)
    else:
        voice_client = await voice_channel.connect()

    audio_source = FFmpegPCMAudio(sonido)
    voice_client.play(audio_source)

bot.run(token)
