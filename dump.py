import pickledb
import json

db = pickledb.load('example.db', False)

data = {}
for key in db.getall():
    if key=="i": continue
    data[key] = db.get(key)


with open('data.json', 'w') as outfile:
    json.dump(data, outfile)