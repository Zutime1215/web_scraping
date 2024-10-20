import main
from time import sleep
from cryptography.fernet import Fernet

cookie = main.main()
groupId = 50
key = b'WCShV4-KysPy2PDa7WoilQM6YrZeRXiNkJgNbJ4YwOY='
fernet = Fernet(key)
timer = 2

j = 0
while True:
	messages = main.readMessage(groupId, cookie)["messages"]
	for i in range(-1, -len(messages)-1, -1):
		message_id = messages[i]["message_id"]

		if message_id > j:
			user = messages[i]["posted_by"]
			user_id = messages[i]["sender_user_id"]
			date = messages[i]["date"]
			time = messages[i]["time"]
			content = messages[i]["content"]
			decryptContent = fernet.decrypt(bytes(content, "utf-8")).decode()
			print(f'''{user}({user_id}) || {date}( {time} )\n({message_id}) ==> {content}\n''')

	j = message_id
	sleep(timer)