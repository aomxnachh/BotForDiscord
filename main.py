import discord
import random
import os
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

# When a member leaves
@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    if channel is not None:
        text = f"Goodbye, {member.mention}! Skibidi"
        await channel.send(text)

#hello
@bot.command()
async def hello(ctx):
    text = f"KoKo Sawasdee {ctx.author.mention} Kub Jub Jub"
    file = discord.File("image/Kokosawasdee.jpg", filename="Kokosawasdee.jpg")
    embed = discord.Embed(title='Hello', description=text, color=0x66FFFF)
    embed.set_image(url="attachment://Kokosawasdee.jpg")
    await ctx.channel.send(embed=embed, file=file)

#meme
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

#coin flip
@bot.command()
async def coin(ctx,ip):
    ip=ip.lower()
    num = random.randint(1,2)
    if num == 1 and ip == "head":
        Head = discord.Embed(title="Correct,It Head!!!",color=0x80ff00)
        await ctx.send(embed=Head)
    elif num == 2 and ip == "tail":
        Tail = discord.Embed(title="Correct,It Tail!!!",color=0x80ff00)
        await ctx.send(embed=Tail)
    else:
        Wrong = discord.Embed(title="It wrong are you smart?",color=0x80ff00)
        await ctx.send(embed=Wrong)


#help
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help",color=0x80ff00)
    embed.add_field(name="./hello",value="to greet you",inline=False)
    embed.add_field(name="./meme",value="to generate meme of cs",inline=False)
    embed.add_field(name="./coin",value="to guess flip coin",inline=False)
    await ctx.send(embed=embed)

server_on()

bot.run(os.getenv('TOKEN'))
