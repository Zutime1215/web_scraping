import requests
import json
import time

codeforces_api = "https://codeforces.com/api/contest.list"

def codeforces(futuTime):
	res = json.loads(requests.get(codeforces_api).text)
	result = res['result']

	forces = []
	tomo_time = time.time() + (futuTime*86400)

	for i in result:
		secrof = {}
		if (i['phase'] == 'BEFORE' or i['phase'] == 'CODING'):
			if i['startTimeSeconds'] <= tomo_time:
				secrof['title'] = i['name']
				secrof['startTime'] = i['startTimeSeconds']
				secrof['duration'] = int(i['durationSeconds']/60)
				secrof['link'] = 'https://codeforces.com/contests'

				forces.append(secrof)
		else:
			break

	return forces