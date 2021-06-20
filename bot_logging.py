from replit import db
import json

def log_action(action):
    print(action)
    if "actions" in db.keys():
        actions = db["actions"]
        actions.append(json.dumps({"action": action}))
        db["actions"] = actions
    else:
        db["actions"] = [action]