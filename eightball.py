import bot_sync
import random

"""
8ball command

Usage:
8ball <question> e.g. 8ball Will I ever become cool?
"""
class Eightball():
  words = [
      "Δεν έχω ιδέα μαγκάρα.", 
      "Σίγουρα θα γίνει.", 
      "Πιθανό αλλά δεν το βλέπω.",
      "Καλύτερα μην σε πω τώρα...", 
      "Συγκεντρόσου και ρώτισε ξανά.",
      "Αρκετά πιθανό να γίνει.", 
      "Εγώ λέω όχι.", 
      "Δεν έχω ιδέα.", 
      "Που να ξέρω;",
      "Όπως βλέπω τα πράγματα τώρα, ποντάρω στο ότι θα γίνει.",
      "Sorry δεν πρόσεχα ξαναρώτα λίγο.",
      "Γράψε 'sad' γιατί αυτό βλέπω να γίνεται."
  ]

  msg_error_action_too_fast = "Μην βιάζεσαι μαγκάρα."
  msg_error_action_invalid = "Ρώτα κάτι μαγκάρα αλλιώς τι να προβλέπω;"

  def __init__(self, name):
    self.name = name
    pass

  async def command(self, message):
    has_question = message.content.split(self.name + " ", 1)

    if (bot_sync.is_action_too_soon()):
        await message.channel.send(self.msg_error_action_too_fast)
    else:
        bot_sync.update_last_action()
        if (len(has_question) == 1):
            await message.channel.send(self.msg_error_action_invalid)
        else:
            await message.channel.send(random.choice(self.words))

    pass
