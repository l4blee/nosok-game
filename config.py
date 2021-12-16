import json

with open('./config.json') as f:
    variables = json.load(f)

for var in variables.items():
    exec(f'{var[0]} = {var[1]}')

del var, variables
