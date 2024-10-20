import json
import time
import requests
import warnings
warnings.filterwarnings('ignore')

api_url = "https://103.162.56.10/chat/api_request/"
loadMedia = {'load': 'group_media_files', 'offset': 0, 'group_id': 50}

def makeRequest(typo, cookie=None):
	return requests.post(api_url, data=typo, cookies=cookie, verify=False)

def sessionRemain(sessionData, cookie):
	cookie["login_session_id"] = sessionData[0]
	cookie["access_code"] = sessionData[1]
	cookie["session_time_stamp"] = sessionData[2]
	return cookie

def sessionExpire(cookie):
	login = {"user": "sirens", "password": "bdixchatkori", "remember_me": "remembe", "add": "login_session"}
	cookieStr = makeRequest(login).headers['Set-Cookie'].split(';')
	cookie["login_session_id"] = cookieStr[0].split('=')[-1]
	cookie["access_code"] = cookieStr[3][21:]
	cookie["session_time_stamp"] = cookieStr[6][28:]
	return cookie

def sendMessage(id, msg, cookie, attach=0):
	sndMsg = {'add': 'message', 'group_id': id, 'message': msg, 'attach_message': attach}
	return json.loads(makeRequest(sndMsg, cookie).text)

def readMessage(id, cookie):
	rdMsg = {'load': 'group_messages', 'group_id': id}
	return json.loads(makeRequest(rdMsg, cookie).text)

def deleteMessage(message_id, cookie):
	dltMsg = {"remove": "group_messages", "message_id": message_id}
	return json.loads(makeRequest(dltMsg, cookie).text)

def groupLists(cookie):
	allGroups = {'load': 'groups', 'filter': 0, 'offset': 1, 'sortby': 0, 'search': 0}
	res = makeRequest(allGroups, cookie)
	print(res.text)

def joinGroup(id):
	jnGrp = {'add': 'group_members', 'group_id': id}
	res = makeRequest(jnGrp, cookie)
	print(res.text)

def leaveGroup(id):
	lvGrp = {'remove': 'group_members', 'info_box': 'true', 'group_id': id}
	res = makeRequest(lvGrp, cookie)
	print(res.text)


def main():
	cookie = {"current_color_scheme": "0", "current_language_id": "0"}
	with open('sessionId.txt') as file:
		sessionData = file.read().split('-')

	if int(sessionData[-1]) + 2419200 > time.time():
		cookie = sessionRemain(sessionData, cookie)
	else:
		cookie = sessionExpire(cookie)
		with open('sessionId.txt', 'w') as file:
			tempString = f"{cookie['login_session_id']}-{cookie['access_code']}-{cookie['session_time_stamp']}"
			file.write(tempString)

	return cookie