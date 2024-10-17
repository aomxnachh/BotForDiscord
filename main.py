import discord
import random
import os
import youtube_dl
from discord.ext import commands

from myserver import server_on

bot = commands.Bot(command_prefix='./', intents=discord.Intents.all())
bot.remove_command("help")

# Bot Event
@bot.event
async def on_ready():
    print("KoKo is awake!!!")

# who enter or out
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        text = f"Welcome to the island, {member.mention}!"
        embed = discord.Embed(title='Welcome to the island!!!', description=text, color=0x66FFFF)
        await channel.send(text)
        await channel.send(embed=embed)

# when a member leaves
@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    if channel is not None:
        text = f"Goodbye, {member.mention}! Skibidi"
        await channel.send(text)

# hello section
@bot.command()
async def hello(ctx):
    text = f"KoKo Sawasdee {ctx.author.mention} Kub Jub Jub"
    file = discord.File("image/Kokosawasdee.jpg", filename="Kokosawasdee.jpg")
    embed = discord.Embed(title='Hello', description=text, color=0x66FFFF)
    embed.set_image(url="attachment://Kokosawasdee.jpg")
    await ctx.channel.send(embed=embed, file=file)

# meme section
@bot.command()
async def meme(ctx, number_of_memes: int = 1):
    image_folder = "image/"
    images = os.listdir(image_folder)
    images = [img for img in images if img.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if not images:
        await ctx.channel.send("No images found in the folder.")
        return

    if number_of_memes < 1:
        await ctx.channel.send("The number of memes must be at least 1.")
        return
    elif number_of_memes > 5:
        await ctx.channel.send("You can't request more than 5 memes.")
        return
    selected_images = random.sample(images, k=min(number_of_memes, len(images)))

    for selected_image in selected_images:
        image_path = os.path.join(image_folder, selected_image)
        file = discord.File(image_path, filename=selected_image)
        embed = discord.Embed(title="Meme!", color=0x66FFFF)
        embed.set_image(url=f"attachment://{selected_image}")
        await ctx.channel.send(embed=embed, file=file)

# coin section
@bot.command()
async def coin(ctx, ip):
    ip = ip.lower()
    num = random.randint(1, 2)
    if num == 1 and ip == "head":
        Head = discord.Embed(title="Correct, It’s Head!!!", color=0x80ff00)
        await ctx.send(embed=Head)
    elif num == 2 and ip == "tail":
        Tail = discord.Embed(title="Correct, It’s Tail!!!", color=0x80ff00)
        await ctx.send(embed=Tail)
    else:
        Wrong = discord.Embed(title="It’s wrong! Are you smart?", color=0x80ff00)
        await ctx.send(embed=Wrong)

#music section
queues = {}

@bot.command()
async def p(ctx, url: str):
    if "youtube.com" not in url and "youtu.be" not in url:
        await ctx.send("Please provide a valid YouTube URL.")
        return

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("You need to be in a voice channel to play music.")
        return

    voice_client = await connect_to_channel(ctx, voice_channel)
    
    # Add the song to the queue
    if ctx.guild.id not in queues:
        queues[ctx.guild.id] = []
    
    if not voice_client.is_playing():
        await play_song(ctx, url)
    else:
        queues[ctx.guild.id].append(url)
        await ctx.send("Added to queue.")

# Skip the current song
@bot.command()
async def skip(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is not None and voice_client.is_playing():
        voice_client.stop()  # Stop the current song, automatically moves to next in queue

# Stop and clear the queue
@bot.command()
async def stop(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is not None:
        queues[ctx.guild.id] = []  # Clear the queue
        await voice_client.disconnect()  # Disconnect from the voice channel

async def connect_to_channel(ctx, voice_channel):
    voice_client = ctx.guild.voice_client
    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel)
    return voice_client

async def play_song(ctx, url):
    voice_client = ctx.guild.voice_client
    if voice_client is None:
        await ctx.send("I'm not in a voice channel.")
        return

    with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']

    voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=URL), after=lambda e: check_queue(ctx))

async def check_queue(ctx):
    if queues[ctx.guild.id]:
        next_song = queues[ctx.guild.id].pop(0)  # Get the next song from the queue
        await play_song(ctx, next_song)
    else:
        voice_client = ctx.guild.voice_client
        if voice_client is not None:
            await voice_client.disconnect()  # Disconnect if the queue is empty

server_on()

bot.run(os.getenv('TOKEN'))
