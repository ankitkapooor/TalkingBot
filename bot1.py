from transformers import AutoModelForCausalLM, AutoTokenizer
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from model_generator import Generator

#model and tokenizer initialization through HuggingFace
tokenizer = AutoTokenizer.from_pretrained('Models/20K_steps/')
model = AutoModelForCausalLM.from_pretrained('Models/20K_steps/')
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

    if message.content.startswith(msg) and client.user.mentioned_in(message) and not message.content.startswith('!') and len(stop_list) == 0:
        await message.channel.send('<@945365580905611314> ' + reply)
    await client.process_commands(message)

#help command: type "!help" to get more information about the bot
@client.command()
async def help(ctx, *, message = "all"):
    name = "bot1!"
    text = '**!help**: Provides a list of all the commands\n**!start** or **!start <prompt>**: Starts the conversation between the bots\n**!stop**: Halts the conversation between the bots.'

    emb = discord.Embed(title = name, description = text, color = 0xf4fc58)
    await ctx.send(embed = emb)

#an easy way to start and stop the bots
stop_list = []
@client.command()
async def stop(ctx):
    stop_list.append("stop")
    emb = discord.Embed(
        title = "You have stopped the conversation",
        description = "Press **!start**, or **!start <prompt>** to start the conversation again, or press **!help** for more information!",
        color = 0xf4fc58
    )
    await ctx.send(embed = emb)

@client.command()
async def start(ctx, *, message = "Hi"):
    stop_list.clear()

    if message == "Hi":
        prompt = "Default Prompt"
    else:
        prompt = message

    emb = discord.Embed(
        title = "You have started the conversation",
        description = f"**Prompt**: {prompt}\n\nType **!stop** to stop the conversation at any time, type **!help** to get more information!",
        color = 0xf4fc58
    )
    await ctx.send(embed = emb)
    await ctx.send(f"{'<@945365580905611314>'} {message}")

client.run('ENTER BOT TOKEN HERE')
