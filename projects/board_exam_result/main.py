import json
import requests
from time import sleep
from scraper import scraper
from urllib.parse import quote_plus

with open('~/.imp.json', "r") as f:
	all_info = json.loads(f.read())
	api = all_info['board_exam_result_telegram_api']

base_url = "https://api.telegram.org/"
update_url = base_url + api + "getUpdates"
send_url = base_url + api + 'sendMessage'

def sender(chat_id, msg):
	send_me = f"{send_url}?chat_id={chat_id}&text={msg}"
	requests.get(send_me)

def remover(update):
	param = {'offset': update}
	requests.get(update_url, params=param)
	print("removed Previous 80")

def receiver():
	msg = requests.get(update_url).text
	msg = json.loads(msg)
	return msg['result']

# -----------------------------------------------------------
normal_reply = '''
Exam id:
   1 JSC/JDC.           5 HSC(Vocational).
   2 SSC/Dakhil.        6 HSC(BM).
   3 SSC(Vocational).   7 Diploma in Commerce.
   4 HSC/Alim.          8 Diploma in Business Studies.
   
Board id:
  1 Barisal.      7 Mymensingh.
  2 Chittagong.   8 Rajshahi.
  3 Comilla.      9 Sylhet.
  4 Dhaka.        10 Madrasah.
  5 Dinajpur.     11 Technical.
  6 Jessore.      12 DIBS(Dhaka).

Send Info in this Format.
2-3-2020-159876-1711997465
(Exam id)-(Board id)-(Year)-(Roll)-(Registration)
'''
# ----------------------------------------------------------


def main():

	while True:
		all_message = receiver()
		number_of_message = all_message[-1]['update_id'] - all_message[0]['update_id']

		if number_of_message > 50:
			remover(all_message[-1]['update_id'])
			all_message = receiver()

		for ith in all_message:
			try:
				chat_id = ith['message']['from']['id']
				message = ith['message']['text']
				pro_epoch = ith['message']['date']

				with open('last_epoch.txt', 'r') as r:
					pre_epoch = int(r.read())


				if ( len(message) < 26 or len(message) > 27 ) and pro_epoch > pre_epoch:
					sender(chat_id, normal_reply)

					with open('last_epoch.txt', 'w') as w:
						w.write(str(pro_epoch))

				else:	
					if pro_epoch > pre_epoch:
						sender(chat_id, 'Please Wait For A Moment....')

						with open('last_epoch.txt', 'w') as w:
							w.write(str(pro_epoch))

						try:
							data = message.split('-')
							if len(data) != 5:
								sender(chat_id, "Your Given Data is wrong Or Format is Invalid.\n" + normal_reply)
								continue
							else:
								return_string = scraper(int(data[0]), int(data[1]), data[2], data[3], data[4])
								sender(chat_id, quote_plus(return_string))
						except:
							sender(chat_id, "Your Given Data is wrong Or Format is Invalid.\n" + normal_reply)
							continue
			except:
				continue
		sleep(1)
		# print('For Loop Complete')

main()
