
# Get live captains that are on campaign mode and on placement mode
from datetime import datetime, timedelta
import requests, time
import constants
import private_constants
from tasks import open_file, post_to_discord

def check_url():
    gameDataResponse = requests.get(constants.game_url, headers=get_headers())

    # Check if the request was successful (status code 200)
    if gameDataResponse.status_code == 200:
        response_json = gameDataResponse.json()
        
        local_data = open_file()
        local_url = local_data["url"]
        new_url = response_json["info"]["dataPath"]
        if new_url != local_url:
            # Fetch maps from the new url and update the file
            print("Update chests")
        else:
            print("Chests are up to date")
    


def get_headers():
    headers = {"Cookie": "ACCESS_INFO=" + private_constants.token, "User-Agent": constants.user_agent}
    return headers


def get_game_data():

    gameDataResponse = requests.get(constants.game_url, headers=get_headers())

    # Check if the request was successful (status code 200)
    if gameDataResponse.status_code == 200:
        response_json = gameDataResponse.json()

        # Extract version from the JSON response
        # Version which goes in the clientVersion command. _shrug_
        version = response_json["info"]["version"]
        data_version = response_json["info"]["dataVersion"]
        return version, data_version

def get_live_captains():
    live_captains_list = []
    version, data_version = get_game_data()
    
    for i in range(50):
        url = (
            constants.game_url
            + "?cn=getCaptainsForSearch&isPlayingS=desc&isLiveS=desc&page="
            + str(i)
            + "&format=normalized&seed=270&resultsPerPage=30&filters={%22favorite%22:false,%22isPlaying%22:1,%22ambassadors%22:%22false%22}&clientVersion="
            + version
            + "&clientPlatform=WebGL&gameDataVersion="
            + data_version
            + "&command=getCaptainsForSearch&isCaptain=0"
        )

        response = requests.get(url, headers=get_headers())

        live_captains_list.append(response.json())
        if response.json()["data"] is None or response.json()["data"]["captains"] == []:
            break

        time.sleep(0.2)


    captains_data_list = [entry["data"]["captains"] for entry in live_captains_list]
    merged_data = [
        captain for captains_data in captains_data_list for captain in captains_data
    ]
    tuples = {tuple(item.items()) for item in merged_data}
    merged_data = [dict(t) for t in tuples]
    return merged_data


# Filter captains in active placement and loyalty chests
def get_special_chests(campaign_captains):
    # Join battle, check time and check chests. If loyalty chest add it to the returning list
    version, data_version = get_game_data()
    headers = get_headers()
    # Join each battle, check the timer and the chest type
    for captain in campaign_captains:

        # Add captain to the slot
        add_raid_url = (constants.game_url
        + "?cn=addPlayerToRaid&captainId="
        + captain["userId"]
        + "&userSortIndex=0&clientVersion="
        + version
        + "&clientPlatform=WebGL&gameDataVersion="
        + data_version +
        "&command=addPlayerToRaid&isCaptain=0")
        
        requests.get(add_raid_url, headers=headers)
        
        time.sleep(0.2)
        # Get raid info
        get_raid_url = (constants.game_url
                        + "?cn=getActiveRaidsByUser&clientVersion="
                        + version + "&clientPlatform=WebGL&gameDataVersion="
                        + data_version
                        + "&command=getActiveRaidsByUser&isCaptain=0")
        raid = requests.get(get_raid_url, headers=headers).json()["data"]
        if len(raid) == 0:
            leave_raid(captain_id, data_version, version, headers)
            continue
        captain_name = raid[0]["twitchDisplayName"]
        captain_id = raid[0]["userId"]
        map_node = raid[0]["nodeId"]
        creation_date = raid[0]["creationDate"]
        
        if creation_date is None:
            leave_raid(captain_id, data_version, version, headers)
            continue
         
        # Check raid age
        utc_now = datetime.utcnow()
        creation_date = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
        time_difference = utc_now - creation_date
        if time_difference > timedelta(minutes=30):
            leave_raid(captain_id, data_version, version, headers)
            continue
        
        # Get time remaining
        time_remaining_timedelta = timedelta(minutes=30) - (utc_now - creation_date)
        minutes_remaining = time_remaining_timedelta.seconds // 60
        seconds_remaining = time_remaining_timedelta.seconds % 60
        time_remaining_str = f"{minutes_remaining:02}:{seconds_remaining:02}"
        
        
        
        loyalty_chests = open_file()["MapNodes"]
        for node_key, node_data in loyalty_chests.items():
            if node_key == map_node:
                chest_type = node_data.get("ChestType", "Unknown")
                post_to_discord(captain_name, chest_type, time_remaining_str)
                leave_raid(captain_id, data_version, version, headers)
                continue
                
        leave_raid(captain_id, data_version, version, headers)


def leave_raid(captain_id, data_version, version, headers):
    leave_raid_url = (constants.game_url
                      + "?cn=leaveCaptain&userId="
                      + private_constants.user_id
                      + "&isCaptain=0&gameDataVersion="
                      + data_version
                      + "&command=leaveCaptain&captainId="
                      + captain_id
                      + "&clientVersion="
                      + version
                      + "&clientPlatform=WebGL")
    
    requests.get(leave_raid_url, headers=headers)
    
    time.sleep(0.2)

    pass