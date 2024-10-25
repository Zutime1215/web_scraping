import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

base_url = "https://atcoder.jp"
atcoder_page = "https://atcoder.jp/contests/"

def epoch_converter(time):
	dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S%z")
	return int(dt.timestamp())

def atcoder(futuTime):
	res = requests.get(atcoder_page).text

	soup = BeautifulSoup(res, 'html.parser')
	contest_div = soup.find(id='contest-table-upcoming')
	contest_tbody = contest_div.find('tbody')
	contests = contest_tbody.find_all('tr')

	atco = []
	tomo_time = time.time() + (futuTime*86400)

	for i in contests:
		octa = {}
		a_tags = i.find_all('a')
		tm = epoch_converter(a_tags[0].text)
		
		if tm <= tomo_time:
			octa['title'] = a_tags[1].text
			octa['startTime'] = tm
			duration_list = (i.find_all('td')[-2].text).split(':')
			octa['duration'] = int(duration_list[0])*60 + int(duration_list[1])
			octa['link'] = base_url + a_tags[1]['href']

			atco.append(octa)

	return atco