import requests
import json
import time

base_url = "https://leetcode.com/contest/"
leetcode_api = "https://leetcode.com/graphql"
query = {
    "query": """
    {
        upcomingContests {
            title
            startTime
            duration
            titleSlug
        }
    }
    """
}


def leetcode(futuTime):
	res = json.loads(requests.post(leetcode_api, json=query).text)
	upcomingContests = res['data']['upcomingContests']
	leet = []
	tomo_time = time.time() + (futuTime*86400)
	for i in upcomingContests:
		teel = {}
		if i['startTime'] <= tomo_time:
			teel['title'] = i['title']
			teel['startTime'] = i['startTime']
			teel['duration'] = i['duration']/60
			teel['link'] = base_url + i['titleSlug']

			leet.append(teel)

	return leet