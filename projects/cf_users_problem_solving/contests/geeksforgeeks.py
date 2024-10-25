import requests
import json
import time
from datetime import datetime

base_url = "https://practice.geeksforgeeks.org/contest/"
geeks_api = "https://practiceapi.geeksforgeeks.org/api/vr/events/?page_number=1&sub_type=all&type=contest"

def epoch_converter(time):
	dt = datetime.fromisoformat(time)
	return int(dt.timestamp())

def geeksforgeeks(futuTime):
	res = json.loads(requests.get(geeks_api).text)['results']['upcoming']

	geek = []
	tomo_time = time.time() + (futuTime*86400)

	for i in res:
		keeg = {}
		tm = epoch_converter(i['start_time'])

		if tm <= tomo_time:
			keeg['title'] = i['name']
			keeg['startTime'] = tm
			keeg['duration'] = int((epoch_converter(i['end_time'])-tm)/60)
			keeg['link'] = base_url + i['slug']

			geek.append(keeg)

	return geek