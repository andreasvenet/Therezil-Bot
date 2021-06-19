import discord
import os
import requests
import json
import random
import time
from replit import db
from keep_alive import keep_alive

last_action_time = int(time.time())
cooldown = random.randint(5,
                          random.randint(10, int(time.time() / 100000000 - 1)))


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


def log_action(action):
    print(action)
    if "actions" in db.keys():
        actions = db["actions"]
        actions.append(json.dumps({"action": action}))
        db["actions"] = actions
    else:
        db["actions"] = [action]


def is_action_too_soon():
    if (last_action_time + cooldown >= int(time.time())):
        return True
    return False


client = discord.Client()

sad_words = [
    "sad", "depressed", "unhappy", "miserable", "depressing", "magkaras",
    "malakas", "θλιψη", "thlipsi", "θλίψη", "tsiab", "σαδ"
]

if "responding" not in db.keys():
    db["responding"] = True

starter_encouragements = ["o magaras einai t-word"]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


def update_last_action():
    global last_action_time
    last_action_time = int(time.time())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))
            if (random.randint(1, 100) > 69):
              await message.channel.send(random.choice(options))
              if (random.randint(1, 100) > 98):
                await message.channel.send(random.choice(options))

    if msg.startswith("8ball"):
      has_question = msg.split("8ball ", 1)
      
      predictions = ["Δεν έχω ιδέα μαγκάρα.", "Σίγουρα θα γίνει.", "Πιθανό αλλά δεν το βλέπω.", "Καλύτερα μην σε πω τώρα...", "Συγκεντρόσου και ρώτισε ξανά.", "Αρκετά πιθανό να γίνει.", "Εγώ λέω όχι.", "Δεν έχω ιδέα.", "Που να ξέρω;", "Όπως βλέπω τα πράγματα τώρα, ποντάρω στο ότι θα γίνει.", "Sorry δεν πρόσεχα ξαναρώτα λίγο.", "Γράψε 'sad' γιατί αυτό βλέπω να γίνεται."]

      if (is_action_too_soon()):
          await message.channel.send("Μην βιάζεσαι μαγκάρα.")
      else:
          update_last_action()
          if (len(has_question) == 1):
            await message.channel.send("Ρώτα κάτι μαγκάρα αλλιώς τι να προβλέπω;")
          else:
            await message.channel.send(random.choice(predictions))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        ts = time.ctime(int(time.time()))
        log_action("{}: New message incoming from @{} in channel #{}".format(
            ts, message.author, message.channel))

        if (is_action_too_soon()):
            await message.channel.send("Μην βιάζεσαι μαγκάρα.")
        else:
            if (len(encouraging_message) < 2):
                await message.channel.send("Γράψε κάτι παραπάνω, κουφάλα.")
            else:
                update_last_action()
                update_encouragements(encouraging_message)
                log_action(
                    "{}: New message added by @{} in channel #{}".format(
                        ts, message.author, message.channel))
                await message.channel.send(
                    "Προστέθηκε νέο ενθαρρυντικό μήνυμα!")

    if msg.startswith("$del"):
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_encouragement(index)
        ts = time.ctime(int(time.time()))
        log_action("{}: Message {} deleted by @{} in channel #{}".format(
            ts, index, message.author, message.channel))
        await message.channel.send(
            "Message with id {} has been deleted!".format(index))

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")


keep_alive()
client.run(os.getenv('TOKEN'))
