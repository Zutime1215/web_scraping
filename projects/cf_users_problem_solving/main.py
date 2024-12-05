import json
import requests
import datetime
from time import sleep, time
from collections import defaultdict as dd
from pathlib import Path

from contests.codechef import codechef
from contests.codeforces import codeforces
from contests.leetcode import leetcode
from contests.atcoder import atcoder
from contests.geeksforgeeks import geeksforgeeks

home_dir = Path.home()
file_path = home_dir / '.imp.json'
with file_path.open("r") as f:
	all_info = json.loads(f.read())
	bot_token = all_info['cf_users_problem_solve_finder_api']

cf_url = "https://codeforces.com/api/user.status?count=50&handle="

def file(file_name, mode, text=None):
	if mode == 'write':
		with open(file_name, 'w') as fl: fl.write(str(text))
	else:
		with open(file_name, 'r') as fl: return fl.read()
		

def setime(epoc, phase):
	mytimestamp = datetime.datetime.fromtimestamp(epoc)
	datetime_str = mytimestamp.strftime(phase)
	return datetime_str

def requesting(url):
	try:
		return requests.get(url).text
	except Exception as e:
		print(e)
		sleep(20)
		requesting(url)

def sendMessage(text, chat_id=2048432908, thread_id=""):
	snd_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&message_thread_id={thread_id}&text={text}&parse_mode=Markdown"
	try:
		res = requesting(snd_url)
		return res
	except Exception as e:
		print(e)
		sleep(20)
		sendMessage(text, chat_id, thread_id)


def getUpdates():
	get_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
	try:
		res = json.loads(requesting(get_url))
		return res
	except Exception as e:
		print(e)
		sleep(20)
		getUpdates()


def theMain(handles, epoch):
	message = "```" + setime(epoch, '%Y-%m-%d') + "\n"

	for handle in handles:
		rspns = json.loads(requesting(cf_url+handle))
		stat = rspns['status']
		result = rspns["result"]
		
		if stat == 'FAILED':
			message += (rspns["comment"] + "\n")
		elif len(result) == 0:
			message += f"{handle}: no solve yet\n"

		else:
			i = 0
			total_tried = set()
			accepted = set()
			l = dd(set)

			while result[i]["creationTimeSeconds"] >= epoch:
				rslt = result[i]
				prblm = rslt['problem']
				verdict = rslt["verdict"]
				
				if "contestId" in prblm.keys():
					problem_path = f'{prblm["contestId"]}/{prblm["index"]}'
				elif prblm["problemsetName"] == "acmsguru":
					problem_path = f'acmsguru/{prblm["index"]}'

				
				if "rating" in prblm.keys():
					rating = rslt["problem"]['rating']
				else:
					rating = None


				total_tried.add(problem_path)
				if verdict == 'OK':
					accepted.add(problem_path)

				
				l[prblm.get('rating')].add(f'{problem_path}')
				
				i+=1

			if len(total_tried) == 0:
				msg = ""
			else:
				rate = ""
				for k,v in l.items():
					rate += f"Rating({k}): {v}\n"
				msg = f"""{handle}:\nTotal Tried: {len(total_tried)}\nAccepted: {len(accepted)}\n{rate}\n"""
			
			message += msg
	return message


def contest_msg():
	con_msg = "::Upcoming Contests::\n"
	ojs = [codeforces, codechef, leetcode, atcoder, geeksforgeeks]
	for oj in ojs:
		cons = oj(1)
		if len(cons) == 0:
			continue
		for con in cons:
			con_msg += f'''Name: {con['title']}\nTime: {setime(con['startTime'], '%d.%m %H:%M')}\nDuration: {con['duration']} Min\n{con['link']}\n\n'''
	return con_msg


todays_epoch = int(file("lastEpoch.txt", "read"))
while True:
	if time() >= todays_epoch+86400:

		con_msg = contest_msg()
		profiles = json.loads(file("handles.json", "read"))
		for key,value in profiles.items():
			chat_id = value["chat_id"]
			thread_id = "" if value["message_thread_id"] == -1 else value["message_thread_id"]
			handles = value["handles"]
			message = theMain(handles, todays_epoch)
			if len(message) < 25:
				message = f'''```{setime(todays_epoch, '%Y-%m-%d')}\nEkjon o korlo na, so sad!!!\n{con_msg}```'''
			else:
				message += '\n' + con_msg + "```"
			
			sendMessage(message, chat_id, thread_id)
			# sendMessage(message)

		todays_epoch += 86400
		file("lastEpoch.txt", "write", todays_epoch)
	
	sleep(3600)