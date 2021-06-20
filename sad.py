import time
import bot_sync
from bot_logging import log_action
from replit import db
import random

"""
Sad command

A command that sends out random custom quotes added by users.

Usage:
sad
$del <id>
$new <message>
"""
class Sad:
    # Sad database index on repl.it
    sad_db = "encouragements"

    # Chances of displaying multiple combo messages when using 'sad'
    sad_chances_of_second_msg = 31
    sad_chances_of_third_message = 2

    # Starting sad message in case there's none
    starter_sad = ["o magaras einai t-word"]

    # Sad keywords
    sad_words = [
        "sad", 
        "depressed", 
        "unhappy", 
        "miserable", 
        "depressing", 
        "magkaras",
        "malakas", 
        "θλιψη", 
        "thlipsi", 
        "θλίψη", 
        "tsiab", 
        "σαδ"
    ]

    def get_sad_words(self):
        return self.sad_words

    def __init__(self, name):
        self.name = name

    def update_sad(self, message):
        if self.sad_db in db.keys():
            encouragements = db[self.sad_db]
            encouragements.append(message)
            db[self.sad_db] = encouragements
        else:
            db[self.sad_db] = [message]

    def delete_sad(self, index):
        encouragements = db[self.sad_db]
        if len(encouragements) > index:
            del encouragements[index]
            db[self.sad_db] = encouragements

    async def command(self, message):
        if self.sad_db in db.keys():
            options = self.starter_sad
            options = options + db[self.sad_db]

        await message.channel.send(random.choice(options))
        if (random.randint(1, 100) > 100 - self.sad_chances_of_second_msg):
            await message.channel.send(random.choice(options))
            if (random.randint(1, 100) >
                    100 - self.sad_chances_of_third_message):
                await message.channel.send(random.choice(options))
        pass

    async def delete(self, message):
        if self.sad_db in db.keys():
            index = int(message.split(self.name, 1)[1])
            self.delete_sad(index)
        ts = time.ctime(int(time.time()))
        log_action("{}: Message {} deleted by @{} in channel #{}".format(
            ts, index, message.author, message.channel))
        await message.channel.send(
            "Message with id {} has been deleted!".format(index))
        pass

    async def create(self, message):
        sad_message = message.content.split(self.name + " ", 1)[1]
        ts = time.ctime(int(time.time()))
        log_action("{}: New message incoming from @{} in channel #{}".format(
            ts, message.author, message.channel))

        if (bot_sync.is_action_too_soon()):
            await message.channel.send("Μην βιάζεσαι μαγκάρα.")
        else:
            if (len(sad_message) < 2):
                await message.channel.send("Γράψε κάτι παραπάνω, κουφάλα.")
            else:
                bot_sync.update_last_action()
                self.update_sad(sad_message)
                log_action(
                    "{}: New message added by @{} in channel #{}".format(
                        ts, message.author, message.channel))
                await message.channel.send(
                    "Προστέθηκε νέο ενθαρρυντικό μήνυμα!")
        pass
