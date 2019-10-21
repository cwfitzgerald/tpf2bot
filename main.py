import db
import discord
import logging
import os

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.get_all_members()

    members = [m.id for m in client.get_all_members()]
    connection.init_users(members)


@client.event
async def on_message(message):
    if message.author.bot:
        return

    connection.user_message(message.author.id, message.channel.id)

    if message.content.startswith('tpf2!ping'):
        await message.channel.send(f'pong @ {client.latency * 1000:.0f}ms!')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    connection = db.open_database("data/tpf2bot.sqlite", "data/init.sqlite")  # data.

    discord_token = os.getenv("DISCORD_TOKEN")
    if discord_token is not None:
        client.run(discord_token)
    else:
        print("DISCORD_TOKEN not found in environment")
