import json

json1_file = open('bottlecaps.json')
json1_str = json1_file.read()
bottlecaps = json.loads(json1_str)
