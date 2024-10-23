import requests
import json
import time
from datetime import datetime

base_url = 'https://www.codechef.com/'
codechef_api = "https://www.codechef.com/api/list/contests/all?sort_by=START&sorting_order=asc&offset=0&mode=all"

def epoch_converter(time):
	dt = datetime.fromisoformat(time)
	return int(dt.timestamp())

def codechef(futuTime):
	res = json.loads(requests.get(codechef_api).text)
	result = res['future_contests']

	chef = []
	tomo_time = time.time() + (futuTime*86400)

	for i in result:
		fehc = {}
		tm = epoch_converter(i['contest_start_date_iso'])

		if tm <= tomo_time:
			fehc['title'] = i['contest_name']
			fehc['startTime'] = tm
			fehc['duration'] = i['contest_duration']
			fehc['link'] = base_url + i['contest_code']

			chef.append(fehc)

	return chef