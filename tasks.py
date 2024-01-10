

# Local tasks
# Filter captains on active placement campaign 

import datetime, json, time, requests
import private_constants
import constants

def open_file():
    with open('loyalty_chests.json', 'r') as file:
        data = json.load(file)
    return data

def filter_captains(list_of_captains):
    filtered_captains = []
    for captain in list_of_captains:
        if captain is None:
            continue
        else:
            if captain["raidState"] == 4:
                filtered_captains.append(captain)
    return filtered_captains

def post_to_discord(captain_name, chest_type, time_remaining):
    chest_name = ""
    if chest_type == "chestbosssuper":
        chest_name = "Loyalty Super Boss Chest"
    elif chest_type == "chestboss":
        chest_name = "Loyalty Boss Chest"
    else:
        for chest in constants.chest_strings:
            if chest_type.startswith(chest["internal"]):
                chest_name = chest["name"]
                break
    for chest in constants.chest_strings:
        if chest_name == chest["name"] and chest["print"]:
            epoch_time = int(time.time())
            current_time = datetime.datetime.now().strftime('%H:%M')
            post_string = f"<t:{epoch_time}:t> - Captain: {captain_name} - {chest_name} - Time remaining: {time_remaining}"
            print(f"{current_time}: Captain: {captain_name} - {chest_name} - Time remaining: {time_remaining}")
            if private_constants.discord is True:
                send_message_to_discord(post_string)
            break
    
def send_message_to_discord(post_string):
    data = {
        "content": post_string
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    requests.post(private_constants.webhook, data=json.dumps(data), headers=headers)