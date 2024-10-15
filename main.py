import discord
import random
import os
from pytube import YouTube
import asyncio
from discord.ext import commands

from myserver import server_on

bot = commands.Bot(command_prefix='./' , intents=discord.Intents.all())
bot.remove_command("help")

#Bot Event
@bot.event
async def on_ready():
    print("KoKo is awake!!!")

#who enter or out
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        text = f"Welcome to the island, {member.mention}!"
        # Embed
        embed = discord.Embed(title='Welcome to the island!!!',
                              description=text,
                              color=0x66FFFF)
        await channel.send(text)
        await channel.send(embed=embed)

#when a member leaves
@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    if channel is not None:
        text = f"Goodbye, {member.mention}! Skibidi"
        await channel.send(text)

#hello section
@bot.command()
async def hello(ctx):
    text = f"KoKo Sawasdee {ctx.author.mention} Kub Jub Jub"
    file = discord.File("image/Kokosawasdee.jpg", filename="Kokosawasdee.jpg")
    embed = discord.Embed(title='Hello', description=text, color=0x66FFFF)
    embed.set_image(url="attachment://Kokosawasdee.jpg")
    await ctx.channel.send(embed=embed, file=file)

#meme section
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

#coin section
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
queue = []

#check bot
def is_connected(ctx):
    return ctx.voice_client is not None

#func to play next queue
async def play_next_song(ctx):
    if len(queue) > 0:
        url = queue.pop(0)
        await play_song(ctx, url)
    else:
        await ctx.voice_client.disconnect()

#func to play music
async def play_song(ctx, url):
    vc = ctx.voice_client
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first().url

    ffmpeg_opts = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    vc.play(discord.FFmpegPCMAudio(audio_stream, **ffmpeg_opts),
            after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(ctx), bot.loop))

#join voice
@bot.command()
async def p(ctx, url):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return
    channel = ctx.author.voice.channel
    if not is_connected(ctx):
        await channel.connect()
    queue.append(url)
    await ctx.send(f"Added to queue: {url}")
    if not ctx.voice_client.is_playing():
        await play_next_song(ctx)

#skip the current song
@bot.command()
async def skip(ctx):
    if not is_connected(ctx):
        await ctx.send("I am not in a voice channel.")
        return
    if not ctx.voice_client.is_playing():
        await ctx.send("There is no song playing right now.")
        return
    ctx.voice_client.stop()
    await ctx.send("Skipped the song!")

#stop playing
@bot.command()
async def stop(ctx):
    if not is_connected(ctx):
        await ctx.send("I am not in a voice channel.")
        return

    queue.clear() #clear the queue
    await ctx.send("Stopping and leaving the voice channel.")
    await ctx.voice_client.disconnect()

#bot leave
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is not None and after.channel is None:
        if member == bot.user:
            await member.guild.voice_client.disconnect()

#help section
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", color=0x80ff00)
    embed.add_field(name="./hello", value="to greet you", inline=False)
    embed.add_field(name="./meme", value="to generate meme of cs", inline=False)
    embed.add_field(name="./coin", value="to guess flip coin", inline=False)
    await ctx.send(embed=embed)

server_on()

bot.run(os.getenv('TOKEN'))
