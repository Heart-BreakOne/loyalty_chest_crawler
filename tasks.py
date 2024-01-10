

# Local tasks
# Filter captains on active placement campaign 

import datetime, json, time, requests
import private_constants

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
            if captain["type"] == "1" and captain["raidState"] == 4:
                filtered_captains.append(captain)
    # TODO REMOVE DUPLICATE CAPTAINS
    return filtered_captains

chest_strings = [
    {"internal": "chestboostedgold", "name": "Loyalty Gold Chest"},
    {"internal": "chestboostedtoken", "name": "Loyalty Token Chest"},
    {"internal": "chestboostedscroll", "name": "Loyalty Scroll Chest"},
    {"internal": "chestboostedskin", "name": "Loyalty Skin Chest"},
    {"internal": "chestboostedbeastlands", "name": "Beastlands Chest"},
    {"internal": "chestboostedskinalternate", "name": "Skin Alternate Chest"},
]
def post_to_discord(captain_name, chest_type, time_remaining):
    chest_name = ""
    if chest_type == "chestbosssuper":
        chest_name = "Loyalty Super Boss Chest"
    elif chest_type == "chestboss":
        chest_name = "Loyalty Boss Chest"
    else:
        for chest in chest_strings:
            if chest_type.startswith(chest["internal"]):
                chest_name = chest["name"]
                break
    epoch_time = int(time.time())
    current_time = datetime.datetime.now().strftime('%H:%M')
    post_string = f"<t:{epoch_time}:t> - Captain: {captain_name} - {chest_name} - Time remaining: {time_remaining}"
    print(f"{current_time}: Captain: {captain_name} - {chest_name} - Time remaining: {time_remaining}")
    if private_constants.discord is True:
        send_message_to_discord(post_string)
    
def send_message_to_discord(post_string):
    data = {
        "content": post_string
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    requests.post(private_constants.webhook, data=json.dumps(data), headers=headers)