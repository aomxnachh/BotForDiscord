import discord
import random
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='./' , intents=discord.Intents.all())

TOKEN= 'MTI5Mzg4NjM2ODc0NDg2OTkzOQ.GeeEcH.hPGgwZl4nVe122J_mHQCI7F1vUPA7RpL0iEGZc'

#Bot Event
@bot.event
async def on_ready():
    print("KoKo is awake!!!")

#who enter or out
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1293939779976695901)
    text = f"Welcome to the island, {member.mention}!"
    #Embed
    emmbed = discord.Embed(title = 'Welcome to the island!!!',
                            descipton = text,
                            color = 0x66FFFF)
    await channel.send(text)
    await channel.send(embed = emmbed)

@bot.event
async def  on_member_remove(member):
    channel = bot.get_channel(1293939779976695901)
    text = f"Goodbye, {member.mention} Skibidi"
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
async def meme(ctx):
    image_folder = "image/"
    images = os.listdir(image_folder)
    images = [img for img in images if img.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if not images:
        await ctx.channel.send("No images found in the folder.")
        return
    selected_image = random.choice(images)
    image_path = os.path.join(image_folder, selected_image)
    file = discord.File(image_path, filename=selected_image)
    embed = discord.Embed(title="Meme!", color=0x66FFFF)
    embed.set_image(url=f"attachment://{selected_image}")
    await ctx.channel.send(embed=embed, file=file)

bot.run(TOKEN)
