else:
    res = getUpdates()
    all_message = res['result']
    if len(all_message) == 0: continue
    last_update_id = int(file('lastUpdateId.txt', 'read'))

    for i in all_message:
        try: type = i['message']['entities'][0]['type']
        except: type = None
        if type == 'bot_command' and i['update_id'] > last_update_id:
            chat_id = i['message']['chat']['id']
            try: thread_id = i['message']['message_thread_id']
            except: thread_id = ""
            bot_cmd_msg = i['message']['text']

            if '/stat' in bot_cmd_msg:
                try:
                    handles = bot_cmd_msg.split()[1].split("|")[0].split(",")
                    hour = int(bot_cmd_msg.split()[1].split("|")[1])
                except:
                    index_error = "Text Format is Wrong. Try with this format\n```YourBossSays\n/stat handle1,handle2,handle3|6```\nHere 6 means previous 6 hour status"
                    sendMessage(index_error, chat_id, thread_id)
                    continue

                message = theMain(handles, time()-(hour*3600))
                sendMessage(message, chat_id, thread_id)
                # sendMessage(message)

    file("lastUpdateId.txt", "write", all_message[-1]['update_id'])