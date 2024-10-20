import json
from thefuzz import fuzz, process

with open("./output.json", 'r') as file:
    data = json.loads(file.read())

titles = [i["title"] for i in data]
des = [i["description"] for i in data]

inp = "drakula story"

title_sim = process.extract(inp, titles, limit=5, scorer=fuzz.token_sort_ratio)
des_sim = process.extract(inp, des, limit=5, scorer=fuzz.token_sort_ratio)

print(title_sim)
print(des_sim)