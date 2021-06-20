import discord
import os
from keep_alive import keep_alive
import commands

# Discord client instance
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # Prevents the bot from talking to itself
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith(commands.inspire.name):
        await commands.inspire.command(message)

    if msg.startswith(commands.responding.name):
        await commands.responding.command(message)

    if commands.responding.is_enabled():
        if any(word in msg for word in commands.sad.get_sad_words()):
            await commands.sad.command(message)

        if msg.startswith(commands.imagetext.name):
            await commands.imagetext.command(message, discord)

        if msg.startswith(commands.eightball.name):
            await commands.eightball.command(message)

        if msg.startswith(commands.sad_add.name):
            await commands.sad_add.create(message)

        if msg.startswith(commands.sad_del.name):
            await commands.sad_del.delete(message)

# Webserver/ keepalive for the bot
keep_alive()
client.run(os.getenv('TOKEN'))
