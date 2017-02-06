import settings
import dataset
import json


db = dataset.connect(settings.CONNECTION_STRING)
result = db.query("SELECT lat,lng FROM geocoords ORDER BY tm DESC LIMIT 1")
dataset.freeze(result, format='json', filename="recent.json")
with open('recent.json') as json_data:
    d = json.load(json_data)
del d['count']
del d['meta']
# Output the updated file with pretty JSON                                      
open("recent.json", "w").write(
    json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))
)