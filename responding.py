from replit import db

"""
Responding command

Handles bot responding functionality.

Usage:
responding
"""
class Responding:
    bot_responding_db = "responding"

    if bot_responding_db not in db.keys():
        db[bot_responding_db] = True

    def is_enabled(self):
        return db[self.bot_responding_db]

    def __init__(self, name):
        self.name = name

    async def command(self, message):
        value = message.content.split(self.name + " ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")
