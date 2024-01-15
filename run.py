
import time
import webhook
from game_requests import check_url, get_live_captains, get_special_chests
from tasks import filter_captains, send_message_to_discord

def run():
    
    while True:
        if webhook.discord is True:
            send_message_to_discord("Beginning cycle.")
        print("Beginning cycle.")
        check_url()
        list_of_captains = get_live_captains()
        campaign_captains = filter_captains(list_of_captains)
        get_special_chests(campaign_captains)
        
        if webhook.discord is True:
            send_message_to_discord("Completed cycle. Sleeping for 3 minutes.")
        
        print("Completed cycle. Sleeping for 1 minute.")
        time.sleep(60)

if __name__ == "__main__":
    run()
