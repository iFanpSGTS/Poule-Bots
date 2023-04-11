import json

with open('./data/config.json', 'r') as f:
    config = json.load(f)

bot_token = config['bot_token']