from transformers import AutoModelForCausalLM, AutoTokenizer
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from model_generator import Generator

#model and tokenizer initialization through HuggingFace
tokenizer = AutoTokenizer.from_pretrained('Models/epochs_4/')
model = AutoModelForCausalLM.from_pretrained('Models/epochs_4/')
special_token = '<|endoftext|>'

#Creating a discord bot
client = commands.Bot(command_prefix = '!', help_command = None)

#command executed when the bot first comes online
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="bot2"))

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
        await message.channel.send('<@945365580905611314> ' + reply)
    await client.process_commands(message)

#help command: type "!help" to get more information about the bot
@client.command()
async def help(ctx, *, message = "all"):
    name = "bot1!"
    text = 'Just an iteration of the previous bots, here for a little experiment'

    emb = discord.Embed(title = name, description = text, color = 0xf4fc58)
    await ctx.send(embed = emb)

client.run('OTQ1MzYzODk2MDE1OTE3MDk2.YhPEvA.besVutzZNDeqoviqA5FzhkoWUg0')
