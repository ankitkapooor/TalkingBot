from transformers import AutoModelForCausalLM, AutoTokenizer
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from model_generator import Generator

#model and tokenizer initialization through HuggingFace
#tokenizer = AutoTokenizer.from_pretrained('Models/epochs_4/')
#model = AutoModelForCausalLM.from_pretrained('Models/epochs_4/')

tokenizer = AutoTokenizer.from_pretrained('Models/20K_steps/')
model = AutoModelForCausalLM.from_pretrained('Models/20K_steps/')
special_token = '<|endoftext|>'

#Creating a discord bot
client = commands.Bot(command_prefix = '!', help_command = None)

#command executed when the bot first comes online
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="bot1"))

#the first message sent by MinecraftLibrarian when it joins a server
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            txt = "Hello there"
            await channel.send(txt)
        break

#constantly runs, takes messages from the user and responds using the provided dataset
@client.event
async def on_message(message):
    msg = message.content.strip()
    reply = Generator.get_reply(msg.strip())
    if message.author == client.user:
        return

    if message.content.startswith(msg) and client.user.mentioned_in(message) and not message.content.startswith('!'):
        await message.channel.send('<@945363896015917096>' + reply)
    await client.process_commands(message)

    #a log of every conversation is recorded on Logs.txt
    with open('Logs.txt', 'a', encoding = "UTF-8") as f:
        f.write(f'Bot1: {msg[23:]}\nBot2: {reply}\n')

#help command: type "!help" to get more information about the bot
@client.command()
async def help(ctx, *, message = "all"):
    name = "bot2!"
    text = 'Just an iteration of the previous bots, here for a little experiment'

    emb = discord.Embed(title = name, description = text, color = 0xf4fc58)
    await ctx.send(embed = emb)

client.run('OTQ1MzY1NTgwOTA1NjExMzE0.YhPGTg.NYNqrvD5KHXT5s9EByQDNrnD57A')
