import json
import requests
from cryptography.fernet import Fernet

def generateKey():
    return Fernet.generate_key()

base_url   = "http://localhost:8080"
create_url = base_url + "/createRoom"
rooms_url  = base_url + "/rooms"

while True:
    n = input("""
Press 1 - To create a Room.
Press 2 - To see the List of The Rooms.
Press 0 - To Exit
>>> """)

    if n == "1":
        name = input("<<<>>> Enter Your Room Name: ")
        desc = input("<<<>>> Enter Your Room Description: ")
        r = requests.post(create_url, json={"name": name, "description": desc})
        r = json.loads(r.text)
        if r["status"] == 133:
            print("<<<<>>> Your Room Name must be in 32 Characters. Your Room description must be in 100 Characters.")
        elif r["status"] == 132:
            print("\n")
            print("<<<>>> Edit the configme.txt file and replace the url to " + r["url"] )
            print(f"<<<>>> Here is your key => {generateKey().decode()}")
            print("<<<>>> This key is client side generated. Server do not have this. Anyone with this key and url can read your message! Store this key. without it, you cannot decrypt messages.")
    elif n == "2":
        r = json.loads(requests.get(rooms_url).text)
        print("\n")
        if len(r) == 0:
            print("No Chan yet!")
        else:
            for i in r:
                print(f'''<<<>>> {i["name"]} - {i["description"]} - Created {i["created"]}''')
    elif n == "0":
        break
