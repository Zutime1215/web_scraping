import json
import requests
from cryptography.fernet import Fernet

with open("configme.txt") as file:
    data = json.loads(file.read())
    my_name = data["my_name"]
    key = data["key"]
    url = data["url"][:26]
    room_id = data["url"][27:]


fernet = Fernet(key)

print("type '.exit' (without '') to exit.")
if my_name.__len__() != 0:
	requests.post(url, json = { "room_id": room_id, "name": "<<<>>>", "msg": my_name + " has joined the room." } )

while True:
    if my_name.__len__() == 0:
        print("Please edit configme.py and fillup the 'my_name' variable.")
        break

    else:
        msg = input("Enter your Messege: ")
        if msg == ".exit":
            requests.post(url, json = { "room_id": room_id, "name": "<<<>>>", "msg": my_name + " has left the room." } )
            break
        else:
            encMsg = fernet.encrypt(msg.encode()).decode("utf-8")
            response = requests.post(url, json={"room_id": room_id, "name": my_name, "msg": encMsg})
            
            if response.text != "ok":
                print(">>> Message Cannot Send.Try again.")