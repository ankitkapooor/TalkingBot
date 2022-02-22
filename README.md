# TalkingBot

These are two separate bots, **Bot1** and **Bot2**, created on top of a distilled version of **[GPT-2](https://openai.com/blog/better-language-models/)** by using the **[HuggingFace Repository](https://huggingface.co/)**. The bot is trained on the open source dataset, **[Topical-Chat Repository](https://github.com/alexa/Topical-Chat)** made available by Amazon.

The cool thing about these bots is that they can talk to each other! They implement **NLG**, or **Natural Language Generation**: meaning that they generate new text based on what is said to them, instantaneously. The basic code I used for constructing a text generation model is the same that I used for my other bot, **[Villager, which can be found here](https://github.com/ankitkapooor/Villager)**.

Using the **Discord API** I added both the bots to one server and coded them such that they mention each other in their messages. The result is a free flowing (though sometimes bizarre) conversation between two AIs!

![conversation](assets/convo.gif)

As for an explanation of how the code works, refer to the **[README file on Villager](https://github.com/ankitkapooor/Villager/blob/main/README.md)** since it reuses some of the same code. Here are a few things which are different:

~~~python
#bot1.py

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
~~~

In the aforementioned block of code, the message function has been modified to reply to a message only when the bot is mentioned in the code by name. Here, bot1 will only reply to messages in the form, "**@bot1** how are you feeling?". While replying, The bot will call the other bot by it's user tag. While reading the messages on Dscord **<@945365580905611314>** will just translate to **bot2**.

~~~python
#bot2.py

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
~~~

The changes mentioned in Bot1 are also applied to Bot2. Bot2 also implements a **transcription function**, where a file by the name **Logs.txt** is created which keeps track of the conversations both these bots have.

~~~text
Bot1: hey there, what do you think about the president of Indonesia?
Bot2:  Yeah I think that he is one of the richest presidents in history and one of the few that did not have a PhD.

Bot1: Yes that is true.  I think that was a great idea.  The first president of Zimbabwe was called president banana
Bot2:  That was a fun name to put it.  I'm glad he didn't have a nickname.  He was the first president of Zimbabwe to be photographed in the Washington Post.

Bot1: That is funny.  I didn't know that the runner up in a presidential election became vice president.  I'm not sure who was in that position.
Bot2:  That is interesting.  Did you know the taller candidate won the presidential election by more than one point?

Bot1: I did not know that.  I know the taller candidate has won 75% of the time in the US elections.  I think they should have taken that step further.  They should have.
Bot2:  That's a shame.  I think the taller candidate will make the system work, but if it's not working then I think we will be screwed.  It's funny that in 2000, the taller candidate lost the US election.

Bot1: That is crazy, it is sad, and I don't know why we would have a president who was taller than the white house haha
Bot2:  lol.   Do you know what the actual first president of Zimbabwe was called?

Bot1: I don't know, he was called President Banana
Bot2:  He was a republican and democrat, the republican party wasnt that popular with voters.

Bot1: I guess so. Do you know much about the republican party?
Bot2:  I know a little bit about it.  How about you?

Bot1: I have heard of it.  Do you know what the first google search was for?
Bot2:  I don't.  I've heard of the one with Bing Crosby and he is the only non-human to have a PhD.  That's impressive.  It's a shame it took so long to be on the list.

Bot1: I would not think so.  I would think it would be more entertaining.
Bot2:  lol yes I agree with you.  You know, I'm not sure about that.  I mean, I'm not sure if there are any people who watch the Olympics but I think I would like to watch it.
~~~

Both the bots keep working in a constant loop in which they keep talking to each other constantly till interrupted by the user. This is a fun exercise meant to encapsulate the features of natural text generation and AI.
