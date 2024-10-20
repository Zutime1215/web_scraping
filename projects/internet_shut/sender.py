import main
from cryptography.fernet import Fernet

cookie = main.main()
groupId = 50
key = b'WCShV4-KysPy2PDa7WoilQM6YrZeRXiNkJgNbJ4YwOY='
fernet = Fernet(key)


def sender():


while True:
	msg = input("Enter your Messege: ")
	if msg == "":
		continue
	elif msg.startswith("#cmd-"):
		command = msg.split("-")[-1]
		if command == 'exit':
			break
		elif command.startswith('dltMsg'):
			message_id = command.split()[-1]
			res = main.deleteMessage(message_id, cookie)
			print("Message id", res["remove_data"]["message_id"][0], "Removed.")

		continue
	else:
		encMsg = fernet.encrypt(msg.encode()).decode("utf-8")
		response = main.sendMessage(groupId, encMsg, cookie)
		status = response["success"]
		message_id = response["message"]["messages"][0]["message_id"]
	if status: print("Success. Message id =", message_id)
	else: print("Failed")



#cmd-dltMsg 2020
#cmd-rplMsg 2020 this is the reply