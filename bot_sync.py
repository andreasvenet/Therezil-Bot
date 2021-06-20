import random
import time

# Post delay setting (Alter carefully, this is to avoid costs!)
last_action_time = int(time.time())
action_cooldown = random.randint(5, random.randint(10, int(time.time() / 100000000 - 1)))

def update_last_action():
    global last_action_time
    last_action_time = int(time.time())

def is_action_too_soon():
    if (last_action_time + action_cooldown >= int(time.time())):
        return True
    return False
