import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import time
import env

from discord.ui import Select

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
chat_id = env.chat_id


@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name}')


@bot.command()
async def saludo(ctx):
    username = ctx.author.name
    await ctx.send(f'Hola chaparro, {username} ahora si te voy a subir el sueldo!')


@bot.command()
async def taka(ctx):
    await ctx.send(f'TAKA-TAKA-TAKA-TAKA-TAKA-TAKA-TAKA-TAKA!!!!!')


@bot.command()
async def menu(ctx, interaction):
    selected_value = interaction.data['values'][0]
    if selected_value == '1':
        await interaction.send("Seleccionaste la opción 1")
    elif selected_value == '2':
        await interaction.send("Seleccionaste la opción 2")
    elif selected_value == '3':
        await interaction.send("Seleccionaste la opción 3")

    options = [
        discord.SelectOption(label='Option 1', value='1'),
        discord.SelectOption(label='Option 2', value='2'),
        discord.SelectOption(label='Option 3', value='3')
    ]

    select = discord.ui.Select(
        placeholder='Select some options',
        min_values=0,
        max_values=len(options),
        options=options
    )

    view = discord.ui.View()
    view.add_item(select)
    message = await ctx.send("Mensaje con select:", view=view)


@bot.event
async def on_select_option(interaction):
    if interaction.component.custom_id == 'select':
        selected_value = interaction.values[0]
        ctx = await bot.get_context(interaction.message)

        if selected_value == 'opcion1':
            await bot.invoke(ctx, 'sonido')
        elif selected_value == 'opcion2':
            await bot.invoke(ctx, 'sonido')
        elif selected_value == 'opcion3':
            await bot.invoke(ctx, 'sonido')


@bot.command()
async def sonido(ctx):
    global voice_client
    canal_voz = ctx.author.voice.channel

    if voice_client and voice_client.is_connected():
        await voice_client.move_to(canal_voz)
    else:
        voice_client = await canal_voz.connect()

    audio_source = FFmpegPCMAudio('quierosemen.mp3')
    voice_client.play(audio_source)
    # time.sleep(1)


bot.run(token)
