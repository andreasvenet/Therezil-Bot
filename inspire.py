import requests
import json

"""
Inspire command

Gets an inspirational quote from zenquotes.

Usage:
inspire
"""
class Inspire:
    def __init__(self, name):
        self.name = name

    def get_quote():
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        return (quote)

    async def command(self, message):
        quote = self.get_quote()
        await message.channel.send(quote)
